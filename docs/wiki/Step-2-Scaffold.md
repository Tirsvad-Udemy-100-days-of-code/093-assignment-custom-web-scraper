# Step 2: Scaffold

🌐 **English** · [Dansk](Step-2-Scaffold-da) · [Bahasa Melayu](Step-2-Scaffold-ms)

Milestone `MIL-002`. Branch and pull request: one for this step.

![Smoke tests passing in the .venv](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/02-scaffold-tests.png)

## What was done

An empty but runnable Python project: `pyproject.toml` (Python 3.14 or newer and no runtime dependencies), the package `src/nutrition_scraper/` with `constants.py`, smoke tests, a `Doxyfile`, a Python `.gitignore` that also ignores scraped data, an `.editorconfig` and the README with setup steps. opengrep ran clean before the push.

## What was gained

- `pyproject.toml` holds metadata, the empty `dependencies` list and the pytest settings in one file; `pip install -e ".[dev]"` installs the test tools.
- The Python standard library is enough for a scraper: `urllib`, `html.parser`, `csv` and `urllib.robotparser`.
- Putting the delay, the User-Agent and the thresholds in `constants.py` makes the politeness of the scraper visible in one place and testable from the first commit.
