# Trin 4: Skraber

🌐 [English](Step-4-Scraper) · **Dansk** · [Bahasa Melayu](Step-4-Scraper-ms)

Milepæl `MIL-004`. Gren og pull request: én for dette trin.

![Skraber-tests med 99 % dækning](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/04-scraper-tests.png)

## Hvad der blev gjort

Infrastrukturlaget: en høflig webklient, der læser `robots.txt` først, afviser forbudte stier, sender en ærlig User-Agent, venter mellem forespørgsler og gentager en mislykket forespørgsel et begrænset antal gange; en parser til rangeringssider og en til fødevaresider, begge bygget på `html.parser`; og enhedstests med små HTML-fixtures og en falsk transport, så ingen test rører netværket.

## Hvad vi fik ud af det

- `urllib.robotparser` svarer på "må jeg hente dette?" i ét kald, og at tjekke det før hver forespørgsel er billig høflighed.
- `html.parser` er hændelsesbaseret: parseren holder en lille tilstand (inde i en tabelrække, i første celle) i stedet for at søge i et træ, og derfor er fixtures vigtige.
- At injicere transport og ur gør forsinkelsen og genforsøgene testbare på millisekunder.
