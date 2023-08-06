import logging
import sys


DEFAULT_USER_LOG_FORMAT = '%(levelname)s: %(message)s'


def __build_logger(service_name: str) -> logging.Logger:
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(DEFAULT_USER_LOG_FORMAT))
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


# The logger for runtime code
__LOGGER = __build_logger('runtime')


def get_logger() -> logging.Logger:
    """
    Return the logger instance for runtime.
    """
    return __LOGGER
