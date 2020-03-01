#!/usr/bin/env python
import sys

from prompt_toolkit.input.vt100 import raw_mode
from prompt_toolkit.input.vt100_parser import Vt100Parser
from prompt_toolkit.key_binding.key_processor import KeyPress


CAPTURE_FILE = 'captured_keys.txt'


def callback(key: KeyPress):
    with open(CAPTURE_FILE, 'a') as f:
        if key.key in ('c-d', 'c-c'):
            print('Stuff is saved to', CAPTURE_FILE, 'See ya!')
            sys.exit()
        f.write(key.key)
        f.write('\n')


def main():
    print('Saving typed keys...')
    print('Press ctrl+d or ctrl+c to quit.')
    stream = Vt100Parser(callback)

    with raw_mode(sys.stdin.fileno()):
        while True:
            c = sys.stdin.read(1)
            stream.feed(c)


if __name__ == '__main__':
    main()
