# Step 5: Wellness CSV

🌐 **English** · [Dansk](Step-5-Wellness-CSV-da) · [Bahasa Melayu](Step-5-Wellness-CSV-ms)

Milestone `MIL-005`. Branch and pull request: one for this step.

![A run of the scraper that writes the CSV](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/05-wellness-csv-run.png)

## What was done

The rules that tag a food as high protein, high fibre or low calorie (and drop it when the sodium is high), the `scrape_foods` use case that goes from ranking pages to food pages to kept foods, the `save_to_csv` writer and the command line `python -m nutrition_scraper`. A live run against the site wrote the CSV on the local computer; the CSV itself is not committed.

## What was gained

- The `csv` module quotes commas and quotes for you; one `DictWriter` and a fixed column list make the file predictable.
- Separating the rules (domain) from the fetching (infrastructure) meant the wellness thresholds are tested with plain numbers, no HTML.
- A real run showed what fixtures cannot: some pages have no value for a nutrient, so every optional value is stored as empty instead of zero.
