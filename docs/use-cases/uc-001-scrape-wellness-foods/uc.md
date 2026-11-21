# Use Case UC-001: Scrape wellness foods to a CSV

## Metadata

| Key | Value |
| --- | --- |
| ID | UC-001 |
| CrossReference | [SA-001], [BC-001], [MIL-003], [DM-001], [SSD-001] |
| Language | en |
| Domain | it |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | pending |
| 2026-11-21 | Accepted | S01 | S01 | Accepted after review RC-010 Go; stand-in review, not independent | pending |

---

## Purpose

Describe the one user goal of the project: a student starts the scraper and gets
a CSV of wellness and fitness friendly foods with their values per 100 g.
Answers CN-001, CN-003, CN-004 and CN-008 for S01, S02 and S04.

## Use Case

| Field | Value |
| --- | --- |
| Name | Scrape wellness foods to a CSV |
| Format | Fully Dressed |
| Scope | Nutrition Wellness Scraper (the command-line program) |
| Level | User goal |
| Primary actor | Student (S01 or an S02 course participant who runs the scraper) |

## Stakeholders and Interests

| Stakeholder | Interest |
| --- | --- |
| S01 Course participant | The assignment works end to end and practises scraping (CN-001, CN-002) |
| S02 Udemy course participants | The CSV is useful for wellness and fitness: protein, fibre, calories and sodium per 100 g (CN-004) |
| S03 GitHub viewers | The program shows the idea clearly with no runtime dependencies (CN-005) |
| S04 nutritionvalue.org | Its rules are followed and its servers are not loaded (CN-008) |

## Preconditions

- The computer can reach nutritionvalue.org.
- The student has a folder where the CSV may be written.

## Postconditions

- Success: a CSV exists with one header row and one row per kept food; each row
  has the name, category, tags, the values per 100 g and the address of the
  page. The student has been told how many foods were kept and how many pages
  were skipped.
- Failure: the student is told why nothing was written; no half-written CSV is
  left behind.

## Main Success Scenario

1. The student starts the scraper and, if they want, chooses the output file, how many foods to take from each ranking and the wait between requests.
2. The system reads the rules of the site and keeps them for the run (BR-1).
3. For each ranking page (for example protein in poultry, fibre in vegetables, lowest calories in fruits) the system reads the top foods (BR-2).
4. For each food the system reads its page with the values per 100 g, waiting between requests (BR-3, BR-6).
5. The system tags the food as high protein, high fibre or low calorie (BR-4) and keeps it when it has a tag and is not high in sodium (BR-5).
6. The system writes the kept foods to the CSV, one row per food, each food once (BR-7), and tells the student how many foods it kept and how many pages it skipped.

## Alternative Flows

- 2a. The rules of the site cannot be read because the site answers with a server error: the system stops and says so; nothing is written.
- 3a. A ranking page is not allowed by the rules or cannot be read after the repeats (BR-3): the system skips that ranking, notes it and continues with the next one.
- 4a. A food page is not allowed, cannot be read after the repeats, or has no values: the system skips that food, notes it and continues.
- 5a. No food is kept: the system writes the CSV with the header row only and says that no food matched.
- 6a. The folder of the output file does not exist: the system creates it.

No step includes or extends another use case; UC-001 is the only use case.

## Business Rules

| ID | Step | Rule |
| --- | --- | --- |
| BR-1 | 2, 3, 4 | A page is requested only when `robots.txt` allows it for this scraper (BC-001 Constraints) |
| BR-2 | 3 | The top 10 foods of a ranking are read unless the student chooses another number (BC-001 AS-2) |
| BR-3 | 4 | There are at least 2 seconds between two requests; a failed request is repeated twice at most (BC-001 AS-5) |
| BR-4 | 5 | High protein is 20 g or more per 100 g, high fibre 6 g or more, low calorie 60 kcal or less (BC-001 AS-4, ADR-0002) |
| BR-5 | 5 | A food with more than 400 mg sodium per 100 g is left out (BC-001 AS-4) |
| BR-6 | 4 | All values are per 100 g (BC-001 AS-3); a value the page does not give is left empty, not zero |
| BR-7 | 6 | A food that appears in several rankings is written once |

---

[SA-001]: ../../stakeholder-analysis.md
[BC-001]: ../../business-case.md
[MIL-003]: ../../milestones/mil-003-design.md
[DM-001]: dm.md
[SSD-001]: ssd.md
