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

    fifo = FIFO_PATH.open('rb', buffering=0)

    print('Reading from', FIFO_PATH, flush=True)
    while True:
        # TODO wait for ready for reading
        time.sleep(0.2)
        print(fifo.readline().decode(), flush=True)
    # for line in fifo.readlines():
    #     print(line, flush=True)


if __name__ == '__main__':
    run_receiver()
