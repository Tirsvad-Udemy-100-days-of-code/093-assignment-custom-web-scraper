"""!
@file fake_transport.py
@brief A Transport that answers from a script and a clock that never waits, for the client tests.
"""

from nutrition_scraper.infrastructure.transport import TransportError, TransportResponse


class FakeTransport:
    """!
    @brief Answers each URL from a list of prepared answers and records every request.
    """

    def __init__(self, answers: dict[str, list[TransportResponse | TransportError]]) -> None:
        """!
        @brief Create the fake.
        @param answers For each URL, the answers to give one after the other; the last one repeats.
        """
        self._answers = {url: list(items) for url, items in answers.items()}
        self.requests: list[tuple[str, dict[str, str]]] = []

    def get(self, url: str, headers: dict[str, str], timeout: float) -> TransportResponse:
        """!
        @brief Record the request and give the next prepared answer.
        @param url Address.
        @param headers Request headers.
        @param timeout Ignored.
        @return The prepared answer, or 404 for an unknown URL.
        @throws TransportError When the prepared answer is an error.
        """
        self.requests.append((url, headers))
        items = self._answers.get(url)
        if not items:
            return TransportResponse(404, "not found")
        item = items.pop(0) if len(items) > 1 else items[0]
        if isinstance(item, TransportError):
            raise item
        return item

    @property
    def urls(self) -> list[str]:
        """!
        @brief The addresses requested so far, in order.
        @return The addresses.
        """
        return [url for url, _ in self.requests]


class FakeClock:
    """!
    @brief A clock and a sleep that move time forward without waiting.
    """

    def __init__(self) -> None:
        """!
        @brief Start at time zero.
        """
        self.now = 0.0
        self.sleeps: list[float] = []

    def time(self) -> float:
        """!
        @brief The current fake time.
        @return Seconds.
        """
        return self.now

    def sleep(self, seconds: float) -> None:
        """!
        @brief Record a wait and move the time forward.
        @param seconds How long to wait.
        """
        self.sleeps.append(seconds)
        self.now += seconds
