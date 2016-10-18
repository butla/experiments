#!/usr/bin/env python3
import asyncio
import random
import sys

from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FillControl
from prompt_toolkit.layout.dimension import LayoutDimension
from prompt_toolkit.shortcuts import create_asyncio_eventloop
from prompt_toolkit.token import Token


KILL_APP = 'sraka'
ASYNC_BUFFER = 'async_buffer'

loop = asyncio.get_event_loop()
manager = KeyBindingManager()
registry = manager.registry

layout = VSplit([
    Window(content=BufferControl(buffer_name=DEFAULT_BUFFER)),

    Window(width=LayoutDimension.exact(1),
           content=FillControl('*', token=Token.Line)),
    Window(width=LayoutDimension.exact(1),
           content=FillControl('|', token=Token.Line)),
    Window(width=LayoutDimension.exact(1),
           content=FillControl('*', token=Token.Line)),

    Window(content=BufferControl(buffer_name=ASYNC_BUFFER)),
])

buffers={
    DEFAULT_BUFFER: Buffer(is_multiline=True),
    ASYNC_BUFFER: Buffer(is_multiline=True),
}


@registry.add_binding(Keys.ControlC, eager=True)
def key_close(event):
    event.cli.set_return_value(KILL_APP)


eventloop = create_asyncio_eventloop()
application = Application(buffers=buffers,
                          key_bindings_registry=registry,
                          layout=layout,
                          use_alternate_screen=True)
cli = CommandLineInterface(
    application=application,
    eventloop=eventloop)


async def do_background_stuff():
    while True:
        buffers[ASYNC_BUFFER].insert_text(random.randint(1, 5) * '*' + '\n')
        cli.invalidate()
        await asyncio.sleep(1)


async def run_application():
    while True:
        try:
            result = await cli.run_async()
            if result == KILL_APP:
                return
        except (EOFError, KeyboardInterrupt):
            return


def main():
    app_task =  asyncio.ensure_future(run_application())

    background_task = asyncio.gather(do_background_stuff(), return_exceptions=True)
    loop.run_until_complete(app_task)

    background_task.cancel()
    loop.run_until_complete(background_task)

    print('Qutting event loop. Bye.')
    loop.close()


if __name__ == '__main__':
    main()
