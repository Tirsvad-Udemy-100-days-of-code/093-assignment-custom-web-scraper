"""!
@file nutritionvalue_source.py
@brief The FoodSource that reads nutritionvalue.org through the polite web client.
"""

from nutrition_scraper.constants import BASE_URL, PORTION_QUERY
from nutrition_scraper.domain.food import Food
from nutrition_scraper.domain.ranked_food import RankedFood
from nutrition_scraper.infrastructure.food_parser import parse_food_page
from nutrition_scraper.infrastructure.polite_web_client import PoliteWebClient
from nutrition_scraper.infrastructure.ranking_parser import parse_ranking_page


class NutritionValueSource:
    """!
    @brief Reads ranking pages and food pages of nutritionvalue.org. Implements the FoodSource port.
    """

    def __init__(self, client: PoliteWebClient, base_url: str = BASE_URL) -> None:
        """!
        @brief Create the source.
        @param client The client every request goes through.
        @param base_url Address of the site, without a trailing slash.
        """
        self._client = client
        self._base_url = base_url.rstrip("/")

    def read_ranking(self, path: str) -> list[RankedFood]:
        """!
        @brief Read a ranking page.
        @param path Path of the ranking page.
        @return The foods of the page, best first.
        @throws SourceError When the page is refused or cannot be read.
        """
        return parse_ranking_page(self._client.fetch_page(path))

    def read_food(self, path: str) -> Food:
        """!
        @brief Read a food page with the values per 100 g.
        @param path Path of the food page, without a query.
        @return The food.
        @throws SourceError When the page is refused, cannot be read or has no values.
        """
        html = self._client.fetch_page(f"{path}?{PORTION_QUERY}")
        return parse_food_page(html, f"{self._base_url}{path}")
