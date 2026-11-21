"""!
@file test_csv_writer.py
@brief Unit tests for save_to_csv.
"""

import csv
from pathlib import Path

from nutrition_scraper.constants import CSV_COLUMNS
from nutrition_scraper.domain.food import Food
from nutrition_scraper.infrastructure.csv_writer import save_to_csv

LENTILS = Food(
    name="Lentils, boiled",
    category="Legumes",
    calories_kcal=116,
    protein_g=9.02,
    fibre_g=7.9,
    sodium_mg=2,
    source_url="https://example.test/lentils.html",
    tags=("high-fibre", "low-calorie"),
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def test_save_to_csv_writes_the_header_and_one_row_per_food(tmp_path: Path) -> None:
    target = tmp_path / "foods.csv"

    written = save_to_csv([LENTILS, Food(name="Plain")], target)

    assert written == 2
    assert target.read_text(encoding="utf-8").splitlines()[0] == ",".join(CSV_COLUMNS)
    assert len(read_rows(target)) == 2


def test_save_to_csv_formats_numbers_and_joins_the_tags(tmp_path: Path) -> None:
    target = tmp_path / "foods.csv"

    save_to_csv([LENTILS], target)

    row = read_rows(target)[0]
    assert row["calories_kcal"] == "116"
    assert row["protein_g"] == "9.02"
    assert row["tags"] == "high-fibre;low-calorie"
    assert row["source_url"] == "https://example.test/lentils.html"


def test_save_to_csv_leaves_a_missing_value_empty(tmp_path: Path) -> None:
    target = tmp_path / "foods.csv"

    save_to_csv([Food(name="Plain")], target)

    assert read_rows(target)[0]["protein_g"] == ""


def test_save_to_csv_keeps_commas_and_quotes_in_a_name(tmp_path: Path) -> None:
    target = tmp_path / "foods.csv"

    save_to_csv([Food(name='Beans, "baked"')], target)

    assert read_rows(target)[0]["name"] == 'Beans, "baked"'


def test_save_to_csv_stops_a_spreadsheet_from_reading_a_name_as_a_formula(tmp_path: Path) -> None:
    target = tmp_path / "foods.csv"

    save_to_csv([Food(name="=SUM(A1)")], target)

    assert read_rows(target)[0]["name"] == "'=SUM(A1)"


def test_save_to_csv_creates_a_missing_folder(tmp_path: Path) -> None:
    target = tmp_path / "data" / "deep" / "foods.csv"

    save_to_csv([LENTILS], target)

    assert target.exists()


def test_save_to_csv_writes_only_the_header_for_no_foods(tmp_path: Path) -> None:
    target = tmp_path / "foods.csv"

    assert save_to_csv([], target) == 0
    assert read_rows(target) == []
    assert target.read_text(encoding="utf-8").strip() == ",".join(CSV_COLUMNS)


def test_save_to_csv_replaces_an_old_file_and_leaves_no_temporary_file(tmp_path: Path) -> None:
    target = tmp_path / "foods.csv"
    target.write_text("old", encoding="utf-8")

    save_to_csv([LENTILS], target)

    assert read_rows(target)[0]["name"] == "Lentils, boiled"
    assert [item.name for item in tmp_path.iterdir()] == ["foods.csv"]


def test_save_to_csv_keeps_the_old_file_when_writing_fails(tmp_path: Path) -> None:
    target = tmp_path / "foods.csv"
    target.write_text("old", encoding="utf-8")

    try:
        save_to_csv([LENTILS, object()], target)  # type: ignore[list-item]
    except AttributeError:
        pass

    assert target.read_text(encoding="utf-8") == "old"
    assert [item.name for item in tmp_path.iterdir()] == ["foods.csv"]
