"""
Functions for working with AWS ALB log files downloaded from S3.
"""

import datetime
import gzip
import pathlib
import typing
from typing import Iterable

from dateutil.parser import parse as parse_date


class LogEntry(typing.NamedTuple):
    type_: str
    timestamp: datetime.datetime
    elb: str
    client: str
    target: str
    request_processing_time: float
    target_processing_time: float
    response_processing_time: float
    elb_status_code: str
    target_status_code: str
    received_bytes: int
    sent_bytes: int
    request: str
    user_agent: str


def get_log_lines(logs_dir: str, line_match: str) -> Iterable[str]:
    logs_path = pathlib.Path(logs_dir)
    for log_path in logs_path.glob('**/*.log.gz'):
        with gzip.open(str(log_path), 'rt') as log_file:
            for line in log_file:
                if line_match in line:
                    yield line


def parse_log_line(line: str) -> LogEntry:
    parts = line.split(' ')
    return LogEntry(
        parts[0],
        parse_date(parts[1]),
        parts[2],
        parts[3],
        parts[4],
        float(parts[5]),
        float(parts[6]),
        float(parts[7]),
        parts[8],
        parts[9],
        int(parts[10]),
        int(parts[11]),
        parts[12],
        parts[13],
    )
