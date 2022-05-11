import asyncio
import json

import aioredis
import pytest

from txodds_code_test import redis_queue


@pytest.fixture
def redis_pool(event_loop: asyncio.AbstractEventLoop, redis_port: int):
    redis_pool = event_loop.run_until_complete(
        aioredis.create_pool(('localhost', redis_port)))
    yield redis_pool
    redis_pool.close()
    event_loop.run_until_complete(redis_pool.wait_closed())


@pytest.mark.asyncio
async def test_push_to_queue(redis_pool):
    dummy_html = 'something'
    url = 'http://exmple.com'

    await redis_queue.push(redis_pool, url, dummy_html)

    async with redis_pool.get() as redis_client:
        saved_payload = await redis_client.lpop(redis_queue.QUEUE_NAME)
        assert json.loads(saved_payload.decode()) == [url, dummy_html]


@pytest.mark.asyncio
async def test_push_to_queue_over_the_limit(redis_pool):
    dummys = ['xxx', 'yyy', 'zzz']

    for dummy in dummys:
        await redis_queue.push(redis_pool, dummy, dummy, max_length=2)

    async with redis_pool.get() as redis_client:
        saved_payloads = await redis_client.lrange(redis_queue.QUEUE_NAME, 0, -1)
        proper_saved_payloads = [b'["zzz", "zzz"]', b'["yyy", "yyy"]']
        assert saved_payloads == proper_saved_payloads


@pytest.mark.asyncio
async def test_pop_from_queue(redis_pool):
    payload = redis_queue.HtmlPayload('dummy-url', 'dummy-html')
    async with redis_pool.get() as redis_client:
        assert await redis_client.lpush(redis_queue.QUEUE_NAME, json.dumps(payload))

    assert await redis_queue.pop(redis_pool) == payload


@pytest.mark.asyncio
async def test_process_queues_html_from_emtpty_queue(redis_pool):
    with pytest.raises(redis_queue.QueueEmptyError):
        assert await redis_queue.pop(redis_pool)
