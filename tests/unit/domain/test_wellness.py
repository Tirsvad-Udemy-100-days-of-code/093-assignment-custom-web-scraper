"""!
@file test_wellness.py
@brief Unit tests for the wellness rules. They use plain numbers, no HTML.
"""

import pytest

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
from nutrition_scraper.domain.wellness import classify_wellness, is_wellness_friendly


def food(**values: float | None) -> Food:
    return Food(name="Test food", **values)


def test_protein_at_the_threshold_is_high_protein() -> None:
    assert classify_wellness(food(protein_g=HIGH_PROTEIN_GRAMS)) == (TAG_HIGH_PROTEIN,)


def test_protein_just_below_the_threshold_earns_no_tag() -> None:
    assert classify_wellness(food(protein_g=HIGH_PROTEIN_GRAMS - 0.01)) == ()


def test_fibre_at_the_threshold_is_high_fibre() -> None:
    assert classify_wellness(food(fibre_g=HIGH_FIBRE_GRAMS)) == (TAG_HIGH_FIBRE,)


def test_calories_at_the_threshold_are_low_calorie() -> None:
    assert classify_wellness(food(calories_kcal=LOW_CALORIE_KCAL)) == (TAG_LOW_CALORIE,)


def test_calories_just_above_the_threshold_earn_no_tag() -> None:
    assert classify_wellness(food(calories_kcal=LOW_CALORIE_KCAL + 0.01)) == ()


def test_a_food_can_earn_several_tags_in_a_fixed_order() -> None:
    tags = classify_wellness(food(protein_g=30, fibre_g=10, calories_kcal=50))

    assert tags == (TAG_HIGH_PROTEIN, TAG_HIGH_FIBRE, TAG_LOW_CALORIE)


def test_a_missing_value_never_earns_a_tag() -> None:
    assert classify_wellness(food()) == ()


def test_a_food_with_a_tag_and_low_sodium_is_kept() -> None:
    assert is_wellness_friendly(food(protein_g=25, sodium_mg=MAX_SODIUM_MG))


def test_a_food_with_too_much_sodium_is_left_out() -> None:
    assert not is_wellness_friendly(food(protein_g=25, sodium_mg=MAX_SODIUM_MG + 1))


def test_a_food_without_a_tag_is_left_out() -> None:
    assert not is_wellness_friendly(food(protein_g=5, sodium_mg=1))


def test_a_food_with_unknown_sodium_is_kept() -> None:
    assert is_wellness_friendly(food(fibre_g=8))


@pytest.mark.parametrize("sodium", [0.0, 15.0, 399.9])
def test_sodium_below_the_limit_does_not_block_a_tagged_food(sodium: float) -> None:
    assert is_wellness_friendly(food(calories_kcal=20, sodium_mg=sodium))
