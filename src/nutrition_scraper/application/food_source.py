"""!
@file food_source.py
@brief The port through which the use case reads foods, and the error it raises.
"""

from typing import Protocol

from nutrition_scraper.domain.food import Food
from nutrition_scraper.domain.ranked_food import RankedFood


class SourceError(ValueError):
    """!
    @brief A page could not be used: refused by the site rules, not reachable, or without values.
    """


class FoodSource(Protocol):
    """!
    @brief Where foods come from. The use case knows only this interface, so it can be tested without the network.
    """

    def read_ranking(self, path: str) -> list[RankedFood]:
        """!
        @brief Read a ranking page.
        @param path Path of the ranking page on the site.
        @return The foods of the page, best first.
        @throws SourceError When the page is refused, not reachable or has no foods.
        """
        ...

    def read_food(self, path: str) -> Food:
        """!
        @brief Read a food page with its values per 100 g.
        @param path Path of the food page on the site.
        @return The food.
        @throws SourceError When the page is refused, not reachable or has no values.
        """
        ...
