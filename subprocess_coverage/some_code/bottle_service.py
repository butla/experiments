import signal
import subprocess
import sys

from bottle import route, run

@route('/')
def example():
    return 'Just some text.'

def sig_handler(*_):
    print('Caught the signal.')
    sys.exit(0)

signal.signal(signal.SIGTERM, sig_handler)

run(port=8080)
