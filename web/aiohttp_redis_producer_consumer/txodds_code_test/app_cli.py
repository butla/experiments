"""
Common parts for the producer and consumer processes.
"""

import asyncio
import argparse
import logging

import uvloop


def get_redis_args_parser(description):
    """Creates an argument parser for a command that requires a Redis host and port
    on the command line.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('redis_host', metavar='REDIS_HOST', type=str,
                        help='IP address or hostname of a Redis instance.')
    parser.add_argument('redis_port', metavar='REDIS_PORT', type=int,
                        help='Port of a Redis instance on the given address.')
    return parser


def setup_logging():
    """Configures logging for the process.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s')


def get_event_loop() -> asyncio.AbstractEventLoop:
    """Sets uvloop as the default loop for a free speedup on CPython
    and returns a loop for the process to use.
    """
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    return asyncio.get_event_loop()
