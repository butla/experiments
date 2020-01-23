import time
import random
import sys

word = sys.argv[1]

fifo = open('bla', 'wb', buffering=0)

start_time = time.time()
while start_time + 15 > time.time():
    fifo.write(f'{word}\n'.encode())
    fifo.flush()
    print('writing', word)
    time.sleep(random.random()/4)
fifo.close()
