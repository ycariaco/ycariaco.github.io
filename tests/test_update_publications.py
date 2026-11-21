"""Regression tests for author matching and safe publication updates."""

import copy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("update_publications", ROOT / "bin/update_publications.py")
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)
CONFIG = json.loads((ROOT / "_data/publication_sources.json").read_text())


def record(**overrides):
    value = {
        "id": "12345678",
        "source": "MED",
        "pmid": "12345678",
        "doi": "10.1234/example",
        "title": "An example study",
        "pubYear": "2026",
        "journalInfo": {"journal": {"title": "Example Journal"}},
        "pubTypeList": {"pubType": ["Journal Article"]},
        "authorList": {"author": [{"firstName": "Yusmaris", "lastName": "Cariaco", "fullName": "Cariaco Y"}]},
    }
    value.update(overrides)
    return value


def catalogue():
    return [{
        "id": "curated_example", "title": "Curated study title", "authors": ["Yusmaris Cariaco"],
        "year": 2026, "journal": "Curated Journal", "doi": "10.1234/example", "pmid": "11111111", "tags": ["Placenta"]
    }]


class AuthorMatchingTests(unittest.TestCase):
    def test_full_name_is_accepted_but_initial_only_is_not(self):
        self.assertTrue(sync.matches_author(record(), CONFIG))
        initial_only = record(authorList={"author": [{"firstName": "Y", "lastName": "Cariaco", "fullName": "Cariaco Y"}]})
        self.assertFalse(sync.matches_author(initial_only, CONFIG))

    def test_matching_orcid_accepts_initials(self):
        item = record(authorList={"author": [{
            "firstName": "Y", "lastName": "Cariaco",
            "authorId": {"type": "ORCID", "value": "https://orcid.org/" + CONFIG["orcid"]}
        }]})
        self.assertTrue(sync.matches_author(item, CONFIG))

    def test_conflicting_orcid_rejects_an_identical_name(self):
        item = record()
        item["authorList"]["author"][0]["authorId"] = {"type": "ORCID", "value": "0000-0001-1111-1111"}
        self.assertFalse(sync.matches_author(item, CONFIG))

    def test_name_alias_is_supported(self):
        item = record(authorList={"author": [{"firstName": "Yusmaris Josefina", "lastName": "Cariaco Sifontes"}]})
        self.assertTrue(sync.matches_author(item, CONFIG))


class MergeTests(unittest.TestCase):
    def test_case_insensitive_doi_corrects_pmid_and_preserves_curated_fields(self):
        existing = catalogue()
        original = copy.deepcopy(existing)
        existing[0]["doi"] = "https://doi.org/10.1234/EXAMPLE"
        updated, summary = sync.merge_publications(existing, [record()], CONFIG)
        self.assertEqual(len(updated), 1)
        self.assertEqual(updated[0]["pmid"], "12345678")
        for field in ("id", "title", "authors", "journal", "tags"):
            self.assertEqual(updated[0][field], original[0][field])
        self.assertEqual(existing[0]["pmid"], "11111111")
        self.assertEqual(summary["corrected_pmids"], 1)

    def test_new_papers_added_once_and_results_are_idempotent(self):
        candidate = record(doi="10.1234/new", title="New study", pmid="22222222", id="22222222")
        updated, summary = sync.merge_publications(catalogue(), [record(), candidate, candidate], CONFIG)
        self.assertEqual(len(updated), 2)
        self.assertEqual(summary["added"], 1)
        repeat, repeated_summary = sync.merge_publications(updated, [candidate, record()], CONFIG)
        self.assertEqual(repeat, updated)
        self.assertEqual(repeated_summary["added"], 0)
        self.assertEqual(repeated_summary["corrected_pmids"], 0)

    def test_existing_paper_missing_from_api_is_never_removed(self):
        item = record(doi="10.1234/new", title="New study", pmid="22222222", id="22222222")
        updated, _ = sync.merge_publications(catalogue(), [item], CONFIG)
        self.assertEqual(updated[0], catalogue()[0])
        self.assertEqual(len(updated), 2)

    def test_conflicting_doi_does_not_merge_unrelated_pmid(self):
        item = record(doi="10.1234/new", title="Another actual paper", pmid="11111111", id="11111111")
        updated, _ = sync.merge_publications(catalogue(), [item], CONFIG)
        self.assertEqual(len(updated), 2)
        self.assertEqual(updated[0], catalogue()[0])

    def test_preprints_and_retractions_are_excluded(self):
        for kind in ("Preprint", "Published Erratum", "Retracted Publication"):
            item = record(pubTypeList={"pubType": ["Journal Article", kind]})
            self.assertIsNone(sync.record_to_publication(item, CONFIG))
        self.assertIsNone(sync.record_to_publication(record(source="PPR"), CONFIG))

    def test_incomplete_verified_record_aborts(self):
        with self.assertRaises(sync.SyncError):
            sync.merge_publications(catalogue(), [record(title="")], CONFIG)

    def test_external_markup_becomes_plain_text(self):
        item = sync.record_to_publication(record(title="Study of <i>Placenta</i> &amp; growth"), CONFIG)
        self.assertEqual(item["title"], "Study of Placenta & growth")

    def test_duplicate_dois_in_existing_data_fail_validation(self):
        existing = catalogue()
        duplicate = copy.deepcopy(existing[0])
        duplicate["id"] = "other"
        duplicate["doi"] = "10.1234/EXAMPLE"
        with self.assertRaises(sync.SyncError):
            sync.validate_publications(existing + [duplicate])


