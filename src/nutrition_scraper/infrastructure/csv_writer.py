"""!
@file csv_writer.py
@brief Writes the kept foods to a CSV file.
"""

import csv
import os
import tempfile
from pathlib import Path

from nutrition_scraper.constants import CSV_COLUMNS
from nutrition_scraper.domain.food import Food

## First characters that make a spreadsheet read a cell as a formula.
_FORMULA_STARTS = ("=", "+", "-", "@", "\t", "\r")


def _format_cell(value: object) -> str:
    """!
    @brief Turn one value of a Food into the text of a CSV cell.
    @param value The value: None, a number, a text or a tuple of tags.
    @return An empty text for None, numbers with at most three decimals, tags joined with a semicolon. A text that a
    spreadsheet would read as a formula gets a leading apostrophe.
    """
    if value is None:
        return ""
    if isinstance(value, tuple):
        return ";".join(str(item) for item in value)
    if isinstance(value, float):
        return f"{value:.3f}".rstrip("0").rstrip(".")
    text = str(value)
    return "'" + text if text.startswith(_FORMULA_STARTS) else text


def save_to_csv(foods: list[Food], path: Path) -> int:
    """!
    @brief Write foods to a CSV file: one header row, then one row per food.
    @details The file is written to a temporary file next to the target and then moved into place, so a failed run
    never leaves a half-written CSV. A missing folder is created.
    @param foods The foods to write.
    @param path The CSV file.
    @return The number of food rows written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            for food in foods:
                writer.writerow({column: _format_cell(getattr(food, column)) for column in CSV_COLUMNS})
        Path(temporary_name).replace(path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise
    return len(foods)
