import asyncio
from unittest.mock import MagicMock

import aiohttp
import pytest

from txodds_code_test import html_extractor


class _StubClientSessionGetMethod:
    """A base class for stubbing (mocking, to be less precise) ClientSession's get() method.
     
    Sadly, there's no class for mocking async context managers yet
    https://github.com/Martiusweb/asynctest/issues/29
    and no specific solution for mocking the client session
    https://github.com/aio-libs/aiohttp/issues/1704
    """
    def __init__(self, _):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


def _get_stubbed_client_session(get_implementation_class):
    mock_session = MagicMock()
    mock_session.get = get_implementation_class
    return mock_session


@pytest.mark.asyncio
async def test_fetch_url_timeout():
    class TimeoutingSessionGet(_StubClientSessionGetMethod):
        async def __aenter__(self):
            await asyncio.sleep(5)
    mock_session = _get_stubbed_client_session(TimeoutingSessionGet)

    with pytest.raises(asyncio.TimeoutError):
        await html_extractor._fetch_url('http://some-fake-url', mock_session, 0.000001)


@pytest.mark.asyncio
async def test_fetch_url_non_200():
    class SessionGetWith400Response(_StubClientSessionGetMethod):
        async def __aenter__(self):
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = aiohttp.ClientResponseError
            return mock_response
    mock_session = _get_stubbed_client_session(SessionGetWith400Response)

    with pytest.raises(aiohttp.ClientResponseError):
        await html_extractor._fetch_url('http://some-fake-url', mock_session)
