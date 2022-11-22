import sys
from loguru import logger

from ballyregan.core.exceptions import InvalidDebugMode


def set_logger_level(log_level: str):
    logger.remove()
    logger.add(sys.stdout, level=log_level)


def init_logger(debug: bool) -> None:
    debug_levels_mapper = {
        True: 'DEBUG',
        False: 'INFO'
    }

    if debug not in debug_levels_mapper.keys():
        raise InvalidDebugMode(f"Invalid debug mode {debug}")

    log_level = debug_levels_mapper[debug]
    set_logger_level(log_level)
