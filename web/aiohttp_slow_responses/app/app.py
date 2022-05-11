import asyncio
import logging
import random

from aiohttp import web


async def slow_response(request: web.Request):
    response = web.StreamResponse()
    await response.prepare(request)

    async for response_chunk in _create_content():
        await response.write(response_chunk)
        await response.write(b'\n')
    return response


async def _create_content():
    interval = random.gauss(0.2, 0.1)
    for number in range(10000):
        await asyncio.sleep(interval)
        yield f'Interval: {interval:.2} | iteration: {number}'.encode()


def create_app():
    app = web.Application()
    app.add_routes([
        web.get('/', slow_response),
    ])
    return app


def run_app():
    logging.basicConfig(level=logging.INFO)
    web.run_app(
        create_app(),
        port=8000,
    )


if __name__ == '__main__':
    run_app()
