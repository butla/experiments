"""
A Redis-based queue for the HTML payloads.

I'm aware of the rq project (http://python-rq.org/), but's it's more of a job queue.
"""

import aioredis

# So the queue doesn't get too long. I haven't thought long about this number,
# it's just to show queue size limiting.
QUEUE_LENGTH = 1000

QUEUE_NAME = 'html_queue'


# class RedisHtmlQueue:
#     """
#     A Redis-based queue for the HTML payloads.
#
#     I'm aware of the rq project (http://python-rq.org/), but's it's more of a job queue.
#     """
#
#     def __init__(self,
#                  redis_host: str,
#                  redis_port: int,
#                  queue_length: int = 1000,
#                  queue_name: str = 'html_queue'):
#         # So the queue doesn't get too long. I haven't thought long about this number,
#         # it's just to show queue size limiting.
#         self.queue_length = queue_length
#         self.queue_name = queue_name
#         self._redis_host = redis_host
#         self._redis_port = redis_port
#         self._redis_pool = None
#
#         self._log = logging.getLogger(self.__class__.__name__)
#
#     async def __aenter__(self):
#         self._log.info('Creating a pool of connections to Redis at %s:%d.',
#                        self._redis_host, self._redis_port)
#     redis_pool = await aioredis.create_pool((redis_host, redis_port))
#
#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         pass

async def push(redis_pool: aioredis.RedisPool,
               payload: str,
               max_length: int = QUEUE_LENGTH):
    """Push a payload onto the queue.
    """
    async with redis_pool.get() as redis_client:
        await redis_client.lpush(QUEUE_NAME, payload)
        await redis_client.ltrim(QUEUE_NAME, 0, max_length-1)


async def pop(redis_pool: aioredis.RedisPool) -> str:
    """Pop payload from the queue.

    For the application to be truly robust we should use RPOPLPUSH
    (https://redis.io/commands/rpoplpush), not just RPOP.
    But that would require a subsystem that would monitor the secondary queue for items that were
    being processed for too long (probably, because the worker handling them have crashed),
    and that's just too much work for this simple demo, in my opinion.
    """
    async with redis_pool.get() as redis_client:
        payload = await redis_client.rpop(QUEUE_NAME)
        return payload.decode()
