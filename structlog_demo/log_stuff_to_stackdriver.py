import logging.config
from os import path
import sys

import google.cloud.logging as google_logging
import structlog

import some_lib

_log = logging.getLogger(__name__)


def cause_error():
    _log.warning("I'm gonna cause an error!")
    raise ValueError("It's just an error")


if __name__ == '__main__':
    # TODO timestamping should be done by the log aggregator/sender
    timestamper = structlog.processors.TimeStamper(fmt="iso")
    # processing for the messages from the standard lib's logger
    pre_chain = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structured": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(colors=False),
                "foreign_pre_chain": pre_chain,
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "structured",
            },
            "stackdriver": {
                "class": "google.cloud.logging.handlers.CloudLoggingHandler",
                "client": google_logging.Client(),
                "name": path.basename(__file__),
                #"formatter": "structured",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default", "stackdriver"],
                "level": "INFO",
                "propagate": True,
            },
        }
    })

    structlog.configure(
        # TODO log level and timestamp should be omitted, because Stackdriver adds them,
        # but we want them in the console output and that doesn't happen if they're not here.
        # Need to investigate.
	    processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=structlog.threadlocal.wrap_dict(dict),
        cache_logger_on_first_use=True)
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
