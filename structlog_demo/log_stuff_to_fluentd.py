import logging
import platform

import fluent.handler
import structlog

import log_config
import some_lib

_log = logging.getLogger(__name__)


def add_fluentd_logging():
    format_for_nonstructured_messages = {
        'event': '%(message)s',
        #'message': '%(event)s',
        'logger': '%(name)s',
        'level': '%(levelname)s',
        'stack_trace': '%(exc_text)s'
    }

    fluentd_handler = fluent.handler.FluentHandler(
        'test_app', host=platform.node())
    fluentd_handler.setFormatter(
        fluent.handler.FluentRecordFormatter(fmt=format_for_nonstructured_messages))

    root_logger = logging.getLogger()
    root_logger.addHandler(fluentd_handler)


def cause_error():
    _log.warning("I'm gonna cause an error!")
    raise ValueError("It's just an error")


if __name__ == '__main__':
    log_config.configure_logging(logging.INFO)
    add_fluentd_logging()

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
