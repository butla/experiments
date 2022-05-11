import logging

logging.basicConfig(level=logging.INFO)

LOG_MESSAGE = "the message we'll look for in the test"

_log = logging.getLogger(__name__)


def bla():
    _log.info(LOG_MESSAGE)
    return 5
