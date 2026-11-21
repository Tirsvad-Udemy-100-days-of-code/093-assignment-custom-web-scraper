"""!
@file test_cli.py
@brief Integration tests of the command line: arguments, use case and CSV writer together, with a fake source.
"""

import csv
import logging
from pathlib import Path

import pytest

from fake_food_source import FakeFoodSource
from nutrition_scraper.__main__ import build_source, main
from nutrition_scraper.application.food_source import SiteRulesError
from nutrition_scraper.constants import RANKING_PAGES
from nutrition_scraper.domain.food import Food
from nutrition_scraper.domain.ranked_food import RankedFood
from nutrition_scraper.infrastructure.nutritionvalue_source import NutritionValueSource

FIRST_RANKING = RANKING_PAGES[0][1]


def make_source() -> FakeFoodSource:
    return FakeFoodSource(
        rankings={FIRST_RANKING: [RankedFood("Salmon", "/salmon.html"), RankedFood("Bread", "/bread.html")]},
        foods={
            "/salmon.html": Food(name="Salmon", protein_g=25, sodium_mg=60, calories_kcal=200),
            "/bread.html": Food(name="Bread", protein_g=8, sodium_mg=500, calories_kcal=260),
        },
    )


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_main_writes_the_csv_and_returns_zero(tmp_path: Path) -> None:
    target = tmp_path / "out.csv"

    code = main(["--output", str(target)], source=make_source())

    assert code == 0
    assert [row["name"] for row in read_rows(target)] == ["Salmon"]
    assert read_rows(target)[0]["tags"] == "high-protein"


def test_main_passes_the_limit_to_the_use_case(tmp_path: Path) -> None:
    source = make_source()

    main(["--output", str(tmp_path / "out.csv"), "--limit", "1"], source=source)

    assert source.read_foods == ["/salmon.html"]


def test_main_reports_what_it_did(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO, logger="nutrition_scraper")

    main(["--output", str(tmp_path / "out.csv")], source=make_source())

    assert any("Wrote 1 foods" in message for message in caplog.messages)


def test_main_writes_a_header_only_csv_when_nothing_matches(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO, logger="nutrition_scraper")
    source = FakeFoodSource({FIRST_RANKING: [RankedFood("Bread", "/bread.html")]}, {"/bread.html": Food(name="Bread")})
    target = tmp_path / "out.csv"

    assert main(["--output", str(target)], source=source) == 0

    assert read_rows(target) == []
    assert any("No food matched" in message for message in caplog.messages)


def test_main_writes_nothing_and_returns_one_when_the_site_rules_cannot_be_read(tmp_path: Path) -> None:
    source = FakeFoodSource({FIRST_RANKING: SiteRulesError("no rules")}, {})
    target = tmp_path / "out.csv"

    assert main(["--output", str(target)], source=source) == 1
    assert not target.exists()


@pytest.mark.parametrize("bad_limit", ["0", "-3", "many"])
def test_main_refuses_a_limit_that_is_not_a_positive_whole_number(bad_limit: str, tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        main(["--output", str(tmp_path / "out.csv"), "--limit", bad_limit], source=make_source())


def test_build_source_wires_the_real_source_without_touching_the_network() -> None:
    assert isinstance(build_source(0.5), NutritionValueSource)
