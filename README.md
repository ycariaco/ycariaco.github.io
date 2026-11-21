# Cariaco Lab website

Source for the [Cariaco Lab website](https://cariacolab.com/) at the Université du Québec à Montréal (UQAM).
The site presents the lab’s research, projects, team, publications, funding, news, and contact information.

## Where to edit content

| Content                   | Source                                                           |
| ------------------------- | ---------------------------------------------------------------- |
| Welcome page              | `_pages/welcome.md`                                              |
| Research overview         | `_pages/research.md`                                             |
| Research topic pages      | `_pages/research/`                                               |
| Projects diagram          | `_pages/projects.md`, `_data/research_streams.yml`               |
| Team overview             | `_pages/team.md`                                                 |
| Individual profiles       | `_pages/people/` — lowercase names such as `yusmaris-cariaco.md` |
| Publications page         | `_pages/publications.md`                                         |
| Publication records       | `assets/json/publications.json`                                  |
| Funding                   | `_pages/funding.md`, `_data/funders.yml`                         |
| News                      | `_pages/news.md`                                                 |
| Contact                   | `_pages/contact.md`                                              |
| Data Explorer launch page | `_pages/tools.md`                                                |

Each page’s `permalink` setting controls its public address. Keep that setting unchanged when renaming or moving a source file.
Research topic pages retain their `/research/.../` addresses, and profile pages retain their `/people/.../` addresses.
The Tools page remains available at `/tools/` without appearing in the main navigation.

## Automatic publication updates

The site’s publication list is maintained in `assets/json/publications.json`.
An automated PubMed check adds verified matching publications while preserving curated records.

- Author matching and search settings: `_data/publication_sources.json`.
- Update script: `bin/update_publications.py`.
- Scheduling and publication: `.github/workflows/deploy.yml`.
- Maintenance instructions, manual updates, and troubleshooting: [Publication updates](docs/publications.md).

`_bibliography/papers.bib` is retained as an empty theme compatibility file; it does not supply the current publication list.
The previous template Google Scholar citation updater has been removed.

## Files and folders

- `_pages/` contains the public pages; `_data/` contains their shared content and settings.
- `assets/img/` contains lab artwork, portraits, research illustrations, and funding logos.
- `_includes/`, `_layouts/`, `_sass/`, `_scripts/`, and `assets/css/` / `assets/js/` provide the site’s appearance and behavior.
- `_config.yml` contains the site title, custom domain, navigation options, and other Jekyll settings.
- `.github/workflows/` contains the publishing and checking workflows.
- `docs/` contains maintenance notes and preserved historical content. It is excluded from the public website build.

The unused theme demonstration posts, projects, courses, books, and sample media have been removed.
The live Projects and News pages are maintained directly in `_pages/`.
Lab images and original artwork are retained, including files that may be useful for future updates.

## Development and publishing

The website uses [Jekyll](https://jekyllrb.com/) and the [al-folio theme](https://github.com/alshedivat/al-folio).
Jekyll turns the page files and shared templates into the published website.

Use the Docker development instructions in [INSTALL.md](INSTALL.md) and the checks in [AGENTS.md](AGENTS.md) before publishing changes.
The [deployment workflow](.github/workflows/deploy.yml) builds the site and publishes it through GitHub Pages.
The domain is recorded in `CNAME` and `_config.yml`.

Keep public page addresses, image references, and the navigation order intact when reorganizing source files.
Do not commit generated site output, installed dependencies, or credentials.

## Theme reference guides

The following guides are retained from al-folio. They describe the underlying theme, including optional features and demonstration files that are not enabled in this lab site.
Use the content map and publication guide above for this repository’s current organization.

- [Installation and local setup](INSTALL.md)
- [Theme customization](CUSTOMIZE.md)
- [Quick start](QUICKSTART.md)
- [Troubleshooting](TROUBLESHOOTING.md) and [frequently asked questions](FAQ.md)
- [Analytics](ANALYTICS.md) and [search engine settings](SEO.md)
- [Upstream contribution guide](CONTRIBUTING.md)

## License and acknowledgements

This site is adapted from [al-folio](https://github.com/alshedivat/al-folio) by Maruan Alshedivat and its contributors.
The theme is distributed under the [MIT License](LICENSE); its original copyright and permission notice are preserved.

al-folio was originally based on the [\*folio theme](https://github.com/bogoli/-folio) by [Lia Bogoev](https://liabogoev.com), also published under the MIT License.
