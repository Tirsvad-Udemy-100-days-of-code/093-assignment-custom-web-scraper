"""!
@file test_food_parser.py
@brief Unit tests for parse_food_page.
"""

import pytest

from fixtures import read_fixture
from nutrition_scraper.application.food_source import SourceError
from nutrition_scraper.infrastructure.food_parser import parse_food_page

URL = "https://example.test/Lentils_one_nutritional_value.html"


def test_parse_food_page_reads_name_category_and_calories() -> None:
    food = parse_food_page(read_fixture("food_page.html"), URL)

    assert food.name == "Lentils, one"
    assert food.category == "Legumes and Legume Products"
    assert food.calories_kcal == pytest.approx(116)
    assert food.source_url == URL


def test_parse_food_page_reads_the_nutrients_in_their_own_units() -> None:
    food = parse_food_page(read_fixture("food_page.html"), URL)

    assert food.carbohydrate_g == pytest.approx(20.13)
    assert food.fibre_g == pytest.approx(7.90)
    assert food.sugars_g == pytest.approx(1.80)
    assert food.fat_g == pytest.approx(0.38)
    assert food.saturated_fat_g == pytest.approx(0.05)
    assert food.potassium_mg == pytest.approx(369)
    assert food.calcium_mg == pytest.approx(19)
    assert food.iron_mg == pytest.approx(3.33)


def test_parse_food_page_converts_other_units() -> None:
    food = parse_food_page(read_fixture("food_page.html"), URL)

    assert food.sodium_mg == pytest.approx(2.0)  # 0.002 g
    assert food.vitamin_c_mg == pytest.approx(1.5)  # 1500 mcg


def test_parse_food_page_accepts_a_decimal_comma_and_keeps_the_first_row() -> None:
    food = parse_food_page(read_fixture("food_page.html"), URL)

    assert food.protein_g == pytest.approx(9.02)


def test_parse_food_page_ignores_tables_that_are_not_nutrient_tables() -> None:
    food = parse_food_page(read_fixture("food_page.html"), URL)

    assert food.sodium_mg != pytest.approx(77)


def test_parse_food_page_leaves_a_missing_value_empty_not_zero() -> None:
    food = parse_food_page(read_fixture("food_page_few_values.html"), URL)

    assert food.sodium_mg == pytest.approx(4)
    assert food.protein_g is None
    assert food.calories_kcal is None
    assert food.category == ""


def test_parse_food_page_rejects_a_page_without_values() -> None:
    with pytest.raises(SourceError, match="no nutrition values"):
        parse_food_page(read_fixture("food_page_empty.html"), URL)


def test_parse_food_page_rejects_a_page_without_a_name() -> None:
    with pytest.raises(SourceError, match="no food name"):
        parse_food_page(read_fixture("food_page_no_name.html"), URL)


def test_parse_food_page_ignores_a_value_in_an_unknown_unit() -> None:
    html = (
        "<h1 id='food-name'>Odd</h1><table class='nutrient results'>"
        "<tr><td><a data-tooltip='Fat'>Fat</a></td><td>3 oz</td></tr>"
        "<tr><td><a data-tooltip='Iron'>Iron</a></td><td>2 mg</td></tr></table>"
    )

    food = parse_food_page(html, URL)

    assert food.fat_g is None
    assert food.iron_mg == pytest.approx(2)


def test_parse_food_page_ignores_json_data_that_is_not_a_breadcrumb() -> None:
    html = (
        "<script type='application/ld+json'>[1, 2]</script>"
        '<script type=\'application/ld+json\'>{"@type": "Product"}</script>'
        '<script type=\'application/ld+json\'>{"@type": "BreadcrumbList", "itemListElement": []}</script>'
        "<h1 id='food-name'>Odd</h1><td id='calories'>10</td>"
    )

    assert parse_food_page(html, URL).category == ""
