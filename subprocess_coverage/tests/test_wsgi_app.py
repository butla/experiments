import os
import signal
import subprocess
import sys
import time

import requests


def test_waitress_get():
    waitress_path = os.path.join(os.path.dirname(sys.executable), 'waitress-serve')
    _test_service([waitress_path, 'some_code.falcon_service:app'])


def test_gunicorn_get():
    gunicorn_path = os.path.join(os.path.dirname(sys.executable), 'gunicorn')
    _test_service([gunicorn_path, 'some_code.falcon_service:app', '--bind', ':8080'])


def test_uwsgi_get():
    uwsgi_path = os.path.join(os.path.dirname(sys.executable), 'uwsgi')
    _test_service([uwsgi_path, '--module', 'some_code.falcon_service:app', '--http-socket', ':8080'])


def _test_service(service_process_command):
    serv_proc = subprocess.Popen(service_process_command)
    time.sleep(1)

    resp = requests.get('http://localhost:8080/')
    assert resp.text == 'some test response\n'

    serv_proc.send_signal(signal.SIGINT)
    serv_proc.wait()

