#!/usr/bin/env python3
"""Add verified articles and preprints without deleting curated entries.

Only public bibliographic metadata is requested. No API key or third-party
Python package is required. See docs/publications.md for maintenance details.
"""

import argparse
import copy
from datetime import datetime, timedelta, timezone
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import unicodedata
import xml.etree.ElementTree as ET
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, unquote, quote, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CROSSREF_URL = "https://api.crossref.org/works"
PREPRINT_URL = "https://api.biorxiv.org/details/"
USER_AGENT = "CariacoLabPublicationSync/2.0 (+https://cariacolab.com/)"
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/[^\s<>\"']+$", re.IGNORECASE)
ORCID_PATTERN = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")


class SyncError(Exception):
    """An unsafe or incomplete update; leave the published data untouched."""


class SourceNotFound(SyncError):
    """A source explicitly reports that an identifier is not registered."""


class PlainTextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain_text(value):
    # Crossref titles can put line breaks around superscripts, e.g. NAD <sup>+</sup>.
    # Keep the scientific notation attached while retaining spaces between words.
    value = re.sub(r"\s*(<(?:\w+:)?(?:sup|sub)\b[^>]*>)\s*", r"\1", str(value or ""), flags=re.I)
    value = re.sub(r"\s*(</(?:\w+:)?(?:sup|sub)>)", r"\1", value, flags=re.I)
    value = re.sub(r"(</(?:\w+:)?(?:sup|sub)>)\s+(?=[-−])", r"\1", value, flags=re.I)
    parser = PlainTextParser()
    parser.feed(value)
    parser.close()
    return " ".join(html.unescape("".join(parser.parts)).split())


def normalized_name(value):
    value = unicodedata.normalize("NFKD", str(value or "")).casefold()
    value = "".join(c for c in value if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^\w]+", " ", value).split())


def normalized_doi(value):
    value = unquote(str(value or "").strip())
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value, flags=re.I)
    return value.lower() if DOI_PATTERN.fullmatch(value) else ""


def normalized_orcid(value):
    value = str(value or "").strip().removeprefix("https://orcid.org/").removeprefix("http://orcid.org/")
    return value.upper()


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SyncError(f"Cannot read JSON from {path}: {exc}") from exc


def validate_config(config):
    if not isinstance(config, dict) or not ORCID_PATTERN.fullmatch(str(config.get("orcid", ""))):
        raise SyncError("Publication source configuration needs a valid ORCID.")
    names = config.get("author_names")
    if not isinstance(names, list) or not names:
        raise SyncError("At least one exact author name is required.")
    for name in names:
        if not isinstance(name, dict) or not name.get("first") or not name.get("last"):
            raise SyncError("Each author alias needs first and last names.")
        if any('"' in str(name[key]) for key in ("first", "last")):
            raise SyncError("Author aliases cannot contain query quotation marks.")
    for key in ("include_types", "exclude_types", "exclude_dois", "exclude_pmids"):
        if not isinstance(config.get(key), list) or any(not isinstance(v, str) for v in config[key]):
            raise SyncError(f"{key} must be a list of strings.")
    if not config["include_types"] or any('"' in value for value in config["include_types"]):
        raise SyncError("Included publication types must be non-empty and cannot contain query quotation marks.")
    servers = config.get("preprint_servers")
    if not isinstance(servers, list) or not servers or any(server not in ("biorxiv", "medrxiv") for server in servers) or len(set(servers)) != len(servers):
        raise SyncError("Preprint servers must be a non-empty list of biorxiv and/or medrxiv.")
    separate = config.get("keep_preprints_separate", [])
    if not isinstance(separate, list) or any(not normalized_doi(doi) for doi in separate):
        raise SyncError("Preprints kept separately must have valid DOIs.")


