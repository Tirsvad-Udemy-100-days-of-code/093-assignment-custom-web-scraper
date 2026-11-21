# Trin 2: Skelet

🌐 [English](Step-2-Scaffold) · **Dansk** · [Bahasa Melayu](Step-2-Scaffold-ms)

Milepæl `MIL-002`. Gren og pull request: én for dette trin.

![Smoke-tests består i .venv](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/02-scaffold-tests.png)

## Hvad der blev gjort

Et tomt, men kørbart Python-projekt: `pyproject.toml` (Python 3.14 eller nyere og ingen kørselsafhængigheder), pakken `src/nutrition_scraper/` med `constants.py`, smoke-tests, en `Doxyfile`, en Python-`.gitignore`, der også ignorerer skrabede data, en `.editorconfig` og README med opsætning. opengrep var ren før push.

## Hvad vi fik ud af det

- `pyproject.toml` samler metadata, den tomme `dependencies`-liste og pytest-indstillinger i én fil; `pip install -e ".[dev]"` installerer testværktøjerne.
- Pythons standardbibliotek er nok til en skraber: `urllib`, `html.parser`, `csv` og `urllib.robotparser`.
- Når forsinkelsen, User-Agent og grænseværdierne står i `constants.py`, er skraberens høflighed synlig ét sted og kan testes fra første commit.
