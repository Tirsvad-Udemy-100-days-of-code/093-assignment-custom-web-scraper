# Wellness CSV: filter foods and save

## Metadata

| Key | Value |
| --- | --- |
| ID | MIL-005 |
| CrossReference | [BC-001], [SA-001], [PP-001] |
| Language | en |
| Domain | it |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | pending |
| 2026-11-21 | Accepted | S01 | S01 | Accepted by S01 in chat on 2026-11-21; review RC-008 Go, stand-in, not independent | pending |

---

## Purpose

Add the wellness rules, the scrape use case, the CSV writer and the command line, so one command produces the CSV the assignment asks for.

## Target Date

2026-11-26

## Deliverable

`python -m nutrition_scraper` writes `data/wellness_foods.csv`, with unit and integration tests

## Business Case Objectives

OBJ-1, OBJ-3

## Owner and Reviewer

Owner: S01. Approving reviewer: S01.

## Dependencies

MIL-004

## Go/No-Go Criteria

- Tests pass for the wellness tags, the sodium limit, the scrape use case and the CSV writer
- A run against the live site writes a CSV with a header row and at least 20 food rows
- The CSV is not tracked by git
- opengrep reports 0 findings; code review against `qc-programming-python.md` is `Go`

## Branch and Pull Request

One branch `milestone/mil-005-wellness-csv` and one pull request that closes the issues of the tasks below.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Wellness rules | Domain `classify_wellness` returns the tags high protein, high fibre and low calorie; `is_wellness_friendly` also applies the sodium limit | Yes | UC-001 |
| 2 | Scrape use case | Application `scrape_foods`: ranking pages to food pages to kept foods, behind a `FoodSource` port | Yes | UC-001 |
| 3 | Save to CSV | Infrastructure `save_to_csv`: one row per food, one column per nutrient, UTF-8 | Yes | UC-001 |
| 4 | Command line | Presentation `main`: `--output`, `--limit` and `--delay` options and a log of the run | Yes | UC-001 |
| 5 | Tests for the use case and the CLI | Fake `FoodSource`, CSV round trip with `tmp_path`, CLI with a fake client | Yes | UC-001 |
| 6 | Screenshot and wiki step page | Screenshot of this step in `docs/images/`, added to the README step list and to a wiki step page in en, da and ms that explains what was learned | No | CN-007 |

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
