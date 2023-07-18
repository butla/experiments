import subprocess
import sys
import requests
import time
import signal
import os
import socket

for sig in [signal.SIGINT,signal.SIGTERM,signal.SIGKILL]:
    #sp = subprocess.Popen([sys.executable, '-m', 'http.server', '--bind', '127.0.0.1', '9090'])
    sp = subprocess.Popen([sys.executable, '-m', 'SimpleHTTPServer', '9090'])
    time.sleep(1)
    r = requests.get("http://localhost:9090/")
    print(r.content)
    os.kill(sp.pid,sig)
    sp.wait()
    time.sleep(1)
    
    # test if the socket is free
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', 9090))
        print('socket is FREE')
    except Exception:
        print('socket is NOT FREE') 