def validate_publications(publications):
    if not isinstance(publications, list) or not publications:
        raise SyncError("The publication catalogue must be a non-empty list.")
    ids = set()
    dois = set()
    for publication in publications:
        if not isinstance(publication, dict):
            raise SyncError("Each publication must be an object.")
        identifier = publication.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in ids:
            raise SyncError("Publication IDs must be non-empty and unique.")
        ids.add(identifier)
        if not isinstance(publication.get("title"), str) or not publication["title"].strip():
            raise SyncError(f"Publication {identifier} has no title.")
        if not isinstance(publication.get("year"), int) or not 1800 <= publication["year"] <= 2200:
            raise SyncError(f"Publication {identifier} has no valid publication year.")
        authors = publication.get("authors")
        if not isinstance(authors, list) or not authors or any(not isinstance(a, str) or not a.strip() for a in authors):
            raise SyncError(f"Publication {identifier} has no valid author list.")
        doi = normalized_doi(publication.get("doi"))
        if publication.get("doi") and not doi:
            raise SyncError(f"Publication {identifier} has an invalid DOI.")
        if doi in dois:
            raise SyncError(f"Duplicate DOI in the catalogue: {doi}")
        if doi:
            dois.add(doi)
        pmid = str(publication.get("pmid") or "")
        if pmid and not re.fullmatch(r"\d+", pmid):
            raise SyncError(f"Publication {identifier} has an invalid PMID.")
        if publication.get("kind", "article") not in ("article", "preprint"):
            raise SyncError(f"Publication {identifier} has an invalid kind.")
        if publication.get("kind") == "preprint" and (not doi or pmid):
            raise SyncError(f"Preprint {identifier} must have a DOI and no PMID.")
        preprint_dois = publication.get("preprint_dois", [])
        if not isinstance(preprint_dois, list) or any(not normalized_doi(value) for value in preprint_dois):
            raise SyncError(f"Publication {identifier} has invalid preprint DOI links.")
        normalized_preprints = [normalized_doi(value) for value in preprint_dois]
        if len(set(normalized_preprints)) != len(normalized_preprints) or doi in normalized_preprints:
            raise SyncError(f"Publication {identifier} has duplicate preprint DOI links.")
        if "citation_count" in publication:
            count = publication["citation_count"]
            if type(count) is not int or count < 0 or publication.get("citation_source") != "Crossref":
                raise SyncError(f"Publication {identifier} has invalid Crossref citation metadata.")
        elif "citation_source" in publication:
            raise SyncError(f"Publication {identifier} has a citation source without a count.")
        versions = publication.get("preprint_versions", [])
        if not isinstance(versions, list) or any(
            not isinstance(version, dict) or not isinstance(version.get("id"), str)
            or not version["id"] or version.get("kind") != "preprint" or not normalized_doi(version.get("doi"))
            for version in versions
        ):
            raise SyncError(f"Publication {identifier} has invalid archived preprint versions.")


def author_orcids(author):
    values = author.get("authorIdList", {}).get("authorId", [])
    if isinstance(values, dict):
        values = [values]
    direct = author.get("authorId")
    if isinstance(direct, dict):
        values = values + [direct]
    elif isinstance(direct, list):
        values = values + direct
    return {
        normalized_orcid(value.get("value"))
        for value in values
        if isinstance(value, dict) and str(value.get("type", "")).upper() == "ORCID"
    }


def matches_author(record, config):
    target_orcid = normalized_orcid(config["orcid"])
    aliases = {(normalized_name(n["first"]), normalized_name(n["last"])) for n in config["author_names"]}
    for author in record.get("authorList", {}).get("author", []):
        orcids = author_orcids(author)
        if target_orcid in orcids:
            return True
        # A different ORCID is positive evidence of a different person.
        if orcids:
            continue
        first = normalized_name(author.get("firstName"))
        last = normalized_name(author.get("lastName"))
        if (first, last) in aliases:
            return True
        full = normalized_name(author.get("fullName"))
        if any(full in (f"{first} {last}", f"{last} {first}") for first, last in aliases):
            return True
    return False


