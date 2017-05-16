"""
The producer's code.
It takes URLs from the command line and puts the HTML behind them on the queue.
"""

import asyncio
import logging
import traceback
import typing
from typing import Iterable, List

import aiohttp
import aioredis
import async_timeout

from . import app_cli, redis_queue

_log = logging.getLogger('html_extractor')


async def _fetch_url(
        url: str,
        session: aiohttp.ClientSession,
        timeout: float = 10.0) -> str:
    with async_timeout.timeout(timeout):
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()


async def _fetch_and_queue_html(
        url: str,
        session: aiohttp.ClientSession,
        redis_pool: aioredis.RedisPool):
    _log.debug('Fetching %s...', url)
    html = await _fetch_url(url, session)
    _log.debug('Putting the HTML behind %s on the queue...', url)
    await redis_queue.push(redis_pool, url, html)
    _log.info('HTML from %s successfully put on the queue.', url)


class _UrlFetchResult(typing.NamedTuple):
    """
    A result of a single URL fetch. If it was successful, error will be None.
    """
    url: str
    error: Exception


async def _fetch_and_queue_html_for_urls(
        redis_pool: aioredis.RedisPool,
        urls: Iterable[str]) -> List[_UrlFetchResult]:
    async with aiohttp.ClientSession() as session:
        fetch_futures = [_fetch_and_queue_html(url, session, redis_pool)
                         for url in urls]
        results = await asyncio.gather(*fetch_futures, return_exceptions=True)
    return [_UrlFetchResult(url, error) for url, error in zip(urls, results)]


def _log_results(url_fetch_results: Iterable[_UrlFetchResult]):
    all_fetches = len(url_fetch_results)
    bad_fetches = [result for result in url_fetch_results if result.error]
    _log.info('%s out of %s fetches were successful', all_fetches - len(bad_fetches), all_fetches)
    if bad_fetches:
        _log.error('Failed to fetch and queue HTML for urls: %s',
                   ', '.join(result.url for result in bad_fetches))
        for bad_fetch in bad_fetches:
            err = bad_fetch.error
            _log.error('URL %s fetch failure:\n%s',
                       bad_fetch.url,
                       traceback.format_exception(type(err), err, err.__traceback__))


async def produce_html_on_queue(
        redis_host: str,
        redis_port: int,
        urls: Iterable[str]):
    """Extracts HTML for each of the given URLs and puts it on a Redis queue.
    """
    _log.info('Creating a pool of connections to Redis at %s:%d.', redis_host, redis_port)
    redis_pool = await aioredis.create_pool((redis_host, redis_port))

    _log.info('Fetching HTML from urls: %s', ', '.join(urls))
    url_fetch_results = await _fetch_and_queue_html_for_urls(redis_pool, urls)
    _log_results(url_fetch_results)

    _log.info('Closing redis connection pool...')
    redis_pool.close()
    await redis_pool.wait_closed()


def main():
    """Run the HTML extractor (the producer).
    """
    app_cli.setup_logging()
    args_parser = app_cli.get_redis_args_parser(
        'Get the HTML behind the given URLs and put it on a Redis queue.')
    args_parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                             help='URLs from which HTML will be fetched.')
    args = args_parser.parse_args()

    loop = app_cli.get_event_loop()
    loop.run_until_complete(
        produce_html_on_queue(args.redis_host, args.redis_port, args.urls))


if __name__ == '__main__':
    main()
