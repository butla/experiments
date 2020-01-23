import time
import random
import sys

import receiver


def run_writer():
    word = sys.argv[1]

    fifo = open(receiver.FIFO_PATH, 'wb', buffering=0)

    start_time = time.time()
    while start_time + 15 > time.time():
        fifo.write(f'{word}\n'.encode())
        fifo.flush()
        print('writing', word, flush=True)
        time.sleep(random.random()/4)
    fifo.close()


if __name__ == '__main__':
    run_writer()
