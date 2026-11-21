"""!
@file food_parser.py
@brief Reads the name, category, calories and nutrients out of a food page.
"""

import json
import re
from html.parser import HTMLParser

from nutrition_scraper.application.food_source import SourceError
from nutrition_scraper.constants import NUTRIENT_ROWS, UNIT_PER_GRAM
from nutrition_scraper.domain.food import Food

## A number followed by a unit, for example "36.17 g" or "176 mg".
_VALUE = re.compile(r"^\s*(?P<number>\d+(?:[.,]\d+)?)\s*(?P<unit>[A-Za-zµ]+)?")

## Number of the table cell that holds the amount of a nutrient: name, amount, daily value.
_AMOUNT_CELL = 2

## Position of the category in the breadcrumb of a food page: Home, category, food.
_CATEGORY_POSITION = 2


def _convert(number: float, unit: str, target_unit: str) -> float | None:
    """!
    @brief Convert a value between g, mg and mcg.
    @param number The value as the page shows it.
    @param unit The unit the page shows.
    @param target_unit The unit of the Food field.
    @return The value in the target unit, or None when a unit is unknown.
    """
    if unit == target_unit:
        return number
    if unit not in UNIT_PER_GRAM or target_unit not in UNIT_PER_GRAM:
        return None
    return round(number / UNIT_PER_GRAM[unit] * UNIT_PER_GRAM[target_unit], 6)


class _FoodPageParser(HTMLParser):
    """!
    @brief Collects the pieces of a food page. It keeps a small state: which element it is inside.
    """

    def __init__(self) -> None:
        """!
        @brief Create an empty parser.
        """
        super().__init__(convert_charrefs=True)
        self.name = ""
        self.calories_text = ""
        self.json_ld: list[str] = []
        self.nutrients: dict[str, tuple[float, str]] = {}
        self._in_h1 = False
        self._in_calories = False
        self._in_json_ld = False
        self._table_depth = 0
        self._in_row = False
        self._cell = 0
        self._row_name = ""
        self._cell_text: list[str] = []
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """!
        @brief Track which element the parser is inside.
        @param tag Name of the tag.
        @param attrs Attributes of the tag.
        """
        values = dict(attrs)
        classes = (values.get("class") or "").split()
        if tag == "h1" and values.get("id") == "food-name":
            self._in_h1, self._buffer = True, []
        elif tag == "td" and values.get("id") == "calories":
            self._in_calories, self._buffer = True, []
        elif tag == "script" and values.get("type") == "application/ld+json":
            self._in_json_ld, self._buffer = True, []
        elif tag == "table" and (self._table_depth or ("nutrient" in classes and "results" in classes)):
            self._table_depth += 1  # a table inside a nutrient table, such as the omega ratio, is counted too
        elif self._table_depth and tag == "tr":
            self._in_row, self._cell, self._row_name, self._cell_text = True, 0, "", []
        elif self._in_row and tag == "td":
            self._cell += 1
            self._cell_text = []
        elif self._in_row and self._cell == 1 and tag == "a" and not self._row_name:
            self._row_name = values.get("data-tooltip") or ""

    def handle_data(self, data: str) -> None:
        """!
        @brief Collect text for the element the parser is inside.
        @param data Text found.
        """
        if self._in_h1 or self._in_calories or self._in_json_ld:
            self._buffer.append(data)
        elif self._in_row and self._cell == _AMOUNT_CELL:
            self._cell_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        """!
        @brief Finish the element and keep what was collected.
        @param tag Name of the tag.
        """
        if tag == "h1" and self._in_h1:
            self._in_h1 = False
            self.name = " ".join("".join(self._buffer).split())
        elif tag == "td" and self._in_calories:
            self._in_calories = False
            self.calories_text = "".join(self._buffer)
        elif tag == "script" and self._in_json_ld:
            self._in_json_ld = False
            self.json_ld.append("".join(self._buffer))
        elif tag == "td" and self._in_row and self._cell == _AMOUNT_CELL:
            self._keep_nutrient()
        elif tag == "table" and self._table_depth:
            self._table_depth -= 1
            self._in_row = self._in_row and self._table_depth > 0

    def _keep_nutrient(self) -> None:
        """!
        @brief Keep the value of the current row when it is a nutrient the scraper wants and was not seen before.
        """
        match = _VALUE.match("".join(self._cell_text).replace("\xa0", " "))
        if self._row_name in NUTRIENT_ROWS and match and self._row_name not in self.nutrients:
            number = float(match.group("number").replace(",", "."))
            self.nutrients[self._row_name] = (number, match.group("unit") or "")


def _category_from_breadcrumb(json_ld_blocks: list[str]) -> str:
    """!
    @brief Find the category in the breadcrumb data of the page.
    @param json_ld_blocks The JSON-LD blocks found on the page.
    @return The category name, or an empty text when the page has none.
    """
    for block in json_ld_blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict) or data.get("@type") != "BreadcrumbList":
            continue
        items = data.get("itemListElement", [])
        if len(items) > _CATEGORY_POSITION:
            for item in items:
                if item.get("position") == _CATEGORY_POSITION:
                    return str(item.get("name", ""))
    return ""


def parse_food_page(html: str, url: str) -> Food:
    """!
    @brief Read a food page that shows its values per 100 g.
    @param html The page as text.
    @param url Address of the page, kept in the Food.
    @return The food. A value the page does not give is None.
    @throws SourceError When the page has no name or no values at all.
    """
    parser = _FoodPageParser()
    parser.feed(html)
    parser.close()

    calories_match = _VALUE.match(parser.calories_text)
    calories = float(calories_match.group("number").replace(",", ".")) if calories_match else None
    values: dict[str, float | None] = {}
    for row_name, (field, target_unit) in NUTRIENT_ROWS.items():
        found = parser.nutrients.get(row_name)
        values[field] = _convert(found[0], found[1], target_unit) if found else None

    if not parser.name:
        raise SourceError(f"{url} has no food name")
    if calories is None and all(value is None for value in values.values()):
        raise SourceError(f"{url} has no nutrition values")
    return Food(
        name=parser.name,
        category=_category_from_breadcrumb(parser.json_ld),
        calories_kcal=calories,
        source_url=url,
        **values,
    )
