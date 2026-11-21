"""!
@file test_scrape_foods.py
@brief Unit tests for the scrape_foods use case, with a fake FoodSource.
"""

import pytest

from fake_food_source import FakeFoodSource
from nutrition_scraper.application.food_source import SiteRulesError, SourceError
from nutrition_scraper.application.scrape_foods import scrape_foods
from nutrition_scraper.constants import TAG_HIGH_PROTEIN, TAG_LOW_CALORIE
from nutrition_scraper.domain.food import Food
from nutrition_scraper.domain.ranked_food import RankedFood

CHICKEN = Food(name="Chicken", protein_g=30, sodium_mg=70, calories_kcal=165)
CUCUMBER = Food(name="Cucumber", calories_kcal=15, sodium_mg=2)
SALTY_FISH = Food(name="Salted fish", protein_g=60, sodium_mg=5000)
WHITE_RICE = Food(name="White rice", protein_g=7, fibre_g=1, calories_kcal=360, sodium_mg=5)


def ranked(*names: str) -> list[RankedFood]:
    return [RankedFood(name=name, path=f"/{name}.html") for name in names]


def make_source() -> FakeFoodSource:
    return FakeFoodSource(
        rankings={
            "/protein.html": ranked("chicken", "salty", "rice"),
            "/calories.html": ranked("cucumber", "chicken"),
        },
        foods={
            "/chicken.html": CHICKEN,
            "/salty.html": SALTY_FISH,
            "/rice.html": WHITE_RICE,
            "/cucumber.html": CUCUMBER,
        },
    )


RANKINGS = (("protein", "/protein.html"), ("calories", "/calories.html"))


def test_scrape_foods_keeps_tagged_foods_with_their_tags() -> None:
    result = scrape_foods(make_source(), RANKINGS, foods_per_ranking=10)

    by_name = {food.name: food for food in result.foods}
    assert by_name["Chicken"].tags == (TAG_HIGH_PROTEIN,)
    assert by_name["Cucumber"].tags == (TAG_LOW_CALORIE,)


def test_scrape_foods_leaves_out_foods_without_a_tag_or_with_too_much_sodium() -> None:
    result = scrape_foods(make_source(), RANKINGS, foods_per_ranking=10)

    assert {food.name for food in result.foods} == {"Chicken", "Cucumber"}


def test_scrape_foods_reads_a_food_that_is_in_two_rankings_once() -> None:
    source = make_source()

    result = scrape_foods(source, RANKINGS, foods_per_ranking=10)

    assert source.read_foods.count("/chicken.html") == 1
    assert [food.name for food in result.foods].count("Chicken") == 1


def test_scrape_foods_takes_only_the_top_of_each_ranking() -> None:
    source = make_source()

    scrape_foods(source, RANKINGS, foods_per_ranking=1)

    assert source.read_foods == ["/chicken.html", "/cucumber.html"]


def test_scrape_foods_counts_the_food_pages_it_read() -> None:
    result = scrape_foods(make_source(), RANKINGS, foods_per_ranking=10)

    assert result.foods_read == 4


def test_scrape_foods_skips_a_ranking_that_fails_and_goes_on() -> None:
    source = make_source()
    source._rankings["/protein.html"] = SourceError("refused")

    result = scrape_foods(source, RANKINGS, foods_per_ranking=10)

    assert [food.name for food in result.foods] == ["Cucumber", "Chicken"]
    assert result.skipped == ["/protein.html: refused"]


def test_scrape_foods_skips_a_food_that_fails_and_goes_on() -> None:
    source = make_source()
    source._foods["/chicken.html"] = SourceError("no values")

    result = scrape_foods(source, RANKINGS, foods_per_ranking=10)

    assert [food.name for food in result.foods] == ["Cucumber"]
    assert result.skipped == ["/chicken.html: no values"]


def test_scrape_foods_stops_when_the_rules_of_the_site_cannot_be_read_for_a_ranking() -> None:
    source = make_source()
    source._rankings["/protein.html"] = SiteRulesError("no rules")

    with pytest.raises(SiteRulesError):
        scrape_foods(source, RANKINGS, foods_per_ranking=10)


def test_scrape_foods_stops_when_the_rules_of_the_site_cannot_be_read_for_a_food() -> None:
    source = make_source()
    source._foods["/chicken.html"] = SiteRulesError("no rules")

    with pytest.raises(SiteRulesError):
        scrape_foods(source, RANKINGS, foods_per_ranking=10)


def test_scrape_foods_returns_an_empty_result_when_nothing_matches() -> None:
    source = FakeFoodSource({"/r.html": ranked("rice")}, {"/rice.html": WHITE_RICE})

    result = scrape_foods(source, (("r", "/r.html"),), foods_per_ranking=5)

    assert result.foods == []
    assert result.skipped == []
