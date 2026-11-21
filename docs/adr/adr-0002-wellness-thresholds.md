# ADR-0002: Wellness thresholds per 100 g

## Metadata

| Key | Value |
| --- | --- |
| ID | ADR-0002 |
| CrossReference | [BC-001], [UC-001], [DCD-001] |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | [2f482f5] |
| 2026-11-21 | Accepted | S01 | S01 | Accepted after review RC-012 Go; stand-in review, not independent | [2f482f5] |

---

## Context

UC-001 keeps foods that "help wellness and fitness". The assignment does not
say what that means. A rule is needed that is simple, explainable and the same
for every run, so the CSV can be compared between runs and between students.

Forces: simplicity for S02 (CN-003), usefulness of the result (CN-004), honesty
(the rule is not dietary advice) and testability.

Options evaluated:

1. Fixed thresholds per 100 g in `constants.py`: high protein 20 g or more, high fibre 6 g or more, low calorie 60 kcal or less, and a sodium limit of 400 mg.
2. Relative rules, for example the best quarter of the scraped foods for each nutrient.
3. No filter; write every food that was read.

## Decision

Fixed thresholds per 100 g, kept in `constants.py` and applied by the domain
rule `classify_wellness`. A food is kept when it has at least one tag and its
sodium is at most 400 mg. A value that is missing never earns a tag.

## Consequences

Positive:

- The rule is explained in one sentence and tested with plain numbers (Maintainability, Testability).
- Results do not change when more pages are read (Reliability).

Negative:

- The numbers are a simplification and not dietary advice; the README says so (Safety).
- A student with other goals changes the constants (Flexibility).

## Affected Artifacts

- [UC-001]
- [DCD-001]

---

[BC-001]: ../business-case.md
[UC-001]: ../use-cases/uc-001-scrape-wellness-foods/uc.md
[DCD-001]: ../use-cases/uc-001-scrape-wellness-foods/dcd.md
[2f482f5]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/commit/2f482f5390248b63768bfea82809517c324907cf
