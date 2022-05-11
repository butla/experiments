import time
import os
from pathlib import Path

FIFO_PATH = Path('my_fifo')


def run_receiver():
    if FIFO_PATH.exists():
        FIFO_PATH.unlink()
        print('Removing old', FIFO_PATH)

    os.mkfifo(FIFO_PATH)
    print('Creating', FIFO_PATH)

    while True:
        # fifo = FIFO_PATH.open('rb', buffering=0)
        fifo = FIFO_PATH.open('r')
        print('Reading from', FIFO_PATH, flush=True)

        for line in fifo:
            print(line, flush=True, end='')
        # for line in fifo.readlines():
        #     print(line, flush=True)


if __name__ == '__main__':
    run_receiver()
