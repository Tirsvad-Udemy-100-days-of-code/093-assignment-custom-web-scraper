"""!
@file test_nutritionvalue_source.py
@brief Unit tests for NutritionValueSource, with a fake transport behind a real PoliteWebClient.
"""

import pytest

from fake_transport import FakeClock, FakeTransport
from fixtures import read_fixture
from nutrition_scraper.application.food_source import SourceError
from nutrition_scraper.infrastructure.nutritionvalue_source import NutritionValueSource
from nutrition_scraper.infrastructure.polite_web_client import PoliteWebClient
from nutrition_scraper.infrastructure.transport import TransportResponse

BASE = "https://site.test"


def make_source(pages: dict[str, str]) -> tuple[NutritionValueSource, FakeTransport]:
    answers = {BASE + path: [TransportResponse(200, html)] for path, html in pages.items()}
    transport = FakeTransport({BASE + "/robots.txt": [TransportResponse(200, "User-agent: *\n")], **answers})
    clock = FakeClock()
    client = PoliteWebClient(transport, base_url=BASE, sleep=clock.sleep, clock=clock.time)
    return NutritionValueSource(client, base_url=BASE), transport


def test_read_ranking_returns_the_foods_of_the_page() -> None:
    source, _ = make_source({"/ranking.html": read_fixture("ranking_page.html")})

    foods = source.read_ranking("/ranking.html")

    assert [food.path for food in foods][:2] == [
        "/Lentils_one_nutritional_value.html",
        "/Beans_two_nutritional_value.html",
    ]


def test_read_food_asks_for_the_values_per_100_g() -> None:
    source, transport = make_source({"/food.html?size=100%20g": read_fixture("food_page.html")})

    food = source.read_food("/food.html")

    assert transport.urls[-1] == BASE + "/food.html?size=100%20g"
    assert food.name == "Lentils, one"
    assert food.source_url == BASE + "/food.html"


def test_read_food_passes_on_a_page_without_values() -> None:
    source, _ = make_source({"/food.html?size=100%20g": read_fixture("food_page_empty.html")})

    with pytest.raises(SourceError):
        source.read_food("/food.html")
