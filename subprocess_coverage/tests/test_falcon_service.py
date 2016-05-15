import os
import signal
import subprocess
import sys
import time

import requests

def test_get():
    waitress_path = os.path.join(os.path.dirname(sys.executable), 'waitress-serve')
    serv_proc = subprocess.Popen([waitress_path, 'some_code.falcon_service:app'])
    time.sleep(1)

    resp = requests.get('http://localhost:8080/')
    assert resp.text == 'some test response\n'

    serv_proc.send_signal(signal.SIGINT)
    serv_proc.wait()
