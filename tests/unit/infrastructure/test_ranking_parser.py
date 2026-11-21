"""!
@file test_ranking_parser.py
@brief Unit tests for parse_ranking_page.
"""

from fixtures import read_fixture
from nutrition_scraper.domain.ranked_food import RankedFood
from nutrition_scraper.infrastructure.ranking_parser import parse_ranking_page


def test_parse_ranking_page_returns_the_foods_in_page_order() -> None:
    foods = parse_ranking_page(read_fixture("ranking_page.html"))

    assert [food.name for food in foods] == ["Lentils, one", "Beans, two", "Peas, three"]


def test_parse_ranking_page_removes_the_query_from_the_path() -> None:
    foods = parse_ranking_page(read_fixture("ranking_page.html"))

    assert foods[0] == RankedFood(name="Lentils, one", path="/Lentils_one_nutritional_value.html")


def test_parse_ranking_page_lists_a_food_once() -> None:
    foods = parse_ranking_page(read_fixture("ranking_page.html"))

    assert len({food.path for food in foods}) == len(foods)


def test_parse_ranking_page_uses_the_link_text_when_the_title_is_missing() -> None:
    foods = parse_ranking_page(read_fixture("ranking_page.html"))

    assert foods[2].name == "Peas, three"


def test_parse_ranking_page_ignores_links_that_are_not_foods() -> None:
    foods = parse_ranking_page(read_fixture("ranking_page.html"))

    assert all("articles" not in food.path and "page_1" not in food.path for food in foods)


def test_parse_ranking_page_returns_nothing_for_a_page_without_foods() -> None:
    assert parse_ranking_page("<html><body><p>Nothing here</p></body></html>") == []