def record_to_publication(record, config):
    if not matches_author(record, config):
        return None
    types = {str(t).casefold() for t in record.get("pubTypeList", {}).get("pubType", [])}
    preprint = record.get("source") == "PPR" and record.get("verified_preprint_server") in config["preprint_servers"]
    if "preprint" in types and not preprint:
        return None
    excluded_types = {t.casefold() for t in config["exclude_types"]}
    if types.intersection(excluded_types):
        return None
    if not preprint and not types.intersection(t.casefold() for t in config["include_types"]):
        return None
    if record.get("source") == "PPR" and not preprint:
        return None
    doi = normalized_doi(record.get("doi"))
    pmid = str(record.get("pmid") or (record.get("id") if record.get("source") == "MED" else "") or "")
    if doi and doi in {normalized_doi(v) for v in config["exclude_dois"]}:
        return None
    if pmid and pmid in config["exclude_pmids"]:
        return None
    if pmid and not re.fullmatch(r"\d+", pmid):
        raise SyncError("PubMed returned an invalid identifier.")
    title = plain_text(record.get("title"))
    journal = plain_text(record.get("journalInfo", {}).get("journal", {}).get("title"))
    year = str(record.get("pubYear") or "")
    if not title or not year.isdigit() or not journal or not (doi or pmid):
        raise SyncError("A verified paper has incomplete bibliographic metadata; update aborted.")
    authors = []
    for author in record.get("authorList", {}).get("author", []):
        name = " ".join(filter(None, (author.get("firstName"), author.get("lastName"))))
        name = plain_text(name or author.get("fullName") or author.get("collectiveName"))
        if name:
            authors.append(name)
    stable_key = doi or f"pmid:{pmid}"
    publication = {
        "id": "publication_" + hashlib.sha256(stable_key.encode()).hexdigest()[:16],
        "title": title,
        "authors": authors,
        "year": int(year),
        "journal": journal,
        "doi": doi,
        "pmid": pmid,
        "tags": [],
        "kind": "preprint" if preprint else "article",
    }
    if record.get("preprint_dois"):
        publication["preprint_dois"] = sorted({normalized_doi(value) for value in record["preprint_dois"]})
    return publication


def query_for(config):
    clauses = [f'"{config["orcid"]}"[Author Identifier]']
    clauses += [f'"{name["last"]} {name["first"]}"[Full Author Name]' for name in config["author_names"]]
    # Limit source records to journal publications before fetching, so a book
    # chapter by the same author cannot block the journal-only XML parser.
    publication_types = [f'"{value}"[Publication Type]' for value in config["include_types"]]
    return f'({" OR ".join(clauses)}) AND ({" OR ".join(publication_types)})'


def request_bytes(url):
    for attempt in range(3):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=45) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError) as exc:
            if isinstance(exc, HTTPError) and exc.code == 404:
                raise SourceNotFound(f"Publication source did not find this identifier: {url}") from exc
            if attempt == 2:
                raise SyncError(f"A publication source is unavailable; existing publications preserved: {exc}") from exc
            time.sleep(2 ** attempt)


def element_text(parent, path):
    element = parent.find(path)
    return "" if element is None else "".join(element.itertext()).strip()


def parse_pubmed_xml(content):
    try:
        root = ET.fromstring(content)
    except ET.ParseError as exc:
        raise SyncError("PubMed returned malformed XML; catalogue preserved.") from exc
    if root.tag != "PubmedArticleSet":
        raise SyncError("PubMed returned an unexpected document.")
    records = []
    for item in root.findall("PubmedArticle"):
        article = item.find("./MedlineCitation/Article")
        if article is None:
            raise SyncError("PubMed returned a record without article metadata.")
        pmid = element_text(item, "./MedlineCitation/PMID")
        doi = element_text(item, './PubmedData/ArticleIdList/ArticleId[@IdType="doi"]')
        doi = doi or element_text(article, './ELocationID[@EIdType="doi"]')
        year = element_text(article, "./Journal/JournalIssue/PubDate/Year")
        if not year:
            date = element_text(article, "./Journal/JournalIssue/PubDate/MedlineDate")
            match = re.search(r"\b(18|19|20|21)\d{2}\b", date)
            year = match.group(0) if match else element_text(article, "./ArticleDate/Year")
        authors = []
        for author in article.findall("./AuthorList/Author"):
            authors.append({
                "firstName": element_text(author, "ForeName") or element_text(author, "Initials"),
                "lastName": element_text(author, "LastName"),
                "collectiveName": element_text(author, "CollectiveName"),
                "authorId": [
                    {"type": identifier.attrib.get("Source"), "value": identifier.text}
                    for identifier in author.findall("Identifier")
                ],
            })
        records.append({
            "id": pmid, "source": "MED", "pmid": pmid, "doi": doi,
            "title": element_text(article, "ArticleTitle"), "pubYear": year,
            "journalInfo": {"journal": {"title": element_text(article, "./Journal/Title")}},
            "authorList": {"author": authors},
            "pubTypeList": {"pubType": [
                element_text(publication_type, ".") for publication_type in article.findall("./PublicationTypeList/PublicationType")
            ]},
        })
    return records


