import asyncio

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
    dummy_payload = 'something'
    await redis_queue.push(redis_pool, dummy_payload)
    async with redis_pool.get() as redis_client:
        assert await redis_client.lpop(redis_queue.QUEUE_NAME) == dummy_payload.encode()


@pytest.mark.asyncio
async def test_pop_from_queue(redis_pool):
    dummy_payload = 'something'
    async with redis_pool.get() as redis_client:
        assert await redis_client.lpush(redis_queue.QUEUE_NAME, dummy_payload)
    assert await redis_queue.pop(redis_pool) == dummy_payload


@pytest.mark.asyncio
async def test_push_to_queue_over_the_limit(redis_pool):
    dummy_payloads = ['xxx', 'yyy', 'zzz']
    for payload in dummy_payloads:
        await redis_queue.push(redis_pool, payload, max_length=2)
    async with redis_pool.get() as redis_client:
        proper_final_payloads = [b'zzz', b'yyy']
        assert await redis_client.lrange(redis_queue.QUEUE_NAME, 0, -1) == proper_final_payloads