class FetchAndWriteTests(unittest.TestCase):
    def test_search_limits_all_author_variants_to_journal_types(self):
        captured = []

        def fetch(url):
            captured.append(url)
            return json.dumps({"esearchresult": {"count": "0", "idlist": []}}).encode()

        with self.assertRaises(sync.SyncError):
            sync.fetch_records(CONFIG, fetch=fetch)
        query = parse_qs(urlparse(captured[0]).query)["term"][0]
        author_query, type_query = query.split(") AND (")
        self.assertIn(CONFIG["orcid"], author_query)
        self.assertIn("Cariaco Sifontes Yusmaris", author_query)
        self.assertIn('"journal article"[Publication Type]', type_query)
        self.assertIn('"review"[Publication Type]', type_query)

    def test_checkpoint_updates_monthly_or_when_catalogue_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            first_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
            first, changed = sync.checkpoint_update(path, catalogue(), CONFIG, first_date)
            self.assertTrue(changed)
            self.assertEqual(first["publication_count"], 1)
            sync.atomic_write(path, first)
            next_day, changed = sync.checkpoint_update(path, catalogue(), CONFIG, first_date + timedelta(days=1))
            self.assertFalse(changed)
            self.assertEqual(next_day, first)
            next_month, changed = sync.checkpoint_update(path, catalogue(), CONFIG, first_date + timedelta(days=28))
            self.assertTrue(changed)
            self.assertNotEqual(next_month["last_recorded_success"], first["last_recorded_success"])
            updated = catalogue()
            updated[0]["pmid"] = "22222222"
            revised, changed = sync.checkpoint_update(path, updated, CONFIG, first_date + timedelta(days=1))
            self.assertTrue(changed)
            self.assertNotEqual(revised["catalogue_sha256"], first["catalogue_sha256"])

    def test_incomplete_search_fails_closed(self):
        response = json.dumps({"esearchresult": {"count": "2", "idlist": ["12345678"]}}).encode()
        with self.assertRaises(sync.SyncError):
            sync.fetch_records(CONFIG, fetch=lambda _: response)

    def test_missing_fetched_article_fails_closed(self):
        responses = iter([
            json.dumps({"esearchresult": {"count": "1", "idlist": ["12345678"]}}).encode(),
            b"<PubmedArticleSet></PubmedArticleSet>",
        ])
        with self.assertRaises(sync.SyncError):
            sync.fetch_records(CONFIG, fetch=lambda _: next(responses))

    def test_nested_title_and_author_identifiers_from_pubmed(self):
        xml = b"""<PubmedArticleSet><PubmedArticle>
        <MedlineCitation><PMID>12345678</PMID><Article>
          <ArticleTitle>NAD<sup>+</sup> and &amp; cell growth</ArticleTitle>
          <Journal><Title>Example Journal</Title><JournalIssue><PubDate><Year>2026</Year></PubDate></JournalIssue></Journal>
          <AuthorList><Author><ForeName>Yusmaris</ForeName><LastName>Cariaco</LastName>
            <Identifier Source="ORCID">0000-0003-3473-3555</Identifier></Author></AuthorList>
          <PublicationTypeList><PublicationType>Journal Article</PublicationType></PublicationTypeList>
        </Article></MedlineCitation>
        <PubmedData><ArticleIdList><ArticleId IdType="doi">10.1234/example</ArticleId></ArticleIdList></PubmedData>
        </PubmedArticle></PubmedArticleSet>"""
        records = sync.parse_pubmed_xml(xml)
        self.assertEqual(records[0]["title"], "NAD+ and & cell growth")
        self.assertTrue(sync.matches_author(records[0], CONFIG))
        responses = iter([
            json.dumps({"esearchresult": {"count": "1", "idlist": ["12345678"]}}).encode(), xml,
        ])
        self.assertEqual(sync.fetch_records(CONFIG, fetch=lambda _: next(responses)), records)

    def test_api_failure_leaves_existing_file_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "publications.json"
            checkpoint_path = Path(directory) / "checkpoint.json"
            content = json.dumps(catalogue())
            path.write_text(content)
            checkpoint, _ = sync.checkpoint_update(checkpoint_path, catalogue(), CONFIG)
            sync.atomic_write(checkpoint_path, checkpoint)
            previous_checkpoint = checkpoint_path.read_bytes()
            with patch.object(sync, "fetch_records", side_effect=sync.SyncError("Service unavailable")):
                self.assertEqual(sync.main(["--input", str(path), "--checkpoint", str(checkpoint_path)]), 1)
            self.assertEqual(path.read_text(), content)
            self.assertEqual(checkpoint_path.read_bytes(), previous_checkpoint)

    def test_staged_output_does_not_change_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "publications.json"
            candidate_path = Path(directory) / "candidate.json"
            content = json.dumps(catalogue())
            path.write_text(content)
            with patch.object(sync, "fetch_records", return_value=[record()]), \
                    patch.object(sync, "fetch_preprint_records", return_value=[]), \
                    patch.object(sync, "refresh_citations", side_effect=lambda values, **kwargs: (values, {})):
                self.assertEqual(sync.main(["--input", str(path), "--output", str(candidate_path)]), 0)
            self.assertEqual(path.read_text(), content)
            self.assertEqual(json.loads(candidate_path.read_text())[0]["pmid"], "12345678")

    def test_dry_run_does_not_write_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "publications.json"
            candidate_path = Path(directory) / "candidate.json"
            checkpoint_path = Path(directory) / "checkpoint.json"
            content = json.dumps(catalogue())
            path.write_text(content)
            with patch.object(sync, "fetch_records", return_value=[record()]), \
                    patch.object(sync, "fetch_preprint_records", return_value=[]), \
                    patch.object(sync, "refresh_citations", side_effect=lambda values, **kwargs: (values, {})):
                self.assertEqual(sync.main([
                    "--input", str(path), "--output", str(candidate_path), "--checkpoint", str(checkpoint_path), "--dry-run"
                ]), 0)
            self.assertEqual(path.read_text(), content)
            self.assertFalse(candidate_path.exists())
            self.assertFalse(checkpoint_path.exists())


