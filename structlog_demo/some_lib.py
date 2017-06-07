import logging

import structlog

_log = logging.getLogger(__name__)
_log_s = structlog.get_logger()


def ble():
    _log.info("I'm doing something in the library")
    _log_s.info("Structured library logging from global.")
    log = _log_s.new()
    log.info("Structured library logging from new one.")
    return 'ble'
