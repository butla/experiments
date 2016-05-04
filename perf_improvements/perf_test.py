import time

def loop(repeats=10000000):
    x = 0
    for i in range(repeats):
        x += 1
    return x

for i in range(3):
    start_time = time.time()
    loop()
    print(time.time() - start_time)