PREPRINT_DOI = "10.64898/2026.09.17.752392"


def crossref_preprint(**overrides):
    item = {
        "DOI": PREPRINT_DOI, "type": "posted-content", "subtype": "preprint",
        "title": ["Publisher title"], "institution": [{"name": "bioRxiv"}],
        "author": [{"given": "Yusmaris", "family": "Cariaco", "ORCID": "https://orcid.org/" + CONFIG["orcid"]}],
        "published": {"date-parts": [[2026, 9, 18]]}, "is-referenced-by-count": 0,
    }
    item.update(overrides)
    return item


def preprint_detail(**overrides):
    detail = {
        "doi": PREPRINT_DOI, "server": "bioRxiv", "version": "1",
        "date": "2026-09-18", "title": "Prenatal fentanyl and Δ9-tetrahydrocannabinol",
        "published": "NA", "type": "new results",
    }
    detail.update(overrides)
    return detail


def encoded(value):
    return json.dumps(value).encode()


def preprint_payload(*versions):
    return encoded({"messages": [{"status": "ok"}], "collection": list(versions)})


def preprint_record(**overrides):
    item = record(
        source="PPR", id=PREPRINT_DOI, doi=PREPRINT_DOI, pmid="",
        title="A preprint study", verified_preprint_server="biorxiv",
        journalInfo={"journal": {"title": "bioRxiv"}}, pubTypeList={"pubType": ["Preprint"]},
    )
    item.update(overrides)
    return item


