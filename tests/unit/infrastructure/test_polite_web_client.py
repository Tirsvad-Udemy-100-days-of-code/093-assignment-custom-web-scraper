"""!
@file test_polite_web_client.py
@brief Unit tests for PoliteWebClient: robots.txt, delay, repeats and the User-Agent.
"""

import pytest

from fake_transport import FakeClock, FakeTransport
from fixtures import read_fixture
from nutrition_scraper.application.food_source import SourceError
from nutrition_scraper.infrastructure.polite_web_client import PoliteWebClient
from nutrition_scraper.infrastructure.transport import TransportError, TransportResponse

BASE = "https://site.test"
ROBOTS = BASE + "/robots.txt"
PAGE = BASE + "/page.html"
OK = TransportResponse(200, "<html>page</html>")


def make_client(
    answers: dict[str, list[TransportResponse | TransportError]], **options: float
) -> tuple[PoliteWebClient, FakeTransport, FakeClock]:
    transport = FakeTransport({ROBOTS: [TransportResponse(200, read_fixture("robots.txt"))], **answers})
    clock = FakeClock()
    client = PoliteWebClient(
        transport,
        base_url=BASE,
        user_agent="TestAgent/1",
        sleep=clock.sleep,
        clock=clock.time,
        **options,  # type: ignore[arg-type]
    )
    return client, transport, clock


def test_fetch_page_reads_robots_txt_before_the_first_page() -> None:
    client, transport, _ = make_client({PAGE: [OK]})

    assert client.fetch_page("/page.html") == "<html>page</html>"
    assert transport.urls == [ROBOTS, PAGE]


def test_fetch_page_reads_robots_txt_only_once() -> None:
    client, transport, _ = make_client({PAGE: [OK]})

    client.fetch_page("/page.html")
    client.fetch_page("/page.html")

    assert transport.urls.count(ROBOTS) == 1


def test_fetch_page_refuses_a_disallowed_path_without_sending_a_request() -> None:
    client, transport, _ = make_client({})

    with pytest.raises(SourceError, match="robots.txt does not allow /diary.php"):
        client.fetch_page("/diary.php")

    assert transport.urls == [ROBOTS]


def test_fetch_page_sends_the_user_agent() -> None:
    client, transport, _ = make_client({PAGE: [OK]})

    client.fetch_page("/page.html")

    assert all(headers["User-Agent"] == "TestAgent/1" for _, headers in transport.requests)


def test_fetch_page_waits_at_least_the_delay_between_requests() -> None:
    client, _, clock = make_client({PAGE: [OK]}, delay_seconds=2.0)

    client.fetch_page("/page.html")
    client.fetch_page("/page.html")

    assert clock.sleeps == [2.0, 2.0]


def test_fetch_page_does_not_wait_when_enough_time_has_passed() -> None:
    client, _, clock = make_client({PAGE: [OK]}, delay_seconds=2.0)

    client.fetch_page("/page.html")
    clock.now += 10
    client.fetch_page("/page.html")

    assert clock.sleeps == [2.0]


def test_effective_delay_is_the_crawl_delay_of_the_site_when_that_is_longer() -> None:
    transport = FakeTransport({ROBOTS: [TransportResponse(200, "User-agent: *\nCrawl-delay: 5\n")], PAGE: [OK]})
    clock = FakeClock()
    client = PoliteWebClient(transport, base_url=BASE, delay_seconds=2.0, sleep=clock.sleep, clock=clock.time)

    client.fetch_page("/page.html")

    assert client.effective_delay == pytest.approx(5.0)


def test_fetch_page_repeats_a_temporary_failure_and_then_succeeds() -> None:
    client, transport, clock = make_client({PAGE: [TransportResponse(503, "busy"), OK]}, backoff_seconds=5.0)

    assert client.fetch_page("/page.html") == "<html>page</html>"
    assert transport.urls.count(PAGE) == 2
    assert 5.0 in clock.sleeps


def test_fetch_page_repeats_after_a_transport_error() -> None:
    client, transport, _ = make_client({PAGE: [TransportError("timeout"), OK]})

    assert client.fetch_page("/page.html") == "<html>page</html>"
    assert transport.urls.count(PAGE) == 2


def test_fetch_page_gives_up_after_the_repeats() -> None:
    client, transport, _ = make_client({PAGE: [TransportResponse(503, "busy")]}, max_retries=2)

    with pytest.raises(SourceError, match="status 503"):
        client.fetch_page("/page.html")

    assert transport.urls.count(PAGE) == 3


def test_fetch_page_does_not_repeat_a_missing_page() -> None:
    client, transport, _ = make_client({})

    with pytest.raises(SourceError, match="status 404"):
        client.fetch_page("/missing.html")

    assert transport.urls.count(BASE + "/missing.html") == 1


def test_robots_txt_that_is_missing_allows_everything() -> None:
    transport = FakeTransport({ROBOTS: [TransportResponse(404, "")], PAGE: [OK]})
    clock = FakeClock()
    client = PoliteWebClient(transport, base_url=BASE, sleep=clock.sleep, clock=clock.time)

    assert client.fetch_page("/page.html") == "<html>page</html>"


def test_robots_txt_with_a_server_error_stops_the_run() -> None:
    transport = FakeTransport({ROBOTS: [TransportResponse(500, "")]})
    client = PoliteWebClient(transport, base_url=BASE, sleep=lambda _: None)

    with pytest.raises(SourceError, match="rules of the site could not be read"):
        client.fetch_page("/page.html")


def test_robots_txt_that_cannot_be_reached_stops_the_run() -> None:
    transport = FakeTransport({ROBOTS: [TransportError("no network")]})
    client = PoliteWebClient(transport, base_url=BASE, sleep=lambda _: None)

    with pytest.raises(SourceError, match="no network"):
        client.fetch_page("/page.html")
