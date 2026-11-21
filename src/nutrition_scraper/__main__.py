"""!
@file __main__.py
@brief The command line and the composition root: python -m nutrition_scraper [--output FILE] [--limit N] [--delay S].
"""

import argparse
import logging
from pathlib import Path

from nutrition_scraper.application.food_source import FoodSource, SiteRulesError
from nutrition_scraper.application.scrape_foods import scrape_foods
from nutrition_scraper.constants import (
    APP_TITLE,
    DEFAULT_FOODS_PER_RANKING,
    DEFAULT_OUTPUT_PATH,
    RANKING_PAGES,
    REQUEST_DELAY_SECONDS,
)
from nutrition_scraper.infrastructure.csv_writer import save_to_csv
from nutrition_scraper.infrastructure.nutritionvalue_source import NutritionValueSource
from nutrition_scraper.infrastructure.polite_web_client import PoliteWebClient
from nutrition_scraper.infrastructure.transport import UrllibTransport

logger = logging.getLogger("nutrition_scraper")


def _positive_int(text: str) -> int:
    """!
    @brief Read a whole number of at least 1 from the command line.
    @param text The argument.
    @return The number.
    @throws argparse.ArgumentTypeError When the text is not a whole number of at least 1.
    """
    try:
        number = int(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"{text!r} is not a whole number") from error
    if number < 1:
        raise argparse.ArgumentTypeError("the number must be at least 1")
    return number


def build_source(delay_seconds: float) -> FoodSource:
    """!
    @brief Wire the real source: transport, polite client and the nutritionvalue.org reader.
    @param delay_seconds Wait between two requests; a value below the polite minimum is raised to it.
    @return The source.
    """
    client = PoliteWebClient(UrllibTransport(), delay_seconds=max(delay_seconds, REQUEST_DELAY_SECONDS))
    return NutritionValueSource(client)


def main(argv: list[str] | None = None, source: FoodSource | None = None) -> int:
    """!
    @brief Run the scraper and write the CSV.
    @param argv Command-line arguments; None reads sys.argv.
    @param source The food source; None builds the real one. Tests pass a fake.
    @return 0 when the CSV was written, 1 when the run stopped because the rules of the site could not be read.
    """
    parser = argparse.ArgumentParser(prog="nutrition_scraper", description=APP_TITLE)
    parser.add_argument("--output", type=Path, default=Path(DEFAULT_OUTPUT_PATH), help="CSV file to write")
    parser.add_argument(
        "--limit",
        type=_positive_int,
        default=DEFAULT_FOODS_PER_RANKING,
        help=f"foods taken from the top of each ranking page (default {DEFAULT_FOODS_PER_RANKING})",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=REQUEST_DELAY_SECONDS,
        help=f"seconds between requests; values below {REQUEST_DELAY_SECONDS:g} are raised to it",
    )
    arguments = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    active_source = source if source is not None else build_source(arguments.delay)
    try:
        result = scrape_foods(active_source, RANKING_PAGES, arguments.limit)
    except SiteRulesError as error:
        logger.error("%s; nothing was written", error)
        return 1

    written = save_to_csv(result.foods, arguments.output)
    logger.info(
        "Wrote %d foods to %s (read %d food pages, skipped %d pages)",
        written,
        arguments.output,
        result.foods_read,
        len(result.skipped),
    )
    if not result.foods:
        logger.info("No food matched the wellness rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
