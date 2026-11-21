"""!
@file ranking_parser.py
@brief Reads the foods out of a ranking page.
"""

from html.parser import HTMLParser
from urllib.parse import urlsplit

from nutrition_scraper.domain.ranked_food import RankedFood

## CSS class that marks a food link on a ranking page.
_FOOD_LINK_CLASS = "table_item_name"


class _RankingPageParser(HTMLParser):
    """!
    @brief Collects the food links of a ranking page, in page order.
    """

    def __init__(self) -> None:
        """!
        @brief Create an empty parser.
        """
        super().__init__(convert_charrefs=True)
        self.foods: list[RankedFood] = []
        self._current_href: str | None = None
        self._current_title: str = ""
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """!
        @brief Note the start of a food link.
        @param tag Name of the tag.
        @param attrs Attributes of the tag.
        """
        if tag != "a":
            return
        values = dict(attrs)
        if _FOOD_LINK_CLASS in (values.get("class") or "").split() and values.get("href"):
            self._current_href = values["href"]
            self._current_title = values.get("title") or ""
            self._text = []

    def handle_data(self, data: str) -> None:
        """!
        @brief Collect the text inside a food link.
        @param data Text found.
        """
        if self._current_href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        """!
        @brief Finish a food link and keep the food.
        @param tag Name of the tag.
        """
        if tag != "a" or self._current_href is None:
            return
        name = self._current_title or "".join(self._text)
        path = urlsplit(self._current_href).path
        if name.strip() and path:
            self.foods.append(RankedFood(name=" ".join(name.split()), path=path))
        self._current_href = None


def parse_ranking_page(html: str) -> list[RankedFood]:
    """!
    @brief Read the foods of a ranking page.
    @param html The page as text.
    @return The foods in page order, each path once; empty when the page lists no foods.
    """
    parser = _RankingPageParser()
    parser.feed(html)
    parser.close()
    seen: set[str] = set()
    unique: list[RankedFood] = []
    for food in parser.foods:
        if food.path not in seen:
            seen.add(food.path)
            unique.append(food)
    return unique
