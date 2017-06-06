# TODO
# * normal output
# * structured output

import logging

import structlog
import structlog.stdlib

import some_lib

_log = logging.getLogger(__name__)


def cause_error():
    _log.warn("I'm gonna cause an error!")
    raise ValueError("It's just an error")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    independent_log = structlog.get_logger()
    independent_log.info(
        "It's from the independent structured logger!",
        some_key='some_value')

    structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())
    structured_log = structlog.get_logger() 
    structured_log.info(
        "It's from the tied in structured logger!",
        some_key='some_other_value')

    _log.debug("I'm a debug message, you won't see me")

    _log.info('glowny plik!')
    print(some_lib.ble())

    try:
        cause_error()
    except ValueError:
        _log.exception("Logging the error before stuffing it out")
