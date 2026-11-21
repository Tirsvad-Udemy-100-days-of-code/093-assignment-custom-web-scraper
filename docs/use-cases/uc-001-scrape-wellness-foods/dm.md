# Domain Model: UC-001 Scrape wellness foods to a CSV

## Metadata

| Key | Value |
| --- | --- |
| ID | DM-001 |
| CrossReference | [UC-001], [SSD-001], [DM-002] |
| Language | en |
| Domain | it |

## Version History

| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-21 | Proposed | S01 | S01 | First edition | pending |
| 2026-11-21 | Accepted | S01 | S01 | Accepted after review RC-013 Go; stand-in review, not independent | pending |

---

## Purpose

The concepts of UC-001 in the student's words, so the design and the code name
things the way S02 participants read them (CN-003, CN-004).

## Diagram

```plantuml
@startuml
hide circle
hide methods
skinparam classBackgroundColor #CDEFD3

class "Site Rule" as SiteRule {
  allowed : yes or no
  wait between requests : seconds
}
class Ranking {
  category : text
  sorted by : nutrient
}
class Food {
  name : text
  category : text
  page address : text
}
class "Nutrition Facts" as NutritionFacts {
  calories : kcal
  protein : g
  carbohydrate : g
  fibre : g
  sugars : g
  fat : g
  saturated fat : g
  sodium : mg
  potassium : mg
  calcium : mg
  iron : mg
  vitamin C : mg
}
class "Wellness Tag" as WellnessTag {
  name : high protein, high fibre, low calorie
  threshold : number
}
class "Wellness List" as WellnessList {
  number of foods : whole number
}

SiteRule "1" --> "0..*" Ranking : allows or refuses >
SiteRule "1" --> "0..*" Food : allows or refuses >
Ranking "1" o-- "1..*" Food : lists >
Food "1" *-- "1" NutritionFacts : has per 100 g >
Food "0..*" --> "0..3" WellnessTag : earns >
WellnessList "1" *-- "0..*" Food : keeps >
@enduml
```

## Concepts

| Concept | Meaning | Source |
| --- | --- | --- |
| Site Rule | What the site allows the scraper to read and how long to wait between requests | UC-001 step 2, BR-1, BR-3 |
| Ranking | A page that lists foods of one category sorted by one nutrient, best first | UC-001 step 3, BR-2 |
| Food | One food with its name, category and the address of its page | UC-001 step 4 |
| Nutrition Facts | The values of one food per 100 g; a value the page does not give is empty | UC-001 step 4, BR-6 |
| Wellness Tag | High protein, high fibre or low calorie, earned when a value passes its threshold | UC-001 step 5, BR-4 |
| Wellness List | The foods that were kept, each once, written to the CSV | UC-001 steps 5 and 6, BR-5, BR-7 |

---

[UC-001]: uc.md
[SSD-001]: ssd.md
[DM-002]: ../../domain-model.md
