# Changelog

## Unreleased

## 1.0.0 (2026-11-21)

First release: a polite command-line scraper that collects wellness and fitness friendly foods from nutritionvalue.org into a CSV file.

### Added

- Scraper built on the standard library: `PoliteWebClient` with `robots.txt`, delay and retries, plus the ranking and food page parsers.
- Wellness rules (`high-protein`, `high-fibre`, `low-calorie`, sodium limit) and the `scrape_foods` use case.
- CSV writer and the `nutrition-scraper` command line with `--output`, `--limit` and `--delay`.
- Project documents, use case UC-001, two ADRs, tests with 99 % coverage and a Doxygen configuration.
- Wiki in English, Danish and Bahasa Melayu with a screenshot per step, and the reflection journal.
