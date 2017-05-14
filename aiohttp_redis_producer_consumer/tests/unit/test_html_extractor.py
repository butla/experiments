from unittest.mock import MagicMock

import aiohttp
import pytest

from txodds_code_test import html_extractor


# class _StubClientSessionGetMethod:
#     """A base class for stubbing (mocking, to be less precise) ClientSession's get() method.
#
#     Sadly, there's no class for mocking async context managers yet
#     https://github.com/Martiusweb/asynctest/issues/29
#     and no specific solution for mocking the client session
#     https://github.com/aio-libs/aiohttp/issues/1704
#     """
#     def __init__(self, _):
#         pass
#
#     async def __aenter__(self):
#         pass
#
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         pass
#
#
# def _get_stubbed_client_session(get_implementation_class):
#     mock_session = MagicMock()
#     mock_session.get = get_implementation_class
#     return mock_session
#
#
# @pytest.mark.asyncio
# async def test_fetch_url_timeout():
#     class GetWithTimeout(_StubClientSessionGetMethod):
#         async def __aenter__(self):
#             await asyncio.sleep(5)
#     mock_session = _get_stubbed_client_session(GetWithTimeout)
#
#     with pytest.raises(asyncio.TimeoutError):
#         await html_extractor._fetch_url('http://some-fake-url', mock_session, 0.000001)
#
#
# @pytest.mark.asyncio
# async def test_fetch_url_non_200():
#     class GetWith400Response(_StubClientSessionGetMethod):
#         async def __aenter__(self):
#             mock_response = MagicMock()
#             mock_response.raise_for_status.side_effect = aiohttp.ClientResponseError
#             return mock_response
#     mock_session = _get_stubbed_client_session(GetWith400Response)
#
#     with pytest.raises(aiohttp.ClientResponseError):
#         await html_extractor._fetch_url('http://some-fake-url', mock_session)


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
