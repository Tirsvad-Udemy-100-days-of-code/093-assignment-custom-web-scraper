"""!
@file transport.py
@brief The one place that talks HTTP. Everything else asks the Transport, so tests can replace it.
"""

import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol

from nutrition_scraper.constants import DEFAULT_CHARSET


class TransportError(OSError):
    """!
    @brief The request did not get an answer at all: no network, a timeout or a refused connection.
    """


@dataclass(frozen=True, slots=True)
class TransportResponse:
    """!
    @brief The answer to one request.
    """

    ## HTTP status code, for example 200.
    status: int
    ## The body of the answer as text.
    body: str


class Transport(Protocol):
    """!
    @brief Sends one GET request.
    """

    def get(self, url: str, headers: dict[str, str], timeout: float) -> TransportResponse:
        """!
        @brief Send a GET request.
        @param url Full address.
        @param headers Request headers, for example the User-Agent.
        @param timeout Seconds to wait for the answer.
        @return The status and the body, also for an error status such as 404.
        @throws TransportError When there is no answer at all.
        """
        ...


class UrllibTransport:
    """!
    @brief The real Transport, built on urllib from the standard library.
    @details It uses an opener that knows only http and https, so an address with another scheme (file:, ftp:) can
    never be opened, whatever the caller passes.
    """

    def __init__(self) -> None:
        """!
        @brief Create the transport with an opener for http and https only.
        """
        self._opener = urllib.request.build_opener(urllib.request.HTTPHandler, urllib.request.HTTPSHandler)

    def get(self, url: str, headers: dict[str, str], timeout: float) -> TransportResponse:
        """!
        @brief Send a GET request with urllib.
        @param url Full address; it must start with https:// or http://.
        @param headers Request headers.
        @param timeout Seconds to wait for the answer.
        @return The status and the body.
        @throws TransportError When there is no answer at all.
        """
        if not url.startswith(("https://", "http://")):
            raise TransportError(f"Only http and https addresses are allowed: {url}")
        request = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with self._opener.open(request, timeout=timeout) as response:
                return TransportResponse(response.status, self._decode(response.read(), response.headers))
        except urllib.error.HTTPError as error:
            return TransportResponse(error.code, self._decode(error.read(), error.headers))
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise TransportError(str(error)) from error

    @staticmethod
    def _decode(raw: bytes, headers: object) -> str:
        """!
        @brief Turn the bytes of an answer into text.
        @param raw The bytes.
        @param headers The answer headers; the charset is read from Content-Type.
        @return The text; characters that do not fit the charset are replaced.
        """
        charset = DEFAULT_CHARSET
        get_content_charset = getattr(headers, "get_content_charset", None)
        if callable(get_content_charset):
            charset = get_content_charset() or DEFAULT_CHARSET
        return raw.decode(charset, errors="replace")