def fetch_records(config, fetch=request_bytes):
    # This author-sized daily query stays well below NCBI's no-key rate limit.
    search_url = API_URL + "esearch.fcgi?" + urlencode({
        "db": "pubmed", "term": query_for(config), "retmode": "json", "retmax": 10000,
        "tool": "CariacoLabPublicationSync",
    })
    try:
        payload = json.loads(fetch(search_url))
        result = payload["esearchresult"]
        count = int(result["count"])
        identifiers = result["idlist"]
    except (ValueError, KeyError, TypeError) as exc:
        raise SyncError("PubMed search returned invalid metadata.") from exc
    if not isinstance(identifiers, list) or any(not isinstance(value, str) or not value.isdigit() for value in identifiers):
        raise SyncError("PubMed search returned invalid identifiers.")
    if not count:
        raise SyncError("PubMed returned no author matches; existing catalogue preserved.")
    if count != len(identifiers) or len(set(identifiers)) != count:
        raise SyncError("PubMed search results are incomplete; existing catalogue preserved.")
    records = []
    for start in range(0, len(identifiers), 100):
        batch = identifiers[start:start + 100]
        time.sleep(0.4)
        fetch_url = API_URL + "efetch.fcgi?" + urlencode({
            "db": "pubmed", "id": ",".join(batch), "retmode": "xml", "tool": "CariacoLabPublicationSync",
        })
        page = parse_pubmed_xml(fetch(fetch_url))
        if len(page) != len(batch) or {r["pmid"] for r in page} != set(batch):
            raise SyncError("PubMed returned incomplete article metadata; catalogue preserved.")
        records.extend(page)
    return records


def source_json(url, source, fetch):
    try:
        payload = json.loads(fetch(url))
    except (ValueError, TypeError) as exc:
        raise SyncError(f"{source} returned invalid JSON; catalogue preserved.") from exc
    if not isinstance(payload, dict):
        raise SyncError(f"{source} returned an unexpected document.")
    return payload


def crossref_search(parameters, fetch=request_bytes):
    """Read every result; never treat a truncated author query as a full check."""
    cursor = "*"
    records = []
    seen_dois = set()
    expected_count = None
    while True:
        url = CROSSREF_URL + "?" + urlencode({**parameters, "rows": 100, "cursor": cursor})
        payload = source_json(url, "Crossref", fetch)
        message = payload.get("message")
        if payload.get("status") != "ok" or not isinstance(message, dict):
            raise SyncError("Crossref search failed; catalogue preserved.")
        count = message.get("total-results")
        items = message.get("items")
        if type(count) is not int or not 0 <= count <= 10000 or not isinstance(items, list):
            raise SyncError("Crossref search returned an invalid or unexpectedly large result set.")
        if expected_count is None:
            expected_count = count
        if count != expected_count:
            raise SyncError("Crossref results changed during pagination; try again later.")
        for item in items:
            doi = normalized_doi(item.get("DOI")) if isinstance(item, dict) else ""
            if not doi or doi in seen_dois:
                raise SyncError("Crossref returned invalid or repeated search results.")
            seen_dois.add(doi)
            records.append(item)
        if len(records) == expected_count:
            return records
        if not items or len(records) > expected_count:
            raise SyncError("Crossref returned incomplete search results.")
        next_cursor = message.get("next-cursor")
        if not isinstance(next_cursor, str) or not next_cursor:
            raise SyncError("Crossref pagination ended before all results were received.")
        cursor = next_cursor
        time.sleep(0.4)


