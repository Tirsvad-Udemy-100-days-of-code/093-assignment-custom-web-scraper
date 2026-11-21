# Scraper: fetch and parse the pages

## Metadata

| Key | Value |
| --- | --- |
| ID | MIL-004 |
| CrossReference | [BC-001], [SA-001], [PP-001] |
| Language | en |
| Domain | it |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | pending |
| 2026-11-21 | Accepted | S01 | S01 | Accepted by S01 in chat on 2026-11-21; review RC-007 Go, stand-in, not independent | pending |

---

## Purpose

Build and test the polite fetching and the HTML parsing on their own, so the core of the assignment is proven before the CSV is written.

## Target Date

2026-11-25

## Deliverable

A polite HTTP client that obeys `robots.txt`, parsers for ranking pages and food pages, and unit tests with HTML fixtures

## Business Case Objectives

OBJ-2, OBJ-3, OBJ-5

## Owner and Reviewer

Owner: S01. Approving reviewer: S01.

## Dependencies

MIL-003

## Go/No-Go Criteria

- All unit tests pass without network access; line coverage of the module at least 90 %
- A request to a path that `robots.txt` disallows is refused before it is sent
- The delay between two requests is at least 2 s
- opengrep reports 0 findings; code review against `qc-programming-python.md` is `Go`

## Branch and Pull Request

One branch `milestone/mil-004-scraper` and one pull request that closes the issues of the tasks below.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Fetch pages politely | Infrastructure `PoliteWebClient`: honest User-Agent, `robots.txt` check with `urllib.robotparser`, delay between requests, timeout and a limited retry | Yes | UC-001 |
| 2 | Parse a ranking page | Infrastructure `parse_ranking_page`: the food names and links of a ranking page with `html.parser` | Yes | UC-001 |
| 3 | Parse a food page | Infrastructure `parse_food_page`: name, category, calories and the nutrients per 100 g as a domain `Food` | Yes | UC-001 |
| 4 | Unit tests for the scraper | Tests with small HTML fixtures and a fake transport: robots rules, delay, parsing, missing values | Yes | UC-001 |
| 5 | Screenshot and wiki step page | Screenshot of this step in `docs/images/`, added to the README step list and to a wiki step page in en, da and ms that explains what was learned | No | CN-007 |

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
