# ADR-0001: Standard library HTTP client and HTML parser

## Metadata

| Key | Value |
| --- | --- |
| ID | ADR-0001 |
| CrossReference | [BC-001], [UC-001], [DCD-001] |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | [2f482f5] |
| 2026-11-21 | Accepted | S01 | S01 | Accepted after review RC-011 Go; stand-in review, not independent | [2f482f5] |

---

## Context

UC-001 needs to fetch pages politely and read values out of HTML. The course
taught `requests` and BeautifulSoup, but S03 (CN-005) and BC-001 AS-1 ask for
no runtime dependency, and the scraper only needs a handful of tags.

Forces: dependency count, how familiar the code is to S02 (CN-003), robustness
against changes of the site's HTML (R-1), the effort of the parser, and the
need to test without the network.

Options evaluated:

1. `urllib.request`, `urllib.robotparser` and `html.parser` from the standard library, behind a small transport interface.
2. `requests` with BeautifulSoup.
3. A scraping framework such as Scrapy.

## Decision

The scraper uses the standard library: `urllib.request` for HTTP,
`urllib.robotparser` for `robots.txt` and `html.parser.HTMLParser` for the HTML.
The HTTP call is hidden behind a `Transport` interface so tests can replace it.

## Consequences

Positive:

- No runtime dependency (Flexibility, CN-005).
- The politeness rules (delay, robots, retries) are written in the open and are tested with a fake transport (Reliability, CN-008).
- `html.parser` is event based and teaches how HTML is read.

Negative:

- More parser code than with BeautifulSoup selectors (Maintainability).
- S02 participants who know `requests` see a different style (Interaction Capability).
- A change of the site's HTML needs a change of the parser state machine (R-1).

## Affected Artifacts

- [UC-001]
- [DCD-001]

---

[BC-001]: ../business-case.md
[UC-001]: ../use-cases/uc-001-scrape-wellness-foods/uc.md
[DCD-001]: ../use-cases/uc-001-scrape-wellness-foods/dcd.md
[2f482f5]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/commit/2f482f5390248b63768bfea82809517c324907cf