def crossref_record(item):
    """Normalize publisher metadata into the same author structure as PubMed."""
    authors = item.get("author", [])
    if not isinstance(authors, list) or any(not isinstance(author, dict) for author in authors):
        raise SyncError("Crossref returned invalid author metadata.")
    normalized_authors = []
    for author in authors:
        normalized_authors.append({
            "firstName": author.get("given", ""),
            "lastName": author.get("family", ""),
            "fullName": author.get("name", ""),
            "authorId": [{"type": "ORCID", "value": author["ORCID"]}] if author.get("ORCID") else [],
        })
    titles = item.get("title")
    journals = item.get("container-title")
    year = ""
    for date_key in ("published", "published-online", "published-print", "issued"):
        parts = item.get(date_key, {}).get("date-parts", [])
        if parts and isinstance(parts[0], list) and parts[0]:
            year = str(parts[0][0])
            break
    return {
        "id": normalized_doi(item.get("DOI")),
        "source": "CROSSREF",
        "doi": normalized_doi(item.get("DOI")),
        "pmid": "",
        "title": titles[0] if isinstance(titles, list) and titles else "",
        "pubYear": year,
        "journalInfo": {"journal": {"title": journals[0] if isinstance(journals, list) and journals else ""}},
        "authorList": {"author": normalized_authors},
        "pubTypeList": {"pubType": ["Journal Article"] if item.get("type") == "journal-article" else ["Preprint"]},
    }


def preprint_server(item, config):
    if item.get("type") != "posted-content" or item.get("subtype") != "preprint":
        return None
    # Check publisher-deposited server identity, not the DOI prefix (bioRxiv
    # has used more than one prefix). The official server API verifies it next.
    institutions = item.get("institution", [])
    if not isinstance(institutions, list):
        raise SyncError("Crossref returned invalid preprint-server metadata.")
    names = {str(value.get("name", "")).casefold() for value in institutions if isinstance(value, dict)}
    resource_url = item.get("resource", {}).get("primary", {}).get("URL", "")
    hostname = (urlparse(str(resource_url)).hostname or "").lower()
    for server in config["preprint_servers"]:
        if server in names or hostname in (server + ".org", "www." + server + ".org"):
            return server
    return None


def fetch_preprint_detail(doi, server, fetch=request_bytes):
    url = PREPRINT_URL + server + "/" + quote(doi, safe="/")
    payload = source_json(url, server, fetch)
    messages = payload.get("messages")
    versions = payload.get("collection")
    if not isinstance(messages, list) or not messages or any(
        not isinstance(message, dict) or message.get("status") != "ok" for message in messages
    ) or not isinstance(versions, list) or not versions:
        raise SyncError(f"{server} did not verify preprint {doi}.")
    seen_versions = set()
    for version in versions:
        if not isinstance(version, dict) or normalized_doi(version.get("doi")) != doi or str(version.get("server", "")).casefold() != server:
            raise SyncError(f"{server} returned a different preprint or server.")
        number = str(version.get("version", ""))
        if not number.isdigit() or int(number) < 1 or int(number) in seen_versions:
            raise SyncError(f"{server} returned incomplete or repeated preprint versions.")
        seen_versions.add(int(number))
    latest = max(versions, key=lambda value: int(value["version"]))
    if any(term in str(latest.get("type", "")).casefold() for term in ("withdraw", "retract")):
        raise SyncError(f"Preprint {doi} is withdrawn or retracted; manual review is required.")
    try:
        datetime.strptime(latest["date"], "%Y-%m-%d")
    except (KeyError, TypeError, ValueError) as exc:
        raise SyncError(f"{server} returned an invalid preprint date.") from exc
    if not plain_text(latest.get("title")) or "published" not in latest:
        raise SyncError(f"{server} returned incomplete preprint metadata.")
    published_value = str(latest["published"] or "").strip()
    published_doi = "" if published_value.upper() in ("", "NA", "N/A") else normalized_doi(published_value)
    if published_value.upper() not in ("", "NA", "N/A") and not published_doi:
        raise SyncError(f"{server} returned an invalid published-article DOI.")
    if published_doi == doi:
        raise SyncError(f"{server} returned a circular preprint relationship.")
    return latest, published_doi


def fetch_crossref_work(doi, fetch=request_bytes, cache=None, allow_missing=False):
    if cache is not None and doi in cache:
        item = cache[doi]
    else:
        try:
            time.sleep(0.4)
            payload = source_json(CROSSREF_URL + "/" + quote(doi, safe="/"), "Crossref", fetch)
        except SourceNotFound:
            if not allow_missing:
                raise
            if cache is not None:
                cache[doi] = None
            return None
        item = payload.get("message")
        if payload.get("status") != "ok":
            raise SyncError("Crossref did not verify the requested DOI.")
    if item is None and allow_missing:
        return None
    if not isinstance(item, dict) or normalized_doi(item.get("DOI")) != doi:
        raise SyncError("Crossref returned metadata for a different DOI.")
    if cache is not None:
        cache[doi] = item
    return item


