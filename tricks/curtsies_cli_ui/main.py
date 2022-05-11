import asyncio
import random

from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, bold, green, yellow

print(yellow('this prints normally, not to the alternate screen'))


async def bla(window, array_):
    mark = '|'

    while True:
        color = random.choice([red, green, yellow])
        row = random.choice(range(window.height))
        column = random.choice(range(window.width-len(mark)))

        a[row, column:column+len(mark)] = [color(mark)]
        window.render_to_terminal(array_)

        await asyncio.sleep(random.random())


async def bla_2(window, array_):
    mark = '-'

    while True:
        color = random.choice([red, green, yellow])
        row = random.choice(range(window.height))
        column = random.choice(range(window.width-len(mark)))

        a[row, column:column+len(mark)] = [color(mark)]
        window.render_to_terminal(array_)

        await asyncio.sleep(random.random()/2)

l = asyncio.get_event_loop()

with FullscreenWindow() as window:
    with Input() as input_generator:
        a = FSArray(window.height, window.width)
        window.render_to_terminal(a)
        l.create_task(bla(window, a))
        l.create_task(bla_2(window, a))

        l.run_forever()
