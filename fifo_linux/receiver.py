import os
import time

fifo_path = 'my_fifo'
os.unlink(fifo_path)
os.mkfifo(fifo_path)
fifo = open(fifo_path, 'rb', buffering=0)

start_time = time.time()
while start_time + 60 > time.time():
    # TODO wait for there to be something?
    print(fifo.readline(), flush=True)