def fetch_crossref_article(doi, config, fetch=request_bytes, cache=None):
    item = fetch_crossref_work(doi, fetch, cache)
    if item.get("type") != "journal-article":
        raise SyncError("The linked published version is not a journal article.")
    record = crossref_record(item)
    if record_to_publication(record, config) is None:
        raise SyncError("The linked published article could not be verified for this author.")
    return record


def fetch_preprint_records(config, published_records=(), existing=(), fetch=request_bytes, crossref_cache=None):
    """Discover by name/ORCID, then verify each DOI with its preprint server."""
    items = {}
    searches = [{"filter": "type:posted-content,orcid:" + config["orcid"]}]
    searches += [
        {"filter": "type:posted-content", "query.author": name["first"] + " " + name["last"]}
        for name in config["author_names"]
    ]
    for parameters in searches:
        for item in crossref_search(parameters, fetch):
            if crossref_cache is not None:
                crossref_cache[normalized_doi(item["DOI"])] = item
            server = preprint_server(item, config)
            if server and matches_author(crossref_record(item), config):
                items[normalized_doi(item["DOI"])] = (item, server)
    # Recheck known preprints even if a later author search omits them. That also
    # allows the server's eventual journal-version link to promote an entry.
    known_preprints = set()
    for publication in existing:
        if publication.get("kind") == "preprint":
            known_preprints.add(normalized_doi(publication.get("doi")))
        known_preprints.update(normalized_doi(value) for value in publication.get("preprint_dois", []))
    excluded = {normalized_doi(value) for value in config["exclude_dois"]}
    for doi in sorted(known_preprints - set(items) - excluded):
        if not doi:
            continue
        item = fetch_crossref_work(doi, fetch, crossref_cache)
        server = preprint_server(item, config)
        if not server or not matches_author(crossref_record(item), config):
            raise SyncError("A previously imported preprint no longer has verifiable author metadata.")
        items[doi] = (item, server)
    published_by_doi = {
        normalized_doi(record.get("doi")): record for record in published_records
        if record_to_publication(record, config) is not None and normalized_doi(record.get("doi"))
    }
    separate = {normalized_doi(doi) for doi in config.get("keep_preprints_separate", [])}
    records = []
    for doi, (item, server) in sorted(items.items()):
        if doi in excluded:
            continue
        detail, published_doi = fetch_preprint_detail(doi, server, fetch)
        if published_doi and doi not in separate:
            if published_doi in excluded:
                continue
            article = copy.deepcopy(published_by_doi.get(published_doi))
            if article is None:
                article = fetch_crossref_article(published_doi, config, fetch, crossref_cache)
            article["preprint_dois"] = [doi]
            records.append(article)
            continue
        record = crossref_record(item)
        record.update({
            "source": "PPR", "title": detail["title"], "pubYear": detail["date"][:4],
            "journalInfo": {"journal": {"title": "bioRxiv" if server == "biorxiv" else "medRxiv"}},
            "verified_preprint_server": server,
        })
        records.append(record)
    return records


def refresh_citations(publications, fetch=request_bytes, crossref_cache=None):
    """Crossref counts describe one index; an unknown count is never a zero."""
    output = copy.deepcopy(publications)
    changed = 0
    known = 0
    total = 0
    for publication in output:
        before = (publication.get("citation_count"), publication.get("citation_source"))
        doi = normalized_doi(publication.get("doi"))
        work = fetch_crossref_work(doi, fetch, crossref_cache, allow_missing=True) if doi else None
        count = work.get("is-referenced-by-count") if work is not None else None
        if count is None:
            publication.pop("citation_count", None)
            publication.pop("citation_source", None)
        else:
            if type(count) is not int or count < 0:
                raise SyncError(f"Crossref returned an invalid citation count for {doi}.")
            publication["citation_count"] = count
            publication["citation_source"] = "Crossref"
            known += 1
            total += count
        if before != (publication.get("citation_count"), publication.get("citation_source")):
            changed += 1
    validate_publications(output)
    return output, {"citation_counts_updated": changed, "citation_records": known, "citation_total": total}


