"""!
@file test_smoke.py
@brief Smoke tests: the package imports and its constants are polite and consistent.
"""

import nutrition_scraper
from nutrition_scraper import constants


def test_package_has_a_version() -> None:
    assert nutrition_scraper.__version__ == "1.0.0"


def test_delay_is_at_least_twice_the_crawl_delay_of_the_site() -> None:
    assert constants.REQUEST_DELAY_SECONDS >= 2.0


def test_user_agent_names_the_scraper_and_the_project() -> None:
    assert constants.USER_AGENT.startswith(constants.USER_AGENT_NAME)
    assert constants.PROJECT_URL in constants.USER_AGENT


def test_every_ranking_page_is_a_path_on_the_site() -> None:
    assert constants.RANKING_PAGES
    assert all(path.startswith("/") and path.endswith(".html") for _, path in constants.RANKING_PAGES)


def test_csv_columns_are_unique_and_start_with_the_name() -> None:
    assert constants.CSV_COLUMNS[0] == "name"
    assert len(set(constants.CSV_COLUMNS)) == len(constants.CSV_COLUMNS)
