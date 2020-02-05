# ran with python 3.8.1
import asyncio
import contextvars
import time

DEFAULT = 'default'
CHANGED = 'changed'
test_var = contextvars.ContextVar('test_var', default=DEFAULT)


async def main():
    asyncio.create_task(task1())
    asyncio.create_task(task2())
    print('created the tasks')


async def task1():
    print('running task 1')
    test_var.set(CHANGED)
    asyncio.create_task(task1_child())

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, synchronous_task)


async def task1_child():
    assert test_var.get() == CHANGED
    print('task 1 child successful')


async def task2():
    print('running task 2')
    await asyncio.sleep(2)
    assert test_var.get() == DEFAULT
    print('task 2 success')


def synchronous_task():
    # sad that the context vars don't get propagated when doing run_in_executor
    assert test_var.get() == DEFAULT
    print("synchronous task success")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
