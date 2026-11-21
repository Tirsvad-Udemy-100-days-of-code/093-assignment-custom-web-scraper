# Business Case: Nutrition Wellness Scraper

## Metadata

| Key | Value |
| --- | --- |
| ID | BC-001 |
| CrossReference | [SA-001], [PP-001] |
| Language | en |
| Domain | it |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | [06512d9] |
| 2026-11-21 | Accepted | S01 | S01 | Accepted by S01 in chat on 2026-11-21; review RC-001 Go, stand-in, not independent | [06512d9] |

---

## Summary

Build a small command-line web scraper that collects nutrition facts for foods
that support wellness and fitness (high protein, high fibre, low calorie, low
sodium) from <https://www.nutritionvalue.org/> and writes them to a CSV file.
The project is the Day 93 assignment ("Custom Web Scraper") of "100 Days of
Code: The Complete Python Pro Bootcamp" and is published in the organisation
`Tirsvad-Udemy-100-days-of-code` as `093-assignment-custom-web-scraper`.

**Recommendation: Go.** The cost is the course time budget of 120 minutes plus
documentation, there is no money at stake, and the result is a reusable,
documented example for the course community (S02, S03).

## Problem and Opportunity

Someone who trains and eats for wellness wants a short list of foods with their
nutrients side by side. The site publishes ranking pages and one page per food,
but not a table that can be filtered and kept offline. The assignment asks for
a scraper that builds such a table as a CSV file.

## Objectives

| ID | Objective | Stakeholder concerns |
| --- | --- | --- |
| OBJ-1 | Deliver a working scraper: ranking pages in, a CSV of wellness-friendly foods out | CN-001, CN-004 |
| OBJ-2 | Practise web scraping with HTML parsing and a polite client | CN-002 |
| OBJ-3 | Publish readable, runnable, tested code with clear run instructions and no runtime dependencies | CN-003, CN-005 |
| OBJ-4 | Document each step: README, a wiki in English, Danish and Bahasa Malaysia, a screenshot per step and a reflection journal | CN-003, CN-005, CN-007 |
| OBJ-5 | Keep personal tokens out of the repository and respect the site's rules | CN-006, CN-008 |

Stakeholders and concerns are defined in [SA-001].

## Scope

### In Scope

- Read `robots.txt` and fetch only what it allows, with a delay between requests.
- Fetch ranking pages (for example foods by protein, by fibre, lowest calories)
  and, for each listed food, its page with the values per 100 g.
- Parse the nutrition values with the Python standard library.
- Keep a food when it is wellness-friendly (tags such as high protein, high
  fibre, low calorie) and not high in sodium.
- Write the kept foods to a CSV file with one row per food and a column per
  nutrient.
- Unit tests with pytest, using small HTML fixtures written for the tests.
- Project files: `pyproject.toml`, `constants.py`, `.gitignore`, `.editorconfig`,
  `Doxyfile`, doxygen comments, `README.md` from the framework template.
- Wiki in en, da and ms, one screenshot per milestone, reflection journal.
- Repository description and topics on the git host.

### Out of Scope

- Scraping pages that `robots.txt` disallows, user accounts or the food diary.
- Storing or publishing the scraped data in the repository (the site's terms
  forbid republishing it); the CSV is created on the user's own computer.
- Medical or dietary advice; the tags are simple thresholds for study.
- A database, a web interface, charts.

## Cost-Benefit

The benefit is qualitative: a completed course step, a portfolio repository
and practice of scraping. The cost is time only.

| Item | Estimate |
| --- | --- |
| Course time budget for the build | 120 minutes |
| Planning and review documents | 60 minutes |
| Wiki in three languages, screenshots, reflection | 90 minutes |
| Money | 0 (free, open-source tools) |

## Success Criteria

| ID | Criterion | Target |
| --- | --- | --- |
| SC-1 | A run writes a CSV | One header row and at least 20 food rows, every row with a name, a category and the per-100 g values |
| SC-2 | Politeness | At least 2 s between requests, `robots.txt` read first, an honest User-Agent, no request to a disallowed path |
| SC-3 | Tests | 100 % of pytest tests pass; line coverage of `src/` at least 90 %; no test touches the network |
| SC-4 | Security scan | opengrep reports 0 findings before every push |
| SC-5 | Runtime dependencies | None; everything else is a dev dependency |
| SC-6 | Documentation | Every wiki page exists in en, da and ms; one screenshot per milestone in README and wiki; reflection journal present |
| SC-7 | Delivery | One pull request per milestone, each closing its issues |

## Assumptions

Each `Decided by default` entry is a choice made where the assignment is
silent; it stays open to challenge by S01.

| ID | Assumption | Decided by default | Rejected alternative |
| --- | --- | --- | --- |
| AS-1 | The scraper uses `urllib` and `html.parser` from the standard library, so the project has no runtime dependency | Yes | requests and BeautifulSoup (familiar from the course, but two dependencies) |
| AS-2 | The ranking pages of the site, limited to a food category, are the source of candidates; a food page gives the full values | Yes | Crawl every page of the site |
| AS-3 | Values are taken per 100 g (`?size=100 g`), so foods are comparable | Yes | The default portion of each page |
| AS-4 | Thresholds per 100 g: high protein at least 20 g, high fibre at least 6 g, low calorie at most 60 kcal, sodium at most 400 mg | Yes | No filter |
| AS-5 | The delay between requests is 2 s, double the 1 s `Crawl-delay` of the site | Yes | Only the 1 s of the site |
| AS-6 | "Python greater than 3.14" means `requires-python = ">=3.14"` | Yes | `>=3.15` |
| AS-7 | The scraped CSV is written to `data/` and is not committed | Yes | Commit the CSV |

## Constraints

- Python 3.14 or later in a local `.venv`; pytest for tests.
- Folder structure `src/`, `tests/`, `docs/`; constants in `constants.py`.
- Doxygen comments in the source and a `Doxyfile`.
- Tokens come from `.env`, which is never committed, imported or tested.
- opengrep runs on the Product Owner's computer before each push.
- One branch and one pull request per milestone.
- The site's `robots.txt` and terms of use apply: automated access only as
  `robots.txt` allows, no republishing and no use of the data to train a model.
- The wording rules of S01 apply to every artifact.

## Risks

| ID | Risk | Impact | Mitigation |
| --- | --- | --- | --- |
| R-1 | The site changes its HTML | The parser returns nothing | Parser tests on fixtures, a clear error when a page has no values |
| R-2 | The site blocks or slows the scraper | Run fails | Delay, honest User-Agent, stop after repeated errors, small page limit |
| R-3 | Scraped data is republished by mistake | Breach of the site terms | `data/` and `*.csv` in `.gitignore`, test fixtures written by hand |
| R-4 | A token is committed | Account misuse | `.env` in `.gitignore`, opengrep and the pre-commit hook before push |
| R-5 | Documentation in three languages overruns the time budget | Late delivery | Short pages; English first, translations follow page by page |

## Methodology

ISO/IEC 25010:2023 quality characteristics in the QC checklists, Larman-style
use case and design artifacts, and the plan-first gate of the framework
(`framework/process/plan-first-gate.md`).

---

[SA-001]: ./stakeholder-analysis.md
[PP-001]: ./project-plan.md
[06512d9]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/commit/06512d9089fccc9f33f90b9cdce559fe9d1d7411
