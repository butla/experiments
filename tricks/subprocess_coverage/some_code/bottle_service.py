import signal
import subprocess
import sys

from bottle import route, run

@route('/')
def example():
    return 'Just some text.'

# this would be needed if the tests closed the service with SIGTERM instead of SIGINT
#def sig_handler(*_):
#    print('Caught the signal.')
#    sys.exit(0)
#
#signal.signal(signal.SIGTERM, sig_handler)

run(port=8080)
