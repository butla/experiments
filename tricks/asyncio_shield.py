import asyncio

async def main():
    task_to_cancel = asyncio.create_task(inner())
    asyncio.create_task(canceller(task_to_cancel))
    try:
        await task_to_cancel
    except asyncio.CancelledError:
        print('task was cancelled')

    # wait for shielded task to finish
    all_tasks = asyncio.all_tasks()
    await asyncio.gather(*all_tasks - {asyncio.current_task()})

    print('finito')

async def canceller(task):
    await asyncio.sleep(1)
    print('cancelling')
    task.cancel()

async def inner():
    await asyncio.shield(shielded())
    print("This shouldn't be printed")

async def shielded():
    print('A')
    await asyncio.sleep(1)
    print('B')
    await asyncio.sleep(1)
    print('C')

asyncio.run(main())
