# Step 4: Scraper

🌐 **English** · [Dansk](Step-4-Scraper-da) · [Bahasa Melayu](Step-4-Scraper-ms)

Milestone `MIL-004`. Branch and pull request: one for this step.

![Scraper tests with 99 % coverage](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/04-scraper-tests.png)

## What was done

The infrastructure layer: a polite web client that reads `robots.txt` first, refuses disallowed paths, sends an honest User-Agent, waits between requests and retries a failed request a limited number of times; a parser for ranking pages and one for food pages, both built on `html.parser`; and unit tests that use small HTML fixtures and a fake transport, so no test touches the network.

## What was gained

- `urllib.robotparser` answers "may I fetch this?" in one call, and checking it before every request is cheap politeness.
- `html.parser` is event based: the parser keeps a small state (inside a table row, inside the first cell) instead of searching a tree, which is why the fixtures matter.
- Injecting the transport and the clock makes the delay and the retries testable in milliseconds.
