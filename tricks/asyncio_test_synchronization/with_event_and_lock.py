import asyncio


async def some_functionality(lock, event):
    event.clear()
    print('doing stuff')
    await asyncio.sleep(1)
    print('doing some more stuff')

    print('at the place we want to test')
    event.set()
    async with lock:
        print('functional code took the lock, doing more stuff')
        await asyncio.sleep(1)
        print('finished doing things')


async def some_test():
    lock = asyncio.Lock()
    event = asyncio.Event()

    async with lock:
        print('starting test')
        real_code_run = asyncio.create_task(some_functionality(lock, event))
        await event.wait()
        print('test arrived to the lock, doing stuff')
        await asyncio.sleep(1)
        print('test releasing the lock')
    await real_code_run
    print('end of test')


if __name__ == '__main__':
    asyncio.run(some_test())
