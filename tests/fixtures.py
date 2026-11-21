"""!
@file fixtures.py
@brief Helper that reads the HTML and text fixtures written for the tests.
"""

from pathlib import Path

FIXTURE_DIRECTORY = Path(__file__).parent / "fixtures"


def read_fixture(name: str) -> str:
    """!
    @brief Read a fixture file.
    @param name File name inside tests/fixtures.
    @return The content as text.
    """
    return (FIXTURE_DIRECTORY / name).read_text(encoding="utf-8")
