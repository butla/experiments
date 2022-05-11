"""Taken from the aiohttp documentaion http://aiohttp.readthedocs.io/en/stable/"""

import asyncio

import aiohttp
import async_timeout


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://python.org')
        print(html)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
