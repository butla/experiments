import asyncio
from unittest.mock import MagicMock

import aiohttp
import pytest

from txodds_code_test import html_extractor


@pytest.mark.asyncio
async def test_fetch_url_timeout():
    # Sadly, there's no class for mocking async context managers yet
    # https://github.com/Martiusweb/asynctest/issues/29
    class TimeoutingSessionGet:
        def __init__(self, _):
            pass

        async def __aenter__(self):
            await asyncio.sleep(5)

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    mock_session = MagicMock()
    mock_session.get = TimeoutingSessionGet

    with pytest.raises(asyncio.TimeoutError):
        await html_extractor._fetch_url('http://some-fake-url', mock_session, 0.000001)

# @pytest.mark.asyncio
# async def test_fetch_json(monkeypatch):
#     """This test is sadly way more tied to the implementation than I like.
#     Because the code doesn't branch at all it could be covered only in the functional tests.
#
#     Also, testing async context managers is still a bit tricky due to lack of a proper
#     mock implementation:
#     https://bugs.python.org/issue26467
#     https://github.com/Martiusweb/asynctest/issues/29
#     So I've worked around it.
#     """
#     test_json = {'a': 'b'}
#     test_url = 'http://blabla'
#     mock_response = asynctest.CoroutineMock()
#     mock_response.json.return_value = test_json
#     mock_request = asynctest.CoroutineMock(return_value=mock_response)
#     monkeypatch.setattr('json_fetcher.json_fetcher.aiohttp.ClientSession._request',
#                         mock_request)
#
#     assert await json_fetcher.fetch_json(test_url) == test_json
#     # check only the positional arguments
#     assert ('GET', test_url) == mock_request.call_args[0]
