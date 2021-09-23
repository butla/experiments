"""
Old script that I was using to calculate how much time I spent on a task based on my notes.
"""

import functools
import re
from datetime import datetime

MATCH_ABSOLUTE_TIME = r'(?P<time>\d\d?:\d\d)'
MATCH_TIME_RANGE = r'(?P<start_time>\d\d?:\d\d)\s?-\s?(?P<end_time>\d\d?:\d\d)'
TIME_MATCH = MATCH_TIME_RANGE + '|' + MATCH_ABSOLUTE_TIME

TIME_ZERO = datetime.strptime('0', '%H')
ONE_DAY_DELTA = datetime.strptime('2', '%d') - TIME_ZERO


def calculate_entire_time(time_ranges: str) -> str:
    def date_from_hour_string(hour_string):
        return datetime.strptime(hour_string, '%H:%M')

    time_deltas = []

    for match in re.finditer(TIME_MATCH, time_ranges):
        if match.group('time'):
            time_delta = date_from_hour_string(match.group('time')) - TIME_ZERO
            time_deltas.append(time_delta)
        else:
            start_time = date_from_hour_string(match.group('start_time'))
            end_time = date_from_hour_string(match.group('end_time'))
            if end_time > start_time:
                time_deltas.append(end_time - start_time)
            else:
                time_deltas.append((end_time - start_time) + ONE_DAY_DELTA)

    overall_timedelta = functools.reduce(lambda x, y: x+y, time_deltas)
    return str(overall_timedelta)

if __name__ == '__main__':
    import sys

    print(calculate_entire_time(' '.join(sys.argv[1:])))
