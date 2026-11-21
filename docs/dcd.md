# Design Class Diagram: Nutrition Wellness Scraper

## Metadata

| Key | Value |
| --- | --- |
| ID | DCD-002 |
| CrossReference | [DCD-001], [DM-002], [SD-001], [OC-001] |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition: adds the design of DCD-001 (UC-001) | [b428560] |
| 2026-11-21 | Accepted | S01 | S01 | Accepted after review RC-019 Go; stand-in review, not independent | [b428560] |

---

## Purpose

The project Design Class Diagram, the consolidated design of every use case. It
holds the additions of [DCD-001] (UC-001): the classes, functions and packages
that implement [UC-001], one package per clean architecture layer. Answers
CN-003 and CN-005 for S02 and S03.

## Diagram

```plantuml
@startuml
title DCD: Nutrition Wellness Scraper
skinparam packageStyle rectangle
hide empty members

package "presentation (Delivery)" #FADADD {
  class main_module <<module>> {
    + main(argv : list[str] | None) : int
    - build_source(delay : float) : FoodSource
  }
}
package "application" #FFF3B0 {
  interface FoodSource <<Protocol>> {
    + read_ranking(path : str) : list[RankedFood]
    + read_food(path : str) : Food
  }
  class ScrapeResult <<dataclass>> {
    + foods : list[Food]
    + skipped : list[str]
  }
  class scrape_foods_module <<module>> {
    + scrape_foods(source : FoodSource, rankings : tuple, foods_per_ranking : int) : ScrapeResult
  }
  class SourceError <<exception>>
}
package "infrastructure" #D4E4F7 {
  interface Transport <<Protocol>> {
    + get(url : str, headers : dict, timeout : float) : TransportResponse
  }
  class UrllibTransport {
    + get(url : str, headers : dict, timeout : float) : TransportResponse
  }
  class PoliteWebClient {
    - _transport : Transport
    - _robots : RobotFileParser
    - _last_request : float
    + fetch_page(path : str) : str
    - _wait_for_turn() : None
  }
  class NutritionValueSource {
    - _client : PoliteWebClient
    + read_ranking(path : str) : list[RankedFood]
    + read_food(path : str) : Food
  }
  class ranking_parser <<module>> {
    + parse_ranking_page(html : str) : list[RankedFood]
  }
  class food_parser <<module>> {
    + parse_food_page(html : str, url : str) : Food
  }
  class csv_writer <<module>> {
    + save_to_csv(foods : list[Food], path : Path) : int
  }
}
package "domain" #CDEFD3 {
  class Food <<value object>> {
    + name : str
    + category : str
    + calories_kcal : float | None
    + protein_g : float | None
    + fibre_g : float | None
    + sodium_mg : float | None
    + tags : tuple[str, ...]
    + source_url : str
  }
  class RankedFood <<value object>> {
    + name : str
    + path : str
  }
  class wellness <<module>> {
    + classify_wellness(food : Food) : tuple[str, ...]
    + is_wellness_friendly(food : Food) : bool
  }
}

main_module ..> scrape_foods_module
main_module ..> NutritionValueSource : wires
main_module ..> csv_writer
scrape_foods_module "1" --> "1" FoodSource : source
scrape_foods_module ..> wellness
scrape_foods_module ..> ScrapeResult : creates
NutritionValueSource ..|> FoodSource
NutritionValueSource "1" o--> "1" PoliteWebClient : _client
NutritionValueSource ..> ranking_parser
NutritionValueSource ..> food_parser
PoliteWebClient "1" o--> "1" Transport : _transport
UrllibTransport ..|> Transport
food_parser ..> Food : creates
ranking_parser ..> RankedFood : creates
wellness ..> Food
csv_writer ..> Food
"presentation (Delivery)" ..> "application"
"presentation (Delivery)" ..> "infrastructure" : wires in main
"infrastructure" ..> "application" : implements FoodSource
"application" ..> "domain"
@enduml
```

## Mapping to the Domain Model

| Domain concept | Design element |
| --- | --- |
| Site Rule | `RobotFileParser` inside `PoliteWebClient`; `REQUEST_DELAY_SECONDS` |
| Ranking | `RankedFood` entries returned by `parse_ranking_page`; the ranking paths are `RANKING_PAGES` |
| Food | `Food` |
| Nutrition Facts | the numeric fields of `Food`, each `None` when the page gives no value |
| Wellness Tag | the strings in `Food.tags`, set by `classify_wellness` |
| Wellness List | `ScrapeResult.foods`, written by `save_to_csv` |

## Design Notes

- Dependencies point inward: `domain` imports nothing from the other layers;
  `application` owns the `FoodSource` protocol (dependency inversion);
  `infrastructure` implements it; `main` wires the parts (composition root).
- `PoliteWebClient` has one job, a polite fetch; parsing is in separate modules
  (single responsibility).
- Every constant lives in `constants.py` (delay, User-Agent, thresholds, ranking
  pages, CSV columns).
- Exceptions: `SourceError` (application) is raised by the source for a refused,
  failed or empty page; it extends `ValueError`.

---

[DCD-001]: use-cases/uc-001-scrape-wellness-foods/dcd.md
[DM-002]: domain-model.md
[SD-001]: use-cases/uc-001-scrape-wellness-foods/sd.md
[OC-001]: use-cases/uc-001-scrape-wellness-foods/oc.md
[UC-001]: use-cases/uc-001-scrape-wellness-foods/uc.md
[b428560]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/093-assignment-custom-web-scraper/commit/b428560f5990f764f9eedcb41f3ec4d3abbaca99
