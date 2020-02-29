# ran on python3.8
import asyncio
import random


async def kill_myself_but_finish_the_job():
    while True:
        print('doing stuff...')
        await asyncio.sleep(0.01)
        print('done')
        if random.random() < 0.2:
            asyncio.current_task().cancel()


async def kill_loop_when_task_ends(task_to_watch):
    print('Waiting for a task to finish before I kill the whole loop.')
    try:
        await task_to_watch
    except asyncio.CancelledError:
        print('The other task got cancelled.')
    asyncio.get_event_loop().stop()


loop = asyncio.get_event_loop()

task = loop.create_task(kill_myself_but_finish_the_job())
loop.create_task(kill_loop_when_task_ends(task))

loop.run_forever()
print('Exited the loop')
