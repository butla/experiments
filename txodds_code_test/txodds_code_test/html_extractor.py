"""Take URLs from the command line and puts the downloaded HTML on the queue."""

# TODO log warning when URL fails to download

import asyncio

import aioredis

async def add_stuff(redis_pool):
    async with redis_pool.get() as redis:
        queue_name = 'the_url_queue'
        await redis.lpush(queue_name, 'aaa')
        await redis.lpush(queue_name, 'bbb')
        await redis.lpush(queue_name, 'ccc')
        await redis.ltrim(queue_name, 0, 4)

        print(await redis.lrange(queue_name, 0, -1))

async def get_pool():
    return await aioredis.create_pool(('localhost', 32768))

loop = asyncio.get_event_loop()
redis_pool = loop.run_until_complete(get_pool())
loop.run_until_complete(add_stuff(redis_pool))

redis_pool.close()
loop.run_until_complete(redis_pool.wait_closed())

