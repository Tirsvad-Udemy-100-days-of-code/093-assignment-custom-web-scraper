# Reflection Journal

Day 93 assignment: Custom Web Scraper. The wiki carries this journal in English, Danish and Bahasa Melayu.

## How I approached the project

I chose a site and a question before writing code: nutritionvalue.org and "which foods help wellness and fitness?". Then I read the rules of the site first, `robots.txt` and the terms, because they decide what a scraper may do. After that I planned six milestones, each with its own branch and pull request, designed the use case, built the fetching and parsing with tests, and only then added the rules and the CSV.

## What was easy

- Reading `robots.txt`: `urllib.robotparser` answers "may I fetch this?" in one call.
- Writing the CSV: `csv.DictWriter` with one fixed column list.
- Testing the rules: thresholds are plain numbers, so the tests need no HTML and no network.

## What was hard

- Reading the HTML with `html.parser`, which only gives events. A table inside a nutrient table closed my state too early, and fat and saturated fat came out empty until a real page showed it. The hand-written fixtures had not contained a nested table.
- Deciding what "wellness friendly" means. The thresholds are a simple study rule, not advice, and writing them as an ADR made that clear.
- Staying polite. With a 2 s delay a full run of 80 pages takes about 3 minutes, so testing against the live site had to be rare and the tests use fakes.

## What I would do differently next time

- Save one real page as a fixture sooner, with the site's permission in mind, or write the fixture from a page's structure after the first live look.
- Add a progress line with the time left, so a long polite run does not look stuck.
- Cache pages for a day, so a second run does not ask the site for the same pages again.

## Biggest learning

A scraper is a guest on someone else's site. The code that fetches is small; most of the work is the rules around it: what is allowed, how often, how to say who you are and what to do when a page is missing. The live run read 80 food pages, kept 63 foods and skipped 0 pages.
