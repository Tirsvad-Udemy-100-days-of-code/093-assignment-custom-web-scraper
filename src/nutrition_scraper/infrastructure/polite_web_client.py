"""!
@file polite_web_client.py
@brief Fetches pages the way a good guest does: robots.txt first, a pause between requests, an honest User-Agent.
"""

import logging
import time
import urllib.robotparser
from collections.abc import Callable
from http import HTTPStatus
from urllib.parse import urljoin

from nutrition_scraper.application.food_source import SourceError
from nutrition_scraper.constants import (
    BASE_URL,
    MAX_RETRIES,
    REQUEST_DELAY_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
    RETRY_BACKOFF_SECONDS,
    RETRY_STATUS_CODES,
    ROBOTS_PATH,
    USER_AGENT,
    USER_AGENT_NAME,
)
from nutrition_scraper.infrastructure.transport import Transport, TransportError

logger = logging.getLogger(__name__)


class PoliteWebClient:
    """!
    @brief Fetches pages from one site and follows its rules.
    @details Before the first page it reads robots.txt. A path the file disallows is refused before any request is
    sent. Between two requests it waits at least the configured delay, or the Crawl-delay of the site if that is
    longer. A request that fails for a temporary reason is repeated a limited number of times.
    """

    def __init__(
        self,
        transport: Transport,
        base_url: str = BASE_URL,
        user_agent: str = USER_AGENT,
        delay_seconds: float = REQUEST_DELAY_SECONDS,
        timeout_seconds: float = REQUEST_TIMEOUT_SECONDS,
        max_retries: int = MAX_RETRIES,
        backoff_seconds: float = RETRY_BACKOFF_SECONDS,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        """!
        @brief Create a client.
        @param transport Sends the requests.
        @param base_url Address of the site, without a trailing slash.
        @param user_agent Value of the User-Agent header.
        @param delay_seconds Wait between two requests.
        @param timeout_seconds Seconds to wait for one answer.
        @param max_retries How many times a temporarily failed request is repeated.
        @param backoff_seconds Pause before a repeat, multiplied by the number of the repeat.
        @param sleep Waits; replaced in tests so they do not wait.
        @param clock Gives the time in seconds; replaced in tests.
        """
        self._transport = transport
        self._base_url = base_url.rstrip("/")
        self._user_agent = user_agent
        self._delay_seconds = delay_seconds
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries
        self._backoff_seconds = backoff_seconds
        self._sleep = sleep
        self._clock = clock
        self._robots: urllib.robotparser.RobotFileParser | None = None
        self._last_request: float | None = None

    def fetch_page(self, path: str) -> str:
        """!
        @brief Fetch one page of the site.
        @param path Path on the site, with a query if needed, for example "/page.html?size=100%20g".
        @return The page as text.
        @throws SourceError When robots.txt refuses the path, the page does not exist, or it still fails after the
        repeats.
        """
        url = urljoin(self._base_url + "/", path.lstrip("/"))
        robots = self._load_robots()
        if not robots.can_fetch(USER_AGENT_NAME, url):
            raise SourceError(f"robots.txt does not allow {path}")
        return self._get_with_repeats(url)

    @property
    def effective_delay(self) -> float:
        """!
        @brief The wait between two requests in use.
        @return The configured delay, or the Crawl-delay of the site when that is longer.
        """
        robots_delay = self._robots.crawl_delay(USER_AGENT_NAME) if self._robots else None
        return max(self._delay_seconds, float(robots_delay or 0))

    def _load_robots(self) -> urllib.robotparser.RobotFileParser:
        """!
        @brief Read robots.txt once, on the first request.
        @return The parsed rules.
        @throws SourceError When the site cannot give its rules because of a server error or no answer.
        """
        if self._robots is not None:
            return self._robots
        self._wait_for_turn()
        try:
            response = self._transport.get(self._base_url + ROBOTS_PATH, self._headers(), self._timeout_seconds)
        except TransportError as error:
            raise SourceError(f"The rules of the site could not be read: {error}") from error
        robots = urllib.robotparser.RobotFileParser()
        if response.status == HTTPStatus.OK:
            robots.parse(response.body.splitlines())
        elif HTTPStatus.BAD_REQUEST <= response.status < HTTPStatus.INTERNAL_SERVER_ERROR:
            robots.parse([])  # no robots.txt: everything is allowed (RFC 9309)
        else:
            raise SourceError(f"The rules of the site could not be read: status {response.status}")
        self._robots = robots
        return robots

    def _get_with_repeats(self, url: str) -> str:
        """!
        @brief Send the request, repeating it when the failure is temporary.
        @param url Full address.
        @return The body of the answer.
        @throws SourceError When the page does not exist or all attempts fail.
        """
        last_problem = "no answer"
        for attempt in range(self._max_retries + 1):
            if attempt:
                self._sleep(self._backoff_seconds * attempt)
            self._wait_for_turn()
            try:
                response = self._transport.get(url, self._headers(), self._timeout_seconds)
            except TransportError as error:
                last_problem = str(error)
                logger.warning("Request failed (%s), attempt %d", error, attempt + 1)
                continue
            if response.status == HTTPStatus.OK:
                return response.body
            last_problem = f"status {response.status}"
            if response.status not in RETRY_STATUS_CODES:
                break
            logger.warning("Status %d for %s, attempt %d", response.status, url, attempt + 1)
        raise SourceError(f"{url} could not be read: {last_problem}")

    def _wait_for_turn(self) -> None:
        """!
        @brief Wait until enough time has passed since the last request, then note the time of this one.
        """
        if self._last_request is not None:
            wait = self.effective_delay - (self._clock() - self._last_request)
            if wait > 0:
                self._sleep(wait)
        self._last_request = self._clock()

    def _headers(self) -> dict[str, str]:
        """!
        @brief The headers sent with every request.
        @return The User-Agent and the kinds of content the scraper accepts.
        """
        return {"User-Agent": self._user_agent, "Accept": "text/html,text/plain;q=0.9"}