def merge_preprint_links(publication, candidate):
    links = {normalized_doi(value) for value in publication.get("preprint_dois", [])}
    links.update(normalized_doi(value) for value in candidate.get("preprint_dois", []))
    if links:
        publication["preprint_dois"] = sorted(links)


def archive_preprint(publication, preprint):
    """Keep the prior ID and all curated preprint metadata when versions join."""
    snapshot = copy.deepcopy(preprint)
    snapshot.pop("preprint_versions", None)
    versions = publication.setdefault("preprint_versions", [])
    if not any(version["id"] == snapshot["id"] and normalized_doi(version["doi"]) == normalized_doi(snapshot["doi"]) for version in versions):
        versions.append(snapshot)


def merge_publications(existing, records, config):
    validate_publications(existing)
    output = copy.deepcopy(existing)
    added = 0
    corrected_pmids = 0
    matched = 0
    promoted = 0
    consolidated = 0
    candidates = [candidate for record in records if (candidate := record_to_publication(record, config)) is not None]
    separate = {normalized_doi(value) for value in config.get("keep_preprints_separate", [])}
    for candidate in candidates:
        if candidate.get("preprint_dois"):
            candidate["preprint_dois"] = [doi for doi in candidate["preprint_dois"] if doi not in separate]
            if not candidate["preprint_dois"]:
                candidate.pop("preprint_dois")
    # Process explicit version relationships first, before the same article's
    # independent PubMed record can be appended beside its existing preprint.
    candidates.sort(key=lambda p: (0 if p.get("preprint_dois") else 1, p["doi"], p["pmid"]))
    for candidate in candidates:
        matched += 1
        candidate_doi = normalized_doi(candidate["doi"])
        related_preprints = {normalized_doi(value) for value in candidate.get("preprint_dois", [])}
        if candidate["kind"] == "preprint" and candidate_doi not in separate and any(
            publication.get("kind", "article") == "article" and candidate_doi in publication.get("preprint_dois", [])
            for publication in output
        ):
            continue
        same_doi = next((p for p in output if candidate_doi and normalized_doi(p.get("doi")) == candidate_doi), None)
        if same_doi:
            # Preserve curated wording, display IDs and tags. Only correct a
            # PMID when the authoritative record has exactly the same DOI.
            if candidate["pmid"] and candidate["pmid"] != str(same_doi.get("pmid") or ""):
                same_doi["pmid"] = candidate["pmid"]
                corrected_pmids += 1
            merge_preprint_links(same_doi, candidate)
            if candidate["kind"] == "article":
                for prior in list(output):
                    if prior.get("kind") == "preprint" and normalized_doi(prior.get("doi")) in related_preprints:
                        archive_preprint(same_doi, prior)
                        output.remove(prior)
                        consolidated += 1
            continue
        prior_preprint = next((p for p in output if p.get("kind") == "preprint" and normalized_doi(p.get("doi")) in related_preprints), None)
        if prior_preprint and candidate["kind"] == "article":
            # Keep stable graph identity, curated wording, authors and tags.
            # Only an official server relationship permits publication status,
            # canonical identifiers and venue/year to change automatically.
            archive_preprint(prior_preprint, prior_preprint)
            for field in ("doi", "pmid", "journal", "year", "kind"):
                prior_preprint[field] = candidate[field]
            merge_preprint_links(prior_preprint, candidate)
            promoted += 1
            continue
        same_pmid = next((p for p in output if candidate["pmid"] and str(p.get("pmid") or "") == candidate["pmid"]), None)
        if same_pmid and (not normalized_doi(same_pmid.get("doi")) or not candidate_doi):
            if candidate_doi and not same_pmid.get("doi"):
                same_pmid["doi"] = candidate_doi
            continue
        same_title = next((p for p in output if normalized_name(p["title"]) == normalized_name(candidate["title"])), None)
        if same_title and same_title.get("kind", "article") == candidate["kind"] and (
            not normalized_doi(same_title.get("doi")) or not candidate_doi
        ):
            # A title can deduplicate records missing identifiers. Distinct
            # DOIs, particularly a preprint and an article, remain distinct
            # unless the source supplies an explicit version relationship.
            continue
        output.append(candidate)
        added += 1
    if not matched:
        raise SyncError("No verified publications matched the configured author; existing catalogue preserved.")
    validate_publications(output)
    return output, {"added": added, "corrected_pmids": corrected_pmids, "promoted_preprints": promoted, "consolidated_preprints": consolidated, "verified_records": matched, "total": len(output)}


