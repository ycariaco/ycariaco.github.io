# Automatic publication updates

The publications list and topic graph use `assets/json/publications.json`. The website checks for articles and preprints authored by Yusmaris Cariaco daily at approximately **10:37 UTC**. It refreshes Crossref citation counts in the same run. The existing page design and manually curated entries remain in place.

## Which papers are added

The author identity and accepted name variants are configured in `_data/publication_sources.json`. A record must contain either Yusmaris's ORCID, `0000-0003-3473-3555`, or an exact configured full name. Initials alone do not qualify, and a conflicting ORCID prevents a name match.

The sources have distinct roles:

- **PubMed** supplies published journal articles and reviews and verifies PubMed links.
- **Crossref** discovers preprints by full name and ORCID. Only records classified as preprints from the configured bioRxiv/medRxiv servers qualify; broad name-search results are filtered by the exact author checks above. Every search page must be received before an update can proceed.
- **The official bioRxiv/medRxiv API** verifies each preprint DOI, server, latest version, title, posting date, and any link to a published journal version. Full author names come from the corresponding Crossref record. Preprints are labeled separately from published articles.

Corrections and retracted PubMed publications are excluded. A withdrawn or retracted preprint stops the automatic update for manual review. Existing titles, author lists, tags, and graph identifiers are preserved. An exact DOI match can fill or correct an existing PubMed link using PubMed's own record. Papers missing from a later search are never deleted, and known preprints are rechecked directly by DOI.

The updater uses DOI and PMID to avoid duplicates. Similar titles alone never establish that a preprint and a journal article are the same work. Only an explicit published-DOI link from the official preprint server can join versions, and the linked article must independently pass the author checks. A preprint already in the catalogue can then keep its ID, title, authors and tags while its venue, year and canonical identifiers are promoted to the published article. Its original record is retained in `preprint_versions`, and its DOI remains available through `preprint_dois`. If both versions were already listed before their relationship became available, the published entry keeps its ID and curated fields, and the original preprint record is preserved under it instead of appearing twice.

`keep_preprints_separate` records explicit decisions to continue displaying particular preprints separately. The 2023 NAD preprint is in this list at the author's request, so a future server relationship will not automatically combine it with another entry.

PubMed does not cover every journal, and Crossref or preprint-server indexing can lag. An eligible paper appears after its source metadata is available, passes the author checks, and the next successful website update runs. The preprint import currently covers bioRxiv and medRxiv; other servers and publications outside these sources can be added manually. Journal versions explicitly linked by a preprint server can be verified through Crossref even before PubMed indexes them. General Crossref journal search is not used, because it also returns conference abstracts and other records that need review.

The sources are public and need no new account or API key: [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25499/), [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/), and the [bioRxiv/medRxiv API](https://api.biorxiv.org/).

## Citation counts

`citation_count` and `citation_source: "Crossref"` contain the count returned for each publication's exact canonical DOI. Counts are refreshed daily, including real zero counts. If Crossref does not register the DOI or does not provide a count, the count is left unknown rather than set to zero. A transient API failure, malformed count, or mismatched DOI aborts the update without saving partial results.

Crossref counts citations found in reference lists deposited with Crossref; they can differ from Google Scholar, Scopus, or Web of Science. The displayed total adds the available counts for the listed records, including separately listed preprints. It is not a count of unique citing papers or an author h-index. See [Crossref Cited-by](https://www.crossref.org/services/cited-by/).

## How updates are published

The `Deploy site` workflow in `.github/workflows/deploy.yml` runs the updater on its daily schedule or when manually run on the default branch. Ordinary website pushes and pull requests run the offline tests and catalogue validation without contacting publication APIs.

The scheduled process:

1. Tests the updater and validates the current catalogue.
2. Fetches and validates all article, preprint, and citation records, then prepares a candidate catalogue.
3. Builds the complete website with that candidate.
4. Checks that nobody changed the source branch during the build.
5. Commits only the publication catalogue and its successful-check record, if changed, and deploys the built site in the same run.

An API, validation, or build failure stops the update and leaves the live site in place. Source changes during the build prevent an outdated publication commit or deployment. The source push is never forced.

The workflow uses GitHub's existing repository token. It deploys in the same run because [commits made with that token do not start another push workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## Scheduled checks and inactivity

`assets/json/publications-sync.json` records the sources, configuration hash, author ORCID, publication count, catalogue hash, and `last_recorded_success`. This record is refreshed when the catalogue or source configuration changes or at least every 28 days after a successful source check. It is committed only after the website builds successfully. The timestamp is the last **recorded** successful check; individual daily runs remain in the workflow logs.

This periodic record provides useful evidence that the source is still reachable even when no papers have appeared. It is not a guarantee that GitHub will keep the schedule running. GitHub schedules can be delayed, and public repositories can have scheduled workflows disabled after 60 days without repository activity. If updates stop, inspect the latest `Deploy site` run and, if necessary, [re-enable the workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows). A manual run on the default branch checks for papers immediately.

## Maintaining the catalogue

- Edit existing publication wording or tags directly in `assets/json/publications.json`; the updater preserves those fields.
- Adjust verified name variants or excluded DOI/PMID values in `_data/publication_sources.json`. Exclusions prevent future imports; they do not remove existing entries.
- Use `keep_preprints_separate` for confirmed decisions to show a preprint independently even if the server later links a published version.
- `kind` defaults to `article`; newly imported preprints use `preprint`. Citation fields and version links are maintained by the updater.
- Keep the stable `id` of each existing entry so its graph connections remain intact.
- Do not edit the generated successful-check record by hand.

Run the offline checks with Python 3:

```bash
python3 -m unittest discover -s tests -v
python3 bin/update_publications.py --validate-only
```

Preview an online update without changing any files:

```bash
python3 bin/update_publications.py --dry-run
```

Or save a candidate separately for inspection:

```bash
python3 bin/update_publications.py --output /tmp/cariaco-publications-candidate.json
```
