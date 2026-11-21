"""!
@file ranked_food.py
@brief A food as listed on a ranking page.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RankedFood:
    """!
    @brief One line of a ranking page: the name of a food and where its page is.
    """

    ## Name of the food, as the ranking page shows it.
    name: str
    ## Path of the food page on the site, without a query, for example "/Lentils_nutritional_value.html".
    path: str
