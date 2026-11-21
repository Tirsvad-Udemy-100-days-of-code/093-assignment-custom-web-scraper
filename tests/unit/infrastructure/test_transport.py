"""!
@file test_transport.py
@brief Unit tests for UrllibTransport. urllib is replaced, so no test uses the network.
"""

import email.message
import io
import urllib.error
from types import TracebackType

import pytest

from nutrition_scraper.infrastructure.transport import TransportError, UrllibTransport


class _FakeResponse:
    """!
    @brief What urllib.request.urlopen returns for a successful request.
    """

    def __init__(self, status: int, body: bytes, charset: str | None) -> None:
        self.status = status
        self._body = body
        self.headers = email.message.Message()
        self.headers["Content-Type"] = "text/html" + (f"; charset={charset}" if charset else "")

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        return None


def test_get_returns_status_and_text(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "urllib.request.urlopen", lambda request, timeout: _FakeResponse(200, "blåbær".encode(), "utf-8")
    )

    response = UrllibTransport().get("https://example.test/", {"User-Agent": "test"}, 5)

    assert (response.status, response.body) == (200, "blåbær")


def test_get_uses_the_charset_of_the_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "urllib.request.urlopen", lambda request, timeout: _FakeResponse(200, "blåbær".encode("latin-1"), "latin-1")
    )

    assert UrllibTransport().get("https://example.test/", {}, 5).body == "blåbær"


def test_get_sends_the_given_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, str] = {}

    def fake_urlopen(request: object, timeout: float) -> _FakeResponse:
        seen.update(request.header_items())  # type: ignore[attr-defined]
        return _FakeResponse(200, b"ok", None)

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    UrllibTransport().get("https://example.test/", {"User-Agent": "TestAgent/1"}, 5)

    assert seen["User-agent"] == "TestAgent/1"


def test_get_returns_an_error_status_instead_of_raising(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: object, timeout: float) -> _FakeResponse:
        raise urllib.error.HTTPError(
            "https://example.test/", 404, "Not Found", email.message.Message(), io.BytesIO(b"gone")
        )

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    response = UrllibTransport().get("https://example.test/", {}, 5)

    assert (response.status, response.body) == (404, "gone")


def test_get_raises_transport_error_when_there_is_no_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: object, timeout: float) -> _FakeResponse:
        raise urllib.error.URLError("no route")

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    with pytest.raises(TransportError):
        UrllibTransport().get("https://example.test/", {}, 5)


def test_get_refuses_addresses_that_are_not_http() -> None:
    with pytest.raises(TransportError, match="Only http and https"):
        UrllibTransport().get("file:///etc/passwd", {}, 5)
