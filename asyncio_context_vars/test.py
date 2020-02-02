# TODO make coroutine call and a task and check if they inherit the vars
import asyncio
import contextvars

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


async def task1_child():
    assert test_var.get() == CHANGED
    print('task 1 child successful')


async def task2():
    print('running task 2')
    await asyncio.sleep(2)
    assert test_var.get() == DEFAULT
    print('task 2 success')



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