def atomic_write(path, publications):
    path = Path(path)
    content = json.dumps(publications, ensure_ascii=False, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temporary = handle.name
            handle.write(content)
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def checkpoint_update(path, publications, config, now=None):
    """Record a real successful source check at least every 28 days.

    The workflow commits this only after the generated site builds successfully.
    Unchanged daily checks remain in the Actions logs instead of making daily
    source commits.
    """
    now = now or datetime.now(timezone.utc)
    previous = read_json(path) if Path(path).exists() else {}
    if not isinstance(previous, dict):
        raise SyncError("Publication sync checkpoint must be an object.")
    catalogue_hash = hashlib.sha256(json.dumps(
        publications, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()
    configuration_hash = hashlib.sha256(json.dumps(config, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    sources = [
        {"name": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/", "purpose": "published articles"},
        {"name": "Crossref", "url": "https://api.crossref.org/", "purpose": "preprint discovery, linked articles and citation counts"},
        {"name": "/".join(config["preprint_servers"]), "url": "https://api.biorxiv.org/", "purpose": "preprint verification and published-version links"},
    ]
    try:
        recorded = datetime.fromisoformat(previous.get("last_recorded_success", "").replace("Z", "+00:00"))
        if recorded.tzinfo is None:
            recorded = recorded.replace(tzinfo=timezone.utc)
        due = now - recorded >= timedelta(days=28)
    except (ValueError, TypeError, AttributeError):
        due = True
    if not due and previous.get("catalogue_sha256") == catalogue_hash and previous.get("author_orcid") == config["orcid"] and previous.get("configuration_sha256") == configuration_hash and previous.get("sources") == sources:
        return previous, False
    return {
        "source": "PubMed, Crossref and verified preprint servers",
        "sources": sources,
        "configuration_sha256": configuration_hash,
        "author_orcid": config["orcid"],
        "last_recorded_success": now.astimezone(timezone.utc).isoformat(timespec="seconds"),
        "publication_count": len(publications),
        "catalogue_sha256": catalogue_hash,
    }, True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "_data/publication_sources.json")
    parser.add_argument("--input", type=Path, default=ROOT / "assets/json/publications.json")
    parser.add_argument("--output", type=Path, help="Write a staged candidate here instead of updating the input file.")
    parser.add_argument("--checkpoint", type=Path, help="Record successful source checks here when data changes or every 28 days.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and validate without writing any files.")
    parser.add_argument("--validate-only", action="store_true", help="Validate the existing catalogue without contacting any API.")
    args = parser.parse_args(argv)
    try:
        config = read_json(args.config)
        validate_config(config)
        existing = read_json(args.input)
        validate_publications(existing)
        if args.validate_only:
            print(f"Validated {len(existing)} publications.")
            return 0
        records = fetch_records(config)
        crossref_cache = {}
        preprints = fetch_preprint_records(config, published_records=records, existing=existing, crossref_cache=crossref_cache)
        records.extend(preprints)
        updated, summary = merge_publications(existing, records, config)
        updated, citation_summary = refresh_citations(updated, crossref_cache=crossref_cache)
        summary.update(citation_summary)
        changed = updated != existing
        summary["changed"] = changed
        checkpoint, checkpoint_changed = checkpoint_update(args.checkpoint, updated, config) if args.checkpoint else ({}, False)
        summary["checkpoint_changed"] = checkpoint_changed
        print(json.dumps(summary, sort_keys=True))
        if not args.dry_run and (changed or args.output):
            atomic_write(args.output or args.input, updated)
        if not args.dry_run and checkpoint_changed:
            atomic_write(args.checkpoint, checkpoint)
        return 0
    except (SyncError, OSError) as exc:
        print(f"Publication update failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
