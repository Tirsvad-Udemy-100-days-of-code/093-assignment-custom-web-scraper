# Trin 5: Velfærds-CSV

🌐 [English](Step-5-Wellness-CSV) · **Dansk** · [Bahasa Melayu](Step-5-Wellness-CSV-ms)

Milepæl `MIL-005`. Gren og pull request: én for dette trin.

![En kørsel af skraberen, der skriver CSV-filen](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/05-wellness-csv-run.png)

## Hvad der blev gjort

Reglerne, der mærker en fødevare som proteinrig, fiberrig eller kalorielav (og fjerner den ved højt natriumindhold), use casen `scrape_foods`, der går fra rangeringssider til fødevaresider til beholdte fødevarer, skriveren `save_to_csv` og kommandolinjen `python -m nutrition_scraper`. En live kørsel mod stedet skrev CSV-filen på den lokale computer; selve CSV-filen committes ikke.

## Hvad vi fik ud af det

- `csv`-modulet sætter citationstegn om kommaer og anførselstegn for dig; én `DictWriter` og en fast kolonneliste gør filen forudsigelig.
- At adskille reglerne (domæne) fra hentningen (infrastruktur) betød, at grænseværdierne testes med rene tal, uden HTML.
- En rigtig kørsel viste, hvad fixtures ikke kan: nogle sider mangler en værdi for et næringsstof, så hver valgfri værdi gemmes som tom i stedet for nul.
