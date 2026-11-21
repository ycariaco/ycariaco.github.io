# Automatic publication updates

The publications list and topic graph use `assets/json/publications.json`. The website checks PubMed daily at approximately **10:37 UTC** for published journal articles and reviews authored by Yusmaris Cariaco. The existing page design and manually curated entries remain in place.

## Which papers are added

The author identity and accepted name variants are configured in `_data/publication_sources.json`. A record must contain either Yusmaris's ORCID, `0000-0003-3473-3555`, or an exact configured full name. Initials alone do not qualify, and a conflicting ORCID prevents a name match.

The updater excludes preprints, corrections, and retracted publications. It matches DOI, PMID, and normalized title to avoid duplicates. Existing titles, author lists, tags, years, and graph identifiers are preserved. A matching DOI can fill or correct an existing PubMed link using PubMed's own record. Papers missing from a later search are never deleted.

PubMed does not cover every journal, and indexing can lag behind publication. An eligible paper appears after it has been indexed, passes the author checks, and the next successful website update runs. Publications outside PubMed can still be added manually to the catalogue. Source access uses [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25499/) without a new account or API key.

## How updates are published

The `Deploy site` workflow in `.github/workflows/deploy.yml` runs the updater on its daily schedule or when manually run on the default branch. Ordinary website pushes and pull requests run the offline tests and catalogue validation without contacting PubMed.

The scheduled process:

1. Tests the updater and validates the current catalogue.
2. Fetches and validates source records, then prepares a candidate catalogue.
3. Builds the complete website with that candidate.
4. Checks that nobody changed the source branch during the build.
5. Commits only the publication catalogue and its successful-check record, if changed, and deploys the built site in the same run.

An API, validation, or build failure stops the update and leaves the live site in place. Source changes during the build prevent an outdated publication commit or deployment. The source push is never forced.

The workflow uses GitHub's existing repository token. It deploys in the same run because [commits made with that token do not start another push workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## Scheduled checks and inactivity

`assets/json/publications-sync.json` records the source, author ORCID, publication count, catalogue hash, and `last_recorded_success`. This record is refreshed when the catalogue changes or at least every 28 days after a successful source check. It is committed only after the website builds successfully. The timestamp is the last **recorded** successful check; individual daily runs remain in the workflow logs.

This periodic record provides useful evidence that the source is still reachable even when no papers have appeared. It is not a guarantee that GitHub will keep the schedule running. GitHub schedules can be delayed, and public repositories can have scheduled workflows disabled after 60 days without repository activity. If updates stop, inspect the latest `Deploy site` run and, if necessary, [re-enable the workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows). A manual run on the default branch checks for papers immediately.

## Maintaining the catalogue

- Edit existing publication wording or tags directly in `assets/json/publications.json`; the updater preserves those fields.
- Adjust verified name variants or excluded DOI/PMID values in `_data/publication_sources.json`. Exclusions prevent future imports; they do not remove existing entries.
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
