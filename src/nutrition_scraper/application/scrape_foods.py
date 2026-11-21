"""!
@file scrape_foods.py
@brief The use case: from ranking pages to food pages to the foods that are kept.
"""

import logging
from dataclasses import dataclass, field, replace

from nutrition_scraper.application.food_source import FoodSource, SiteRulesError, SourceError
from nutrition_scraper.domain.food import Food
from nutrition_scraper.domain.wellness import classify_wellness, is_wellness_friendly

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ScrapeResult:
    """!
    @brief What a run gives back.
    """

    ## The foods that were kept, each once, with their tags.
    foods: list[Food] = field(default_factory=list)
    ## A note for each page that was skipped, with the reason.
    skipped: list[str] = field(default_factory=list)
    ## Number of food pages that were read, kept or not.
    foods_read: int = 0


def scrape_foods(
    source: FoodSource,
    rankings: tuple[tuple[str, str], ...],
    foods_per_ranking: int,
) -> ScrapeResult:
    """!
    @brief Read the top foods of each ranking and keep the wellness friendly ones.
    @param source Where the pages come from.
    @param rankings The ranking pages to read, each as a label and a path.
    @param foods_per_ranking How many foods are taken from the top of each ranking.
    @return The kept foods and the pages that were skipped.
    @throws SiteRulesError When the rules of the site cannot be read; the run stops.
    """
    result = ScrapeResult()
    seen_paths: set[str] = set()
    for label, ranking_path in rankings:
        logger.info("Ranking: %s", label)
        try:
            ranked_foods = source.read_ranking(ranking_path)
        except SiteRulesError:
            raise
        except SourceError as error:
            _skip(result, ranking_path, error)
            continue
        for ranked_food in ranked_foods[:foods_per_ranking]:
            if ranked_food.path in seen_paths:
                continue
            seen_paths.add(ranked_food.path)
            try:
                food = source.read_food(ranked_food.path)
            except SiteRulesError:
                raise
            except SourceError as error:
                _skip(result, ranked_food.path, error)
                continue
            result.foods_read += 1
            if is_wellness_friendly(food):
                result.foods.append(replace(food, tags=classify_wellness(food)))
                logger.info("Kept: %s", food.name)
    return result


def _skip(result: ScrapeResult, path: str, error: SourceError) -> None:
    """!
    @brief Note a page that was skipped and carry on.
    @param result The result being built.
    @param path Path of the page.
    @param error Why the page was skipped.
    """
    note = f"{path}: {error}"
    result.skipped.append(note)
    logger.warning("Skipped %s", note)