class PreprintDiscoveryTests(unittest.TestCase):
    def setUp(self):
        sleep = patch.object(sync.time, "sleep")
        sleep.start()
        self.addCleanup(sleep.stop)

    def discover(self, items=None, detail=None, config=None, published_records=(), existing=()):
        items = [crossref_preprint()] if items is None else items
        detail = preprint_detail() if detail is None else detail
        calls = []

        def fetch(url):
            calls.append(url)
            if url.startswith(sync.CROSSREF_URL + "?"):
                return encoded({"status": "ok", "message": {"items": items, "total-results": len(items)}})
            if url.startswith(sync.PREPRINT_URL):
                return preprint_payload(detail)
            self.fail("Unexpected source request: " + url)

        records = sync.fetch_preprint_records(
            config or CONFIG, published_records=published_records, existing=existing, fetch=fetch, crossref_cache={}
        )
        return records, calls

    def test_verified_preprint_uses_server_title_and_is_added_once(self):
        records, calls = self.discover()
        self.assertEqual(len(records), 1)
        self.assertEqual(sum(url.startswith(sync.PREPRINT_URL) for url in calls), 1)
        candidate = sync.record_to_publication(records[0], CONFIG)
        self.assertEqual(candidate["kind"], "preprint")
        self.assertEqual(candidate["journal"], "bioRxiv")
        self.assertEqual(candidate["title"], preprint_detail()["title"])
        self.assertEqual(candidate["authors"], ["Yusmaris Cariaco"])
        self.assertEqual(candidate["pmid"], "")
        updated, summary = sync.merge_publications(catalogue(), records, CONFIG)
        self.assertEqual(summary["added"], 1)
        repeated, summary = sync.merge_publications(updated, records, CONFIG)
        self.assertEqual(repeated, updated)
        self.assertEqual(summary["added"], 0)

    def test_unrelated_initials_and_conflicting_orcid_preprints_are_rejected(self):
        authors = [
            {"given": "Iraimys", "family": "Cariaco"},
            {"given": "Y", "family": "Cariaco"},
            {"given": "Yusmaris", "family": "Cariaco", "ORCID": "0000-0001-1111-1111"},
        ]
        for author in authors:
            with self.subTest(author=author):
                records, calls = self.discover([crossref_preprint(author=[author])])
                self.assertEqual(records, [])
                self.assertFalse(any(url.startswith(sync.PREPRINT_URL) for url in calls))

    def test_unapproved_server_and_nonpreprint_posted_content_are_ignored(self):
        for change in ({"institution": [{"name": "Unknown Server"}]}, {"subtype": "other"}):
            with self.subTest(change=change):
                records, _ = self.discover([crossref_preprint(**change)])
                self.assertEqual(records, [])

    def test_known_preprint_is_rechecked_when_search_omits_it(self):
        existing = [sync.record_to_publication(preprint_record(), CONFIG)]
        fetched = []

        def fetch(url):
            fetched.append(url)
            if url.startswith(sync.CROSSREF_URL + "?"):
                return encoded({"status": "ok", "message": {"items": [], "total-results": 0}})
            if url.startswith(sync.CROSSREF_URL + "/"):
                return encoded({"status": "ok", "message": crossref_preprint()})
            return preprint_payload(preprint_detail())

        records = sync.fetch_preprint_records(CONFIG, existing=existing, fetch=fetch)
        self.assertEqual(records[0]["doi"], PREPRINT_DOI)
        self.assertTrue(any(url.startswith(sync.PREPRINT_URL) for url in fetched))

    def test_server_metadata_mismatch_and_incomplete_details_fail_closed(self):
        changes = [
            {"doi": "10.1234/wrong"}, {"server": "medRxiv"}, {"date": "not-a-date"},
            {"title": ""}, {"version": "0"}, {"published": "not-a-doi"},
            {"published": PREPRINT_DOI}, {"type": "withdrawn"},
        ]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(sync.SyncError):
                sync.fetch_preprint_detail(PREPRINT_DOI, "biorxiv", fetch=lambda _: preprint_payload(preprint_detail(**change)))
        incomplete = preprint_detail()
        del incomplete["published"]
        with self.assertRaises(sync.SyncError):
            sync.fetch_preprint_detail(PREPRINT_DOI, "biorxiv", fetch=lambda _: preprint_payload(incomplete))

    def test_latest_version_is_used_but_duplicate_versions_are_rejected(self):
        older = preprint_detail()
        latest = preprint_detail(version="2", title="Revised title", date="2026-10-01")
        detail, _ = sync.fetch_preprint_detail(PREPRINT_DOI, "biorxiv", fetch=lambda _: preprint_payload(latest, older))
        self.assertEqual(detail["title"], "Revised title")
        with self.assertRaises(sync.SyncError):
            sync.fetch_preprint_detail(PREPRINT_DOI, "biorxiv", fetch=lambda _: preprint_payload(older, older))

    def test_user_choice_keeps_nad_preprint_separate_even_if_server_links_article(self):
        doi = "10.1101/2023.09.09.556974"
        self.assertIn(doi, CONFIG["keep_preprints_separate"])
        records, _ = self.discover(
            [crossref_preprint(DOI=doi)], preprint_detail(doi=doi, published="10.1234/example"),
            published_records=[record()],
        )
        self.assertEqual(records[0]["source"], "PPR")
        updated, _ = sync.merge_publications(catalogue(), records, CONFIG)
        self.assertEqual(len(updated), 2)
        self.assertEqual(updated[-1]["doi"], doi)

    def test_official_relationship_promotes_preprint_and_preserves_curated_identity(self):
        existing = [sync.record_to_publication(preprint_record(), CONFIG)]
        existing[0].update(id="curated_preprint", title="Curated title", tags=["Placenta"])
        before = copy.deepcopy(existing)
        records, _ = self.discover(detail=preprint_detail(published="10.1234/example"), published_records=[record()])
        updated, summary = sync.merge_publications(existing, [record(), *records], CONFIG)
        self.assertEqual(len(updated), 1)
        self.assertEqual(summary["promoted_preprints"], 1)
        self.assertEqual(updated[0]["kind"], "article")
        self.assertEqual(updated[0]["doi"], "10.1234/example")
        self.assertEqual(updated[0]["pmid"], "12345678")
        self.assertEqual(updated[0]["preprint_dois"], [PREPRINT_DOI])
        for key in ("id", "title", "authors", "tags"):
            self.assertEqual(updated[0][key], before[0][key])
        self.assertEqual(existing, before)
        repeated, _ = sync.merge_publications(updated, [record(), *records], CONFIG)
        self.assertEqual(repeated, updated)

    def test_preprint_link_is_attached_without_duplicating_existing_article(self):
        records, _ = self.discover(detail=preprint_detail(published="10.1234/example"), published_records=[record()])
        updated, summary = sync.merge_publications(catalogue(), records, CONFIG)
        self.assertEqual(len(updated), 1)
        self.assertEqual(summary["added"], 0)
        self.assertEqual(updated[0]["preprint_dois"], [PREPRINT_DOI])
        self.assertEqual(updated[0]["title"], catalogue()[0]["title"])

    def test_late_relationship_consolidates_versions_without_losing_curated_preprint_data(self):
        preprint = sync.record_to_publication(preprint_record(), CONFIG)
        preprint.update(id="curated_preprint", title="Preprint wording", tags=["Placenta"], citation_count=3, citation_source="Crossref")
        existing = catalogue() + [preprint]
        before = copy.deepcopy(existing)
        linked = record(preprint_dois=[PREPRINT_DOI])
        updated, summary = sync.merge_publications(existing, [preprint_record(), linked], CONFIG)
        self.assertEqual(len(updated), 1)
        self.assertEqual(summary["consolidated_preprints"], 1)
        self.assertEqual(updated[0]["id"], catalogue()[0]["id"])
        self.assertEqual(updated[0]["title"], catalogue()[0]["title"])
        self.assertEqual(updated[0]["preprint_dois"], [PREPRINT_DOI])
        self.assertEqual(updated[0]["preprint_versions"], [before[1]])
        self.assertEqual(existing, before)
        repeated, summary = sync.merge_publications(updated, [linked, preprint_record()], CONFIG)
        self.assertEqual(repeated, updated)
        self.assertEqual(summary["consolidated_preprints"], 0)

    def test_explicit_separate_choice_also_blocks_supplied_merge_relationship(self):
        doi = "10.1101/2023.09.09.556974"
        preprint = sync.record_to_publication(preprint_record(doi=doi), CONFIG)
        existing = catalogue() + [preprint]
        updated, summary = sync.merge_publications(existing, [record(preprint_dois=[doi])], CONFIG)
        self.assertEqual(len(updated), 2)
        self.assertEqual(summary["consolidated_preprints"], 0)
        self.assertEqual(updated[1], preprint)
        self.assertNotIn("preprint_dois", updated[0])

    def test_same_title_without_relationship_does_not_suppress_journal_article(self):
        preprint = sync.record_to_publication(preprint_record(title="An example study"), CONFIG)
        for existing, records in (([preprint], [record()]), (catalogue(), [preprint_record(title="Curated study title")])):
            with self.subTest(existing=existing[0]["doi"]):
                updated, _ = sync.merge_publications(existing, records, CONFIG)
                self.assertEqual(len(updated), 2)
                self.assertEqual({p.get("kind", "article") for p in updated}, {"article", "preprint"})


