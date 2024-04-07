import asyncio
import string
import random


async def run_demo_with_random_tasks() -> None:
    queue = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(task_producer(queue))
        for _ in range(2):
            tg.create_task(task_consumer(queue))
        await asyncio.sleep(1)
        print('waiting for queue clear')
        await queue.join()
        print('queue cleared!')


async def task_consumer(queue: asyncio.Queue) -> None:
    while True:
        received_value = await queue.get()
        print(received_value, "- processing...")
        await asyncio.sleep(0.5)

        if random.random() < 0.3:
            print(f"{received_value} - oh noes, I crashed! - returning item to queue")
            await queue.put(received_value)
            continue
        # This probably doesn't affect anything other than join
        queue.task_done()


async def task_producer(queue: asyncio.Queue) -> None:
    for letter in string.ascii_uppercase[:10]:
        await queue.put(letter)


if __name__ == '__main__':
    asyncio.run(run_demo_with_random_tasks())
