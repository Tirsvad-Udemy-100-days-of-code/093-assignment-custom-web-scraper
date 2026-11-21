"""!
@file food.py
@brief The Food value object: one food with its values per 100 g.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """!
    @brief One food with its nutrition facts per 100 g.
    @details A value the page does not give is None, never zero, so a missing value cannot earn a tag.
    """

    ## Name of the food.
    name: str
    ## Category of the food on the site, for example "Legumes and Legume Products".
    category: str = ""
    ## Calories in kcal.
    calories_kcal: float | None = None
    ## Protein in grams.
    protein_g: float | None = None
    ## Carbohydrate in grams.
    carbohydrate_g: float | None = None
    ## Dietary fibre in grams.
    fibre_g: float | None = None
    ## Sugars in grams.
    sugars_g: float | None = None
    ## Fat in grams.
    fat_g: float | None = None
    ## Saturated fat in grams.
    saturated_fat_g: float | None = None
    ## Sodium in milligrams.
    sodium_mg: float | None = None
    ## Potassium in milligrams.
    potassium_mg: float | None = None
    ## Calcium in milligrams.
    calcium_mg: float | None = None
    ## Iron in milligrams.
    iron_mg: float | None = None
    ## Vitamin C in milligrams.
    vitamin_c_mg: float | None = None
    ## Address of the page the values were read from.
    source_url: str = ""
    ## Wellness tags the food earned, for example ("high-protein",).
    tags: tuple[str, ...] = ()
