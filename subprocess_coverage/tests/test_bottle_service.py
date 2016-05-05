import signal
import subprocess
import sys
import time

import requests

def test_get():
    serv_proc = subprocess.Popen([sys.executable, 'some_code/bottle_service.py'])
    time.sleep(1)
    
    resp = requests.get('http://localhost:8080/')
    assert resp.text == 'Just some text.'

    #serv_proc.terminate()
    serv_proc.send_signal(signal.SIGINT)
    serv_proc.wait()
