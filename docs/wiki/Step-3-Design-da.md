# Trin 3: Design

🌐 [English](Step-3-Design) · **Dansk** · [Bahasa Melayu](Step-3-Design-ms)

Milepæl `MIL-003`. Gren og pull request: én for dette trin.

![Use case UC-001](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/raw/branch/main/docs/images/03-design-use-case.png)

## Hvad der blev gjort

Én use case, UC-001 "Skrab velfærdsfødevarer til en CSV", med alternative forløb (en side, som stedet forbyder, en side uden værdier, en mislykket forespørgsel). To ADR'er beskriver standardbibliotek-klienten og grænseværdierne. Domænemodel, systemsekvensdiagram, operationskontrakt, sekvensdiagram og designklassediagram viser, hvordan lagene hænger sammen.

## Hvad vi fik ud af det

- De alternative forløb fandt de svære tilfælde før koden: hvad gør man, når `robots.txt` siger nej, eller en side ikke har en næringstabel?
- En port (`FoodSource`) mellem use case og webklient gør, at use casen kan testes med en falsk kilde og uden netværk.
- At nedskrive grænseværdierne som en beslutning (ADR) gør det tydeligt, at "velfærdsvenlig" er en enkel studieregel og ikke kostrådgivning.
