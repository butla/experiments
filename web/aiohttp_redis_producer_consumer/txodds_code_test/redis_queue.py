"""
A Redis-based queue for the HTML payloads.

I'm aware of the rq project (http://python-rq.org/), but's it's more of a job queue.
"""

import json
import typing

import aioredis

# So the queue doesn't get too long. I haven't thought long about this number,
# it's just to show queue size limiting.
QUEUE_LENGTH = 1000

QUEUE_NAME = 'html_queue'


class HtmlPayload(typing.NamedTuple):
    """
    A HTML payload and the URL it originated from.
    """
    url: str
    html: str


async def push(redis_pool: aioredis.RedisPool,
               originating_url: str,
               html: str,
               max_length: int = QUEUE_LENGTH):
    """Push a payload onto the queue.
    """
    async with redis_pool.get() as redis_client:
        payload = HtmlPayload(url=originating_url, html=html)
        await redis_client.lpush(QUEUE_NAME, json.dumps(payload))
        await redis_client.ltrim(QUEUE_NAME, 0, max_length-1)


class QueueEmptyError(Exception):
    """
    When attempting to pop from an empty Redis queue.
    """


async def pop(redis_pool: aioredis.RedisPool) -> HtmlPayload:
    """Pop payload from the queue.

    For the application to be truly robust we should use RPOPLPUSH
    (https://redis.io/commands/rpoplpush), not just RPOP.
    But that would require a subsystem that would monitor the secondary queue for items that were
    being processed for too long (probably, because the worker handling them have crashed),
    and that's just too much work for this simple demo, in my opinion.
    """
    async with redis_pool.get() as redis_client:
        payload = await redis_client.rpop(QUEUE_NAME)
        if payload:
            payload_json = json.loads(payload.decode())
            return HtmlPayload(*payload_json)
        else:
            raise QueueEmptyError()
