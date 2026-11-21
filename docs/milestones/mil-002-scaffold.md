# Scaffold: Python project skeleton

## Metadata

| Key | Value |
| --- | --- |
| ID | MIL-002 |
| CrossReference | [BC-001], [SA-001], [PP-001] |
| Language | en |
| Domain | it |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | [06512d9] |
| 2026-11-21 | Accepted | S01 | S01 | Accepted by S01 in chat on 2026-11-21; review RC-005 Go, stand-in, not independent | [06512d9] |

---

## Purpose

Give the project a runnable, tested skeleton that follows the course rules, so the feature work starts from a clean base.

## Target Date

2026-11-23

## Deliverable

A repository that installs into a `.venv`, runs a small pytest suite green and passes opengrep

## Business Case Objectives

OBJ-3, OBJ-5

## Owner and Reviewer

Owner: S01. Approving reviewer: S01.

## Dependencies

MIL-001

## Go/No-Go Criteria

- `python -m pip install -e .[dev]` works in a fresh `.venv` on Python 3.14
- `pytest` passes
- opengrep reports 0 findings
- `check-editorconfig.sh` and `check-readme.sh` pass

## Branch and Pull Request

One branch `milestone/mil-002-scaffold` and one pull request that closes the issues of the tasks below.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add pyproject.toml | Project metadata, `requires-python = ">=3.14"`, no runtime dependencies, dev dependencies pytest, pytest-cov and ruff, pytest settings | No | BC-001 AS-1, AS-6 |
| 2 | Add .gitignore and .editorconfig | Python `.gitignore` that also ignores `.env`, `.venv/` and scraped data; `.editorconfig` from the framework baseline | No | BC-001 R-3, R-4 |
| 3 | Add src and tests skeleton with constants.py | Package `src/nutrition_scraper/` with `constants.py` and `__init__.py`, `tests/` with one smoke test | No | BC-001 Constraints |
| 4 | Add Doxyfile | Doxyfile for Python sources under `src/`, output in `docs/doxygen/` (ignored by git) | No | BC-001 Constraints |
| 5 | Write README from the framework template | README with setup of a local `.venv`, `python -m pip install --upgrade pip`, run and test commands, and the step list | No | CN-003, CN-005 |
| 6 | Install git hooks and run opengrep | Install the framework git hooks; run opengrep locally and record a clean result in the pull request | No | CN-006 |
| 7 | Screenshot and wiki step page | Screenshot of this step in `docs/images/`, added to the README step list and to a wiki step page in en, da and ms that explains what was learned; also creates wiki Home, Install and `_Sidebar` in en, da and ms | No | CN-007 |

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
[06512d9]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/commit/06512d9089fccc9f33f90b9cdce559fe9d1d7411
