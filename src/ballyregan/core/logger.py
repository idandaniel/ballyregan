import sys
from loguru import logger


def set_logger_level(log_level: str):
    logger.remove()
    logger.add(sys.stdout, level=log_level)


def init_logger(debug: bool) -> None:
    debug_levels_mapper = {
        True: 'DEBUG',
        False: 'INFO'
    }
    set_logger_level(debug_levels_mapper[debug])
