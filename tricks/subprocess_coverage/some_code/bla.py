import os
import subprocess
import sys

if 'a' in sys.argv:
    print('jestem nowym')
else:
    print('odpalam nowy')
    proc = subprocess.Popen([sys.executable, __file__, 'a'])
    proc.wait()

print(os.environ.get('COVERAGE_PROCESS_START', 'nothing'))

#def sraka():
#    print('nie ttafisz')

