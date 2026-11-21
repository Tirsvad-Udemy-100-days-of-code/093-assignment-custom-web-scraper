# Sequence Diagram: scrapeFoods

## Metadata

| Key | Value |
| --- | --- |
| ID | SD-001 |
| CrossReference | [OC-001], [DCD-001], [ADR-0001], [ADR-0002] |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | [d5d3287] |
| 2026-11-21 | Accepted | S01 | S01 | Accepted after review RC-016 Go; stand-in review, not independent | [d5d3287] |

---

## Purpose

How the classes realise the postconditions of [OC-001] `scrapeFoods`, grouped by
the clean architecture layers. Answers CN-003 (readable names) and CN-008 (where
the politeness is enforced) for S02 and S04.

## Diagram

```plantuml
@startuml
title SD-001: scrapeFoods
actor Student
box "Presentation" #FADADD
  participant "main" as Main <<Controller>>
end box
box "Application" #FFF3B0
  participant "scrape_foods" as UseCase
end box
box "Infrastructure" #D4E4F7
  participant ":NutritionValueSource" as Source
  participant ":PoliteWebClient" as Client
  participant "parse_ranking_page" as RankParser
  participant "parse_food_page" as FoodParser
  participant "save_to_csv" as Writer
end box
box "Domain" #CDEFD3
  participant "classify_wellness" as Rules
  participant ":Food" as Food
end box

Student -> Main : python -m nutrition_scraper --output --limit --delay
activate Main
Main -> UseCase : scrape_foods(source, rankings, foods_per_ranking)
activate UseCase
loop each ranking page
  UseCase -> Source : read_ranking(path)
  activate Source
  Source -> Client : fetch_page(path)
  activate Client
  note right of Client : robots.txt check, wait >= 2 s,\nrepeat twice at most (ADR-0001)
  alt refused by robots.txt or failed
    Client --> Source : raise SourceError
    Source --> UseCase : raise SourceError
    note over UseCase : skip the ranking and note it (3a)
  end
  Client --> Source : html
  deactivate Client
  Source -> RankParser : parse_ranking_page(html)
  RankParser --> Source : ranked foods
  Source --> UseCase : ranked foods
  deactivate Source
  loop top foods_per_ranking foods, not seen before
    UseCase -> Source : read_food(path)
    activate Source
    Source -> Client : fetch_page(path + per 100 g)
    Client --> Source : html
    Source -> FoodParser : parse_food_page(html, url)
    FoodParser -> Food ** : create(name, category, values)
    alt no values on the page
      FoodParser --> Source : raise SourceError
      note over UseCase : skip the food and note it (4a)
    end
    FoodParser --> Source : food
    Source --> UseCase : food
    deactivate Source
    UseCase -> Rules : classify_wellness(food)
    Rules --> UseCase : tags (ADR-0002)
    opt tags not empty and sodium <= 400 mg
      UseCase -> UseCase : keep food with its tags
    end
  end
end
UseCase --> Main : ScrapeResult(foods, skipped)
deactivate UseCase
Main -> Writer : save_to_csv(foods, output_file)
Writer --> Main : rows written
Main --> Student : "Wrote N foods, skipped M pages"
deactivate Main
@enduml
```

## Notes

- GRASP Controller: `main` receives the system operation and only delegates;
  `scrape_foods` is the use case controller.
- The application layer owns the `FoodSource` protocol; `NutritionValueSource`
  implements it, so the use case is tested with a fake source and no network.
- The politeness (robots, delay, repeats) lives in one place, `PoliteWebClient`,
  and every request goes through it.
- The exceptions of OC-001 are the `alt` fragments; a skipped page is added to
  `ScrapeResult.skipped` and the run continues.

---

[OC-001]: oc.md
[DCD-001]: dcd.md
[ADR-0001]: ../../adr/adr-0001-standard-library-client.md
[ADR-0002]: ../../adr/adr-0002-wellness-thresholds.md
[d5d3287]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/commit/d5d328712110d0af9ce8e36a84913faaf3e35d0b
