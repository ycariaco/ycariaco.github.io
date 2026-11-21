#!/usr/bin/env python3
"""Add verified publications from PubMed without deleting curated entries.

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
from urllib.parse import urlencode, unquote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
USER_AGENT = "CariacoLabPublicationSync/1.0 (+https://cariacolab.com/)"
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/[^\s<>\"']+$", re.IGNORECASE)
ORCID_PATTERN = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")


class SyncError(Exception):
    """An unsafe or incomplete update; leave the published data untouched."""


class PlainTextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain_text(value):
    parser = PlainTextParser()
    parser.feed(str(value or ""))
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
    if types.intersection(t.casefold() for t in config["exclude_types"]):
        return None
    if not types.intersection(t.casefold() for t in config["include_types"]):
        return None
    if record.get("source") == "PPR":
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
    return {
        "id": "publication_" + hashlib.sha256(stable_key.encode()).hexdigest()[:16],
        "title": title,
        "authors": authors,
        "year": int(year),
        "journal": journal,
        "doi": doi,
        "pmid": pmid,
        "tags": [],
    }


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
            if attempt == 2:
                raise SyncError(f"PubMed is unavailable; existing publications preserved: {exc}") from exc
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


def merge_publications(existing, records, config):
    validate_publications(existing)
    output = copy.deepcopy(existing)
    added = 0
    corrected_pmids = 0
    matched = 0
    for record in sorted(records, key=lambda p: (str(p.get("doi", "")).lower(), str(p.get("id", "")))):
        candidate = record_to_publication(record, config)
        if not candidate:
            continue
        matched += 1
        candidate_doi = normalized_doi(candidate["doi"])
        same_doi = next((p for p in output if candidate_doi and normalized_doi(p.get("doi")) == candidate_doi), None)
        if same_doi:
            # Preserve curated wording, display IDs and tags. Only correct a
            # PMID when the authoritative record has exactly the same DOI.
            if candidate["pmid"] and candidate["pmid"] != str(same_doi.get("pmid") or ""):
                same_doi["pmid"] = candidate["pmid"]
                corrected_pmids += 1
            continue
        same_pmid = next((p for p in output if candidate["pmid"] and str(p.get("pmid") or "") == candidate["pmid"]), None)
        if same_pmid and (not normalized_doi(same_pmid.get("doi")) or not candidate_doi):
            if candidate_doi and not same_pmid.get("doi"):
                same_pmid["doi"] = candidate_doi
            continue
        same_title = next((p for p in output if normalized_name(p["title"]) == normalized_name(candidate["title"])), None)
        if same_title:
            # A title match is enough to avoid a duplicate, but not enough to
            # replace conflicting identifiers without manual investigation.
            continue
        output.append(candidate)
        added += 1
    if not matched:
        raise SyncError("No verified published papers matched the configured author; existing catalogue preserved.")
    validate_publications(output)
    return output, {"added": added, "corrected_pmids": corrected_pmids, "verified_records": matched, "total": len(output)}


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
    try:
        recorded = datetime.fromisoformat(previous.get("last_recorded_success", "").replace("Z", "+00:00"))
        if recorded.tzinfo is None:
            recorded = recorded.replace(tzinfo=timezone.utc)
        due = now - recorded >= timedelta(days=28)
    except (ValueError, TypeError, AttributeError):
        due = True
    if not due and previous.get("catalogue_sha256") == catalogue_hash and previous.get("author_orcid") == config["orcid"]:
        return previous, False
    return {
        "source": "PubMed (NCBI E-utilities)",
        "source_url": "https://pubmed.ncbi.nlm.nih.gov/",
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
        updated, summary = merge_publications(existing, records, config)
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
