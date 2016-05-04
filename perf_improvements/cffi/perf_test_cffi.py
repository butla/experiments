import time
from cffi import FFI

ffi = FFI()
ffi.cdef("int loop(int);")
ffi.set_source("_example",
"""
    static int loop(int repeats)
    {
        int x = 0;
        int i;
        for(i=0; i<repeats; i++)
        {
            x += 1;
        }
        return x;
    }
""")

ffi.compile()
from _example import lib

def loop(repeats=10000000):
    return lib.loop(repeats)

for i in range(3):
    start_time = time.time()
    loop()
    print(time.time() - start_time)