class CrossrefSafetyTests(unittest.TestCase):
    def setUp(self):
        sleep = patch.object(sync.time, "sleep")
        sleep.start()
        self.addCleanup(sleep.stop)

    def test_complete_paginated_search_accepts_stable_cursor_and_all_records(self):
        pages = iter([
            {"items": [{"DOI": "10.1234/one"}], "total-results": 3, "next-cursor": "stable"},
            {"items": [{"DOI": "10.1234/two"}], "total-results": 3, "next-cursor": "stable"},
            {"items": [{"DOI": "10.1234/three"}], "total-results": 3},
        ])
        urls = []

        def fetch(url):
            urls.append(url)
            return encoded({"status": "ok", "message": next(pages)})

        found = sync.crossref_search({"filter": "type:posted-content"}, fetch)
        self.assertEqual(len(found), 3)
        self.assertEqual(parse_qs(urlparse(urls[-1]).query)["cursor"], ["stable"])

    def test_incomplete_repeated_and_changing_search_results_fail_closed(self):
        scenarios = [
            [{"items": [], "total-results": 1}],
            [{"items": [{"DOI": "10.1234/one"}], "total-results": 2}],
            [{"items": [{"DOI": "10.1234/one"}], "total-results": 2, "next-cursor": "next"},
             {"items": [{"DOI": "10.1234/one"}], "total-results": 2}],
            [{"items": [{"DOI": "10.1234/one"}], "total-results": 2, "next-cursor": "next"},
             {"items": [{"DOI": "10.1234/two"}], "total-results": 3, "next-cursor": "next"}],
        ]
        for responses in scenarios:
            with self.subTest(responses=responses):
                pages = iter(responses)
                with self.assertRaises(sync.SyncError):
                    sync.crossref_search({}, lambda _: encoded({"status": "ok", "message": next(pages)}))

    def test_malformed_source_json_is_rejected(self):
        for value in (b"not json", b"[]", encoded({"status": "error", "message": {}})):
            with self.subTest(value=value), self.assertRaises(sync.SyncError):
                sync.crossref_search({}, lambda _: value)

    def test_zero_and_nonzero_citations_update_without_changing_curated_content(self):
        original = catalogue()
        for count in (0, 12):
            with self.subTest(count=count):
                payload = encoded({"status": "ok", "message": {"DOI": "10.1234/example", "is-referenced-by-count": count}})
                updated, summary = sync.refresh_citations(original, fetch=lambda _: payload)
                self.assertEqual(updated[0]["citation_count"], count)
                self.assertEqual(updated[0]["citation_source"], "Crossref")
                self.assertEqual(summary["citation_total"], count)
                for key, value in original[0].items():
                    self.assertEqual(updated[0][key], value)
                repeated, summary = sync.refresh_citations(updated, fetch=lambda _: payload)
                self.assertEqual(repeated, updated)
                self.assertEqual(summary["citation_counts_updated"], 0)
        self.assertNotIn("citation_count", original[0])

    def test_missing_citation_record_is_unknown_not_zero(self):
        original = catalogue()
        original[0].update(citation_count=7, citation_source="Crossref")

        def missing(_):
            raise sync.SourceNotFound("Not registered")

        updated, summary = sync.refresh_citations(original, fetch=missing)
        self.assertNotIn("citation_count", updated[0])
        self.assertNotIn("citation_source", updated[0])
        self.assertEqual(summary["citation_records"], 0)
        self.assertEqual(original[0]["citation_count"], 7)

    def test_absent_count_field_is_unknown_and_invalid_count_or_doi_aborts(self):
        updated, _ = sync.refresh_citations(catalogue(), fetch=lambda _: encoded({"status": "ok", "message": {"DOI": "10.1234/example"}}))
        self.assertNotIn("citation_count", updated[0])
        for metadata in (
            {"DOI": "10.1234/wrong", "is-referenced-by-count": 8},
            {"DOI": "10.1234/example", "is-referenced-by-count": -1},
            {"DOI": "10.1234/example", "is-referenced-by-count": True},
            {"DOI": "10.1234/example", "is-referenced-by-count": "8"},
        ):
            with self.subTest(metadata=metadata), self.assertRaises(sync.SyncError):
                sync.refresh_citations(catalogue(), fetch=lambda _: encoded({"status": "ok", "message": metadata}))

    def test_linked_article_requires_verified_authorship(self):
        item = crossref_preprint(DOI="10.1234/article", type="journal-article", author=[{"given": "Other", "family": "Scientist"}], **{"container-title": ["Journal"]})
        with self.assertRaises(sync.SyncError):
            sync.fetch_crossref_article("10.1234/article", CONFIG, fetch=lambda _: encoded({"status": "ok", "message": item}))

    def test_preprint_and_citation_source_failures_leave_all_files_untouched(self):
        for failing_function in ("fetch_preprint_records", "refresh_citations"):
            with self.subTest(source=failing_function), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "publications.json"
                candidate = Path(directory) / "candidate.json"
                checkpoint = Path(directory) / "checkpoint.json"
                path.write_text(json.dumps(catalogue()))
                candidate.write_text("previous candidate")
                checkpoint.write_text("{}")
                before = {p: p.read_bytes() for p in (path, candidate, checkpoint)}
                with patch.object(sync, "fetch_records", return_value=[record()]), \
                        patch.object(sync, "fetch_preprint_records", return_value=[]) as preprints, \
                        patch.object(sync, "refresh_citations", side_effect=lambda values, **kwargs: (values, {})) as citations:
                    (preprints if failing_function == "fetch_preprint_records" else citations).side_effect = sync.SyncError("Source unavailable")
                    self.assertEqual(sync.main(["--input", str(path), "--output", str(candidate), "--checkpoint", str(checkpoint)]), 1)
                for target, content in before.items():
                    self.assertEqual(target.read_bytes(), content)

    def test_changed_source_configuration_refreshes_checkpoint_without_catalogue_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            now = datetime(2026, 11, 21, tzinfo=timezone.utc)
            original, _ = sync.checkpoint_update(path, catalogue(), CONFIG, now)
            sync.atomic_write(path, original)
            config = copy.deepcopy(CONFIG)
            config["preprint_servers"] = ["biorxiv"]
            updated, changed = sync.checkpoint_update(path, catalogue(), config, now + timedelta(days=1))
            self.assertTrue(changed)
            self.assertNotEqual(updated["configuration_sha256"], original["configuration_sha256"])
            self.assertEqual(updated["catalogue_sha256"], original["catalogue_sha256"])


if __name__ == "__main__":
    unittest.main()
