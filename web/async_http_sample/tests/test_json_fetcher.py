import asyncio
import json
from unittest.mock import MagicMock

import asynctest
import pytest

import json_fetcher.json_fetcher as json_fetcher


@pytest.mark.asyncio
async def test_fetch_json(monkeypatch):
    """This test is sadly way more tied to the implementation than I like.
    Because the code doesn't branch at all it could be covered only in the functional tests.

    Also, testing async context managers is still a bit tricky due to lack of a proper
    mock implementation:
    https://bugs.python.org/issue26467
    https://github.com/Martiusweb/asynctest/issues/29
    So I've worked around it.
    """
    test_json = {'a': 'b'}
    test_url = 'http://blabla'
    mock_response = asynctest.CoroutineMock()
    mock_response.json.return_value = test_json
    mock_request = asynctest.CoroutineMock(return_value=mock_response)
    monkeypatch.setattr('json_fetcher.json_fetcher.aiohttp.ClientSession._request',
                        mock_request)

    assert await json_fetcher.fetch_json(test_url) == test_json
    # check only the positional arguments
    assert ('GET', test_url) == mock_request.call_args[0]


@pytest.mark.asyncio
async def test_timed_json_fetch(monkeypatch, capsys):
    test_json = {'a': 'b'}
    mock_fetch = asynctest.CoroutineMock(return_value=test_json)
    monkeypatch.setattr('json_fetcher.json_fetcher.fetch_json', mock_fetch)
    test_url = 'http://blabla'

    await json_fetcher.timed_json_fetch(test_url)

    out, _ = capsys.readouterr()
    assert test_json == json.loads(out)
    mock_fetch.assert_called_with(test_url)


@pytest.mark.asyncio
async def test_timed_json_fetch_fail(monkeypatch, capsys):
    error_type = ValueError
    mock_fetch = asynctest.CoroutineMock(side_effect=error_type)
    monkeypatch.setattr('json_fetcher.json_fetcher.fetch_json', mock_fetch)

    with pytest.raises(error_type):
        await json_fetcher.timed_json_fetch('http://blabla')

    _, err = capsys.readouterr()
    assert 'FAILED' in err


async def _fake_asyncio_sleep(_):
    """Async sleep that doesn't wait for any period of time,
    but allows for stepping out of the coroutine."""
    loop = asyncio.get_event_loop()
    empty_task = loop.create_task(asynctest.CoroutineMock()())
    await empty_task


@pytest.mark.asyncio
async def test_show_elapsed_time(capsys, monkeypatch):
    mock_sleep = asynctest.CoroutineMock(wraps=_fake_asyncio_sleep)
    monkeypatch.setattr('json_fetcher.json_fetcher.asyncio.sleep', mock_sleep)
    monkeypatch.setattr('json_fetcher.json_fetcher.time.perf_counter',
                        MagicMock(side_effect=[0.0, 1.0, 2.0]))
    coroutine = json_fetcher._show_elapsed_time()

    # getting to the first await
    await coroutine.send(None)
    _, err = capsys.readouterr()
    assert '\r' in err and '1.0' in err

    # repeat the loop and go to await again
    await coroutine.send(None)
    assert '2.0' in capsys.readouterr()[1]

    # handling of cancellation, as the coroutine is meant to end
    asyncio.Task(coroutine).cancel()
    assert mock_sleep.called


@pytest.mark.parametrize('args, url',
[
    (['something', 'http://a'], 'http://a'),
    (['something'], json_fetcher.DEFAULT_URL),
])
def test_get_url_to_fetch(monkeypatch, args, url):
    monkeypatch.setattr('json_fetcher.json_fetcher.sys.argv', args)
    assert json_fetcher._get_url_to_fetch() == url
