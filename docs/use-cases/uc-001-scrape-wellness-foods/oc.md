# Operation Contract: scrapeFoods

## Metadata

| Key | Value |
| --- | --- |
| ID | OC-001 |
| CrossReference | [SSD-001], [DM-001], [SD-001] |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | [d5d3287] |
| 2026-11-21 | Accepted | S01 | S01 | Accepted after review RC-015 Go; stand-in review, not independent | [d5d3287] |

---

## Operation

`scrapeFoods(outputFile: text = "data/wellness_foods.csv", foodsPerRanking: whole number >= 1 = 10, delay: seconds >= 2 = 2.0) : Wellness List`

Traces to the `scrapeFoods` message of [SSD-001].

## Cross References

UC-001 steps 1 to 6; Domain Model [DM-001]: Site Rule, Ranking, Food,
Nutrition Facts, Wellness Tag, Wellness List.

## Preconditions

- The Site Rule of the site has been read and is `allowed` for the pages that are requested.
- `delay` is at least the wait that the Site Rule asks for.

## Postconditions

- A Wellness List `w` was created.
- For each Ranking that the Site Rule allows and that could be read, up to
  `foodsPerRanking` Foods were read; for each Food `f` that could be read, a
  Nutrition Facts instance was created and associated with `f`.
- For each Food whose Nutrition Facts pass a threshold, a Wellness Tag was
  associated with `f`.
- Each Food with at least one Wellness Tag and sodium of at most 400 mg was
  associated with `w`, once, even when it appeared in several Rankings.
- `w.number of foods` was set to the number of Foods in `w`.
- The Wellness List was written to `outputFile`, one row per Food.
- Between two requests at least `delay` seconds passed.

## Exceptions

| Exception | Triggering condition |
| --- | --- |
| Site rules unreadable | The site answers the request for its rules with a server error (UC-001 2a) |
| Page skipped | A Ranking or Food is refused by the Site Rule, cannot be read after two repeats, or has no values (UC-001 3a, 4a); the run continues |

A `delay` below 2 seconds is raised to 2 seconds; it is not an error.

---

[SSD-001]: ssd.md
[DM-001]: dm.md
[SD-001]: sd.md
[d5d3287]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/commit/d5d328712110d0af9ce8e36a84913faaf3e35d0b
