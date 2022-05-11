#!/usr/bin/env python3
import asyncio
import os
import random

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

# TODO add token colors!

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


WARHAMMER_QUOTES = ['A good soldier obeys without question. A good officer commands without doubt.',
'Blessed is the mind too small for doubt.',
'To admit defeat is to blaspheme against the Emperor.',
'For those who seek perfection there can be no rest on this side of the grave.',
'The difference between heresy and treachery is ignorance.',
'Knowledge is power, guard it well.',
'An open mind is like a fortress with its gates unbarred and unguarded.',
'Innocence proves nothing.',
'Success is commemorated; Failure merely remembered.',
'Even a man who has nothing can still offer his life.',
'Only in death does duty end.',
'No man died in His service that died in vain.',
'Hope is the first step on the road to disappointment.',
'There is no such thing as innocence, only degrees of guilt.',
'Beginning reform is beginning revolution.',
'Educate men without faith and you but make them clever devils.',
'Success is measured in blood; yours or your enemy´s.',
'The man who has nothing can still have faith.',
'Burn the heretic. Kill the mutant. Purge the unclean.',
'It is better to die for the Emperor than to live for yourself.',
'Fear denies faith.',
'Foolish are those who fear nothing, yet claim to know everything.',
'Brave are they who know everything yet fear nothing.',
'Happiness is a delusion of the weak.',
'All souls call out for salvation.',
"Life is the Emperor's currency, spend it well.",
'A suspicious mind is a healthy mind.',
'Cowards die in shame.',
'Faith without deeds is worthless.',
'True Happiness stems only from Duty.',
'The blood of martyrs is the seed of the Imperium.',
'Heresy grows from idleness.',
'There is only the Emperor, and he is our shield and protector.',
'Truth is Subjective.',
'Damnation is Eternal.',
'Know the Mutant; Kill the Mutant.',
'To Question is to doubt.',
'He who keeps silent consents.',
'Prayer cleanses the soul, Pain cleanses the body.',
'Death by thy Compass.',
'Zeal is its own Excuse.',
'Work earns Salvation.',
'Without him there is nothing.',
'Only the Emperor is all.',
"Hatred is the emperor's greatest gift to humanity.",
'Victory needs no explanation, defeat allows none.',
'A small mind is easily filled with faith.']

COWS = [name.replace('.cow', '') for name in os.listdir('/usr/share/cowsay/cows')]


async def do_background_stuff():
    while True:
        # buffers[ASYNC_BUFFER].insert_text(random.randint(1, 5) * '*' + '\n')
        proc = await asyncio.create_subprocess_exec(
            'cowsay', '-f', random.choice(COWS), random.choice(WARHAMMER_QUOTES),
            stdout=asyncio.subprocess.PIPE)

        # Read one line of output
        data = await proc.stdout.read()
        text = data.decode()
        buffers[ASYNC_BUFFER].text = text

        await proc.wait()

        cli.invalidate()
        await asyncio.sleep(5)


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
