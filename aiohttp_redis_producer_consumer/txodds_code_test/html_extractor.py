"""
The producer's code.
It takes URLs from the command line and puts the HTML behind them on the queue.
"""

# TODO log warning when URL fails to download

import argparse
import asyncio
import logging
from typing import Iterable

import aiohttp
import aioredis
import async_timeout
import uvloop

HTML_QUEUE_NAME = 'html_queue'

_log = logging.getLogger(__name__)


# async def add_stuff(redis_pool):
#     async with redis_pool.get() as redis:
#         await redis.lpush(HTML_QUEUE_NAME, 'aaa')
#         await redis.lpush(HTML_QUEUE_NAME, 'bbb')
#         await redis.lpush(HTML_QUEUE_NAME, 'ccc')
#         await redis.ltrim(HTML_QUEUE_NAME, 0, 4)
#
#         print(await redis.lrange(HTML_QUEUE_NAME, 0, -1))
#
#
# async def get_url(redis_client):
#     async with aiohttp.ClientSession() as session:
#         # TODO check timeout or not 200 response
#         with async_timeout.timeout(10):
#             async with session.get('http://python.org') as response:
#                 html = await response.text()
#                 await redis_client.lpush(HTML_QUEUE_NAME, html)
#                 print(await redis_client.lrange(HTML_QUEUE_NAME, 0, -1))


async def _fetch_url(url: str, session: aiohttp.ClientSession, timeout: float = 10.0):
    with async_timeout.timeout(timeout):
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()


async def _fetch_and_queue_html(
        url: str,
        session: aiohttp.ClientSession,
        redis_pool: aioredis.RedisPool):
    # TODO catch exceptions here: timeout, not 200; log them
    # TODO log error if not 200 aiohttp.ClientResponseError
    html = await _fetch_url(url, session)
    # TODO this should be a separate function (maybe of a class)
    async with redis_pool.get() as redis_client:
        await redis_client.lpush(HTML_QUEUE_NAME, html)
        await redis_client.ltrim(HTML_QUEUE_NAME, 0, 4)


async def _fetch_urls_and_queue_html(urls: Iterable[str], redis_pool: aioredis.RedisPool):
    # TODO make docstring better
    """Some may fail, they will be logged
    """
    async with aiohttp.ClientSession() as session:
        fetch_futures = [_fetch_and_queue_html(url, session, redis_pool)
                         for url in urls]
        # TODO test that exceptions are handled
        await asyncio.gather(*fetch_futures, return_exceptions=True)


async def produce_html_on_queue(
        redis_host: str,
        redis_port: int,
        urls: Iterable[str]):
    """Extracts HTML for each of the given URLs and puts it on a Redis queue.
    """
    _log.info('Creating a pool of connections to Redis at %s:%d.', redis_host, redis_port)
    redis_pool = await aioredis.create_pool((redis_host, redis_port))

    _log.info('Fetching HTML from urls: %s', ', '.join(urls))
    await _fetch_urls_and_queue_html(urls, redis_pool)

    _log.info('Closing...')
    redis_pool.close()
    await redis_pool.wait_closed()


def _create_cli_parser():
    parser = argparse.ArgumentParser(
        description='Get the HTML behind the given URLs and put it on a Redis queue.')
    parser.add_argument('redis_host', metavar='REDIS_HOST', type=str,
                        help='IP address or hostname of a Redis instance.')
    parser.add_argument('redis_port', metavar='REDIS_PORT', type=int,
                        help='Port of a Redis instance on the given address.')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='URLs from which HTML will be fetched.')
    return parser


def main():
    """Run the HTML extractor (the producer). 
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s')
    # for free speed-up on CPython
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    args = _create_cli_parser().parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        produce_html_on_queue(args.redis_host, args.redis_port, args.urls))


if __name__ == '__main__':
    main()
