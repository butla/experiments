import asyncio


async def some_functionality(event_waiting_for_test, event_to_signal_tests):
    event_to_signal_tests.clear()
    print('doing stuff')
    await asyncio.sleep(1)
    print('doing some more stuff')

    print('at the place we want to test')
    event_to_signal_tests.set()
    await event_waiting_for_test.wait()
    print('functional code stopped waiting, doing more stuff')
    await asyncio.sleep(1)
    print('finished doing things')


async def some_test():
    event_waiting_for_test = asyncio.Event()
    event_to_signal_tests = asyncio.Event()

    event_waiting_for_test.clear()
    print('starting test')
    real_code_run = asyncio.create_task(some_functionality(event_waiting_for_test, event_to_signal_tests))
    await event_to_signal_tests.wait()
    print('test arrived to the lock, doing stuff')
    await asyncio.sleep(1)
    print('test releasing the lock/event')
    event_waiting_for_test.set()
    await real_code_run
    print('end of test')


if __name__ == '__main__':
    asyncio.run(some_test())
