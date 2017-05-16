"""
The consumer's code.
It takes HTML from the queue and outputs the URIs found in it.
"""

import asyncio
import json
import logging
from typing import List
from urllib.parse import urljoin

import aioredis
from bs4 import BeautifulSoup

from . import app_cli, redis_queue


_log = logging.getLogger('url_extractor')


def _scrape_urls(html: str, base_url: str) -> List[str]:
    """Gets all valid links from a site and returns them as URIs (some links may be relative.

    If the URIs scraped here would go back into the system to have more URIs scraped from their
    HTML, we would need to filter out all those who are not HTTP or HTTPS.
    Also, assuming that many consumers and many producers would be running at the same time,
    connected to one Redis instance, we would need to cache normalized versions or visited URIs
    without fragments (https://tools.ietf.org/html/rfc3986#section-3.5) so we don't fall into loops.
    For example two sites referencing each other.
    The cached entries could have time-to-live (Redis EXPIRE command), so we could refresh our
    knowledge about a site eventually.
    """
    soup = BeautifulSoup(html, 'html.parser')
    href = 'href'
    return [urljoin(base_url, link.get(href))
            for link in soup.find_all('a') if link.has_attr(href)]


async def _scrape_urls_from_queued_html(redis_host: str, redis_port: int):
    _log.info('Creating a pool of connections to Redis at %s:%d.', redis_host, redis_port)
    redis_pool = await aioredis.create_pool((redis_host, redis_port))
    _log.info('Processing HTML from queue...')
    while True:
        try:
            html_payload = await redis_queue.pop(redis_pool)

            _log.info('Processing HTML from URL %s', html_payload.url)
            scraped_urls = _scrape_urls(html_payload.html, html_payload.url)
            _log.info('Scraped URIs from URL %s', html_payload.url)

            output_json = {html_payload.url: scraped_urls}
            print(json.dumps(output_json))
        except redis_queue.QueueEmptyError:
            # wait for work to become available
            await asyncio.sleep(1)
    # not closing the redis pool since the process needs to be terminated to stop anyway


def main():
    """Run the URL extractor (the consumer).
    """
    app_cli.setup_logging()
    args_parser = app_cli.get_redis_args_parser(
        'Start a worker that will get URL/HTML pairs from a Redis queue and for each of those '
        'pairs output (on separate lines) a JSON in format {ORIGINATING_URL: [FOUND_URLS_LIST]}')
    args = args_parser.parse_args()

    loop = app_cli.get_event_loop()
    loop.run_until_complete(
        _scrape_urls_from_queued_html(args.redis_host, args.redis_port))


if __name__ == '__main__':
    main()
