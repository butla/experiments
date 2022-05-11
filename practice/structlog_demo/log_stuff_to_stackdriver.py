import logging
from os import path

import structlog
import google.cloud.logging
import google.cloud.logging.handlers

import log_config
import some_lib

_log = logging.getLogger(__name__)


def add_stackdriver_logging():
    stackdriver_handler = google.cloud.logging.handlers.CloudLoggingHandler(
        client=google.cloud.logging.Client(),
        name=path.basename(__file__),
    )

    root_logger = logging.getLogger()
    root_logger.addHandler(stackdriver_handler)


def cause_error():
    _log.warning("I'm gonna cause an error!")
    raise ValueError("It's just an error")


if __name__ == '__main__':
    log_config.configure_logging(logging.INFO)
    add_stackdriver_logging()

    structured_log = structlog.get_logger() 
    structured_log = structured_log.bind(bound='something_bound')
    structured_log.info(
        "It's from the tied in structured logger!",
        some_key='some_other_value')

    _log.debug("I'm a debug message, you won't see me")

    _log.info('plain logging log!')
    _log.info('logging log with params: %s, %s!', 'the other param will be an int', 13)
    print(some_lib.ble())

    try:
        cause_error()
    except ValueError:
        _log.exception("Logging the error before stuffing it out")
        structured_log.exception("Logging the error with struct log")
