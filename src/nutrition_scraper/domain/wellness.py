"""!
@file wellness.py
@brief The wellness rules: which tags a food earns and whether it is kept.
@details The rules are simple thresholds per 100 g, kept in constants.py (ADR-0002). They are a study rule, not
dietary advice.
"""

from nutrition_scraper.constants import (
    HIGH_FIBRE_GRAMS,
    HIGH_PROTEIN_GRAMS,
    LOW_CALORIE_KCAL,
    MAX_SODIUM_MG,
    TAG_HIGH_FIBRE,
    TAG_HIGH_PROTEIN,
    TAG_LOW_CALORIE,
)
from nutrition_scraper.domain.food import Food


def classify_wellness(food: Food) -> tuple[str, ...]:
    """!
    @brief Find the wellness tags a food earns.
    @param food The food with its values per 100 g. A value that is None never earns a tag.
    @return The tags in a fixed order: high-protein, high-fibre, low-calorie; empty when none is earned.
    """
    tags: list[str] = []
    if food.protein_g is not None and food.protein_g >= HIGH_PROTEIN_GRAMS:
        tags.append(TAG_HIGH_PROTEIN)
    if food.fibre_g is not None and food.fibre_g >= HIGH_FIBRE_GRAMS:
        tags.append(TAG_HIGH_FIBRE)
    if food.calories_kcal is not None and food.calories_kcal <= LOW_CALORIE_KCAL:
        tags.append(TAG_LOW_CALORIE)
    return tuple(tags)


def is_wellness_friendly(food: Food) -> bool:
    """!
    @brief Decide whether a food is kept: it earns at least one tag and is not high in sodium.
    @param food The food with its values per 100 g.
    @return True when the food is kept. A food with an unknown sodium value is kept.
    """
    if not classify_wellness(food):
        return False
    return food.sodium_mg is None or food.sodium_mg <= MAX_SODIUM_MG
