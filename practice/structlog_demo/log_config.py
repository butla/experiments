import logging
import sys

import structlog

def _log_uncaught_exception(exc_type, exc_value, exc_traceback):
    structlog.get_logger().error(
        "Uncaught error",
        exc_info=(exc_type, exc_value, exc_traceback))


def configure_logging(log_level):
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

    console_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(colors=False),
        foreign_pre_chain=pre_chain
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

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
        cache_logger_on_first_use=True
    )

    sys.excepthook = _log_uncaught_exception
