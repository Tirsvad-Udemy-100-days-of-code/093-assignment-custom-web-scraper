# Refleksion

🌐 [English](Reflection) · **Dansk** · [Bahasa Melayu](Reflection-ms)

Dag 93-opgaven: Custom Web Scraper. Wikien har denne journal på engelsk, dansk og bahasa melayu.

## Hvordan jeg greb projektet an

Jeg valgte et websted og et spørgsmål, før jeg skrev kode: nutritionvalue.org og "hvilke fødevarer understøtter velvære og fitness?". Derefter læste jeg stedets regler først, `robots.txt` og vilkårene, fordi de afgør, hvad en skraber må. Så planlagde jeg seks milepæle, hver med egen gren og pull request, designede use casen, byggede hentning og parsing med tests og tilføjede først til sidst reglerne og CSV-filen.

## Hvad der var let

- At læse `robots.txt`: `urllib.robotparser` svarer på "må jeg hente dette?" i ét kald.
- At skrive CSV-filen: `csv.DictWriter` med én fast kolonneliste.
- At teste reglerne: grænseværdierne er rene tal, så testene hverken behøver HTML eller netværk.

## Hvad der var svært

- At læse HTML med `html.parser`, som kun giver hændelser. En tabel inde i en næringstabel lukkede min tilstand for tidligt, og fedt og mættet fedt blev tomme, indtil en rigtig side afslørede det. De håndskrevne fixtures havde ingen indlejret tabel.
- At afgøre, hvad "velfærdsvenlig" betyder. Grænseværdierne er en simpel studieregel og ikke rådgivning, og at skrive dem som en ADR gjorde det tydeligt.
- At være høflig. Med 2 s forsinkelse tager en fuld kørsel på 80 sider cirka 3 minutter, så test mod det rigtige sted måtte være sjælden, og testene bruger falske kilder.

## Hvad jeg ville gøre anderledes næste gang

- Gemme en rigtig side som fixture tidligere, eller skrive fixturen ud fra sidens struktur efter det første live-kig.
- Tilføje en fremdriftslinje med resterende tid, så en lang høflig kørsel ikke ser ud til at hænge.
- Gemme sider i cache et døgn, så en ny kørsel ikke beder stedet om de samme sider igen.

## Den største lærdom

En skraber er gæst på en andens websted. Koden, der henter, er lille; det meste af arbejdet er reglerne omkring den: hvad der er tilladt, hvor ofte, hvordan man siger, hvem man er, og hvad man gør, når en side mangler. Live-kørslen læste 80 fødevaresider, beholdt 63 fødevarer og sprang 0 sider over.
