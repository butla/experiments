import asyncio
import json
import sys
import time

import aiohttp


async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        # no timeout on purpose
        async with session.get(url) as response:
            return await response.json()


async def _show_elapsed_time():
    start_time = time.perf_counter()
    while True:
        current_time = time.perf_counter() - start_time
        print('\rRequest time: {:.2f} seconds.'.format(current_time),
              end='', file=sys.stderr)
        try:
            # take the measurement every 1/100 of a second
            await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            break


async def timed_json_fetch(url):
    print('Fetching JSON from', url, file=sys.stderr)
    loop = asyncio.get_event_loop()
    timer_task = loop.create_task(_show_elapsed_time())

    try:
        fetched_json = await fetch_json(url)
        formatted_json = json.dumps(fetched_json, indent=4)
        # only the JSON document goes on standard output, for easy use in scripting
        print('\n\r', formatted_json, sep='')
    except Exception:
        print('\nFAILED to fetch the JSON!', file=sys.stderr)
        raise
    finally:
        timer_task.cancel()


DEFAULT_URL = 'https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8'


def _get_url_to_fetch():
    """URL can be provided as a parameter."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return DEFAULT_URL


if __name__ == '__main__':
    url = _get_url_to_fetch()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(timed_json_fetch(url))
