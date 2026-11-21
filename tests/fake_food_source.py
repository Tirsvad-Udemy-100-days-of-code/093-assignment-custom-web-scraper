"""!
@file fake_food_source.py
@brief A FoodSource that answers from dictionaries, so the use case and the command line are tested without HTML.
"""

from nutrition_scraper.application.food_source import SourceError
from nutrition_scraper.domain.food import Food
from nutrition_scraper.domain.ranked_food import RankedFood


class FakeFoodSource:
    """!
    @brief Gives prepared rankings and foods; an Exception in the dictionaries is raised instead.
    """

    def __init__(self, rankings: dict[str, list[RankedFood] | Exception], foods: dict[str, Food | Exception]) -> None:
        """!
        @brief Create the fake.
        @param rankings Ranking path to its foods, or to an error.
        @param foods Food path to its Food, or to an error.
        """
        self._rankings = rankings
        self._foods = foods
        self.read_foods: list[str] = []

    def read_ranking(self, path: str) -> list[RankedFood]:
        """!
        @brief Give the prepared ranking.
        @param path Ranking path.
        @return The foods.
        @throws SourceError For an unknown path or a prepared error.
        """
        item = self._rankings.get(path, SourceError(f"unknown ranking {path}"))
        if isinstance(item, Exception):
            raise item
        return item

    def read_food(self, path: str) -> Food:
        """!
        @brief Give the prepared food and remember that it was read.
        @param path Food path.
        @return The food.
        @throws SourceError For an unknown path or a prepared error.
        """
        self.read_foods.append(path)
        item = self._foods.get(path, SourceError(f"unknown food {path}"))
        if isinstance(item, Exception):
            raise item
        return item
