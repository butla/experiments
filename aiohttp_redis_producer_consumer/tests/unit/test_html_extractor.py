from unittest.mock import MagicMock

import aiohttp
import pytest

from txodds_code_test import html_extractor


@pytest.mark.asyncio
async def test_fetch_and_queue_urls_with_http_errors(unused_tcp_port):
    dummy_redis_pool = None
    non_existant_urls = [
        f'http://localhost:{unused_tcp_port}/xxx',
        f'http://localhost:{unused_tcp_port}/yyy',
    ]

    url_fetch_results = await html_extractor._fetch_and_queue_html_for_urls(
        dummy_redis_pool, non_existant_urls)

    assert [result.url for result in url_fetch_results] == non_existant_urls
    assert all(isinstance(result.error, aiohttp.ClientError) for result in url_fetch_results)


@pytest.fixture
def mock_log(monkeypatch):
    mock_log = MagicMock()
    monkeypatch.setattr('txodds_code_test.html_extractor._log', mock_log)
    return mock_log


def test_log_results_no_errors(mock_log: MagicMock):
    results = [html_extractor._UrlFetchResult(url='http://dummy-url', error=None)]
    html_extractor._log_results(results)
    mock_log.info.assert_called()

def test_log_results_with_errors(mock_log: MagicMock):
    results = [html_extractor._UrlFetchResult(url='http://dummy-url', error=ValueError())]
    html_extractor._log_results(results)
    mock_log.info.assert_called()
    mock_log.error.assert_called()
