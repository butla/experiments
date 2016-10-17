#!/usr/bin/env python
"""
(Python >= 3.5)
This is an example of how to embed a CommandLineInterface inside an application
that uses the asyncio eventloop. The ``prompt_toolkit`` library will make sure
that when other coroutines are writing to stdout, they write above the prompt,
not destroying the input line.
This example does several things:
    1. It starts a simple coroutine, printing a counter to stdout every second.
    2. It starts a simple input/echo cli loop which reads from stdin.
Very important is the following patch. If you are passing stdin by reference to
other parts of the code, make sure that this patch is applied as early as
possible. ::
    sys.stdout = cli.stdout_proxy()
"""

from prompt_toolkit.application import Application
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import TokenListControl
from prompt_toolkit.shortcuts import create_asyncio_eventloop
from prompt_toolkit.token import Token

import asyncio
import sys


async def print_counter():
    """
    Coroutine that prints counters.
    """
    i = 0
    while True:
        print('Counter: %i' % i)
        i += 1
        await asyncio.sleep(2)

KILL_APP = 'sraka'

loop = asyncio.get_event_loop()
manager = KeyBindingManager()
registry = manager.registry

layout = Window(content=TokenListControl(
        get_tokens=lambda cli: [(Token, 'Hello world')]))


@registry.add_binding(Keys.ControlC, eager=True)
def key_close(event):
    event.cli.set_return_value(KILL_APP)


async def run_application():
    eventloop = create_asyncio_eventloop()

    application = Application(key_bindings_registry=registry,
                              layout=layout)

    cli = CommandLineInterface(
        application=application,
        eventloop=eventloop)

    sys.stdout = cli.stdout_proxy()

    while True:
        try:
            result = await cli.run_async()
            if result == KILL_APP:
                return
        except (EOFError, KeyboardInterrupt):
            return


def main():
    app_task =  asyncio.ensure_future(run_application())

    background_task = asyncio.gather(print_counter(), return_exceptions=True)
    loop.run_until_complete(app_task)

    background_task.cancel()
    loop.run_until_complete(background_task)

    print('Qutting event loop. Bye.')
    loop.close()


if __name__ == '__main__':
    main()
