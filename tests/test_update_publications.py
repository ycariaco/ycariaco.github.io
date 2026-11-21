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
            with patch.object(sync, "fetch_records", return_value=[record()]):
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
            with patch.object(sync, "fetch_records", return_value=[record()]):
                self.assertEqual(sync.main([
                    "--input", str(path), "--output", str(candidate_path), "--checkpoint", str(checkpoint_path), "--dry-run"
                ]), 0)
            self.assertEqual(path.read_text(), content)
            self.assertFalse(candidate_path.exists())
            self.assertFalse(checkpoint_path.exists())


if __name__ == "__main__":
    unittest.main()
