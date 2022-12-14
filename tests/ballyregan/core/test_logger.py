import re
import logging
from io import StringIO

import pytest
from loguru import logger

import ballyregan.core.exceptions
from src.ballyregan.core.logger import set_logger_level, init_logger
from src.ballyregan.core.exceptions import InvalidDebugMode, NoProxiesFound


class CaptureLoguru:
    """Context manager to capture log streams

    Args:
        logger: logger object

    Results:
        The captured output is available via `self.out`

    """

    def __init__(self, logger):
        self.logger = logger
        self.io = StringIO()
        self.sh = logging.StreamHandler(self.io)
        self.out = ""

    def __enter__(self):
        self.logger.add(self.sh)
        return self

    def __exit__(self, *exc):
        self.logger.remove()
        self.out = self.io.getvalue()


class TestLogger:

    def test_set_logger_level_info(self):
        set_logger_level("INFO")

        info_message = "This is an info message"
        debug_message = "This is a debug message"
        with CaptureLoguru(logger) as caplog:
            logger.info(info_message)
            logger.debug(info_message)

        info_regex = re.compile(f".*INFO.* - {info_message}")
        debug_regex = re.compile(f".*DEBUG.* - {debug_message}")

        assert info_regex.match(
            caplog.out) is not None and not debug_regex.match(caplog.out)

    def test_set_logger_level_debug(self):
        set_logger_level("DEBUG")

        message = "This is a debug message"
        with CaptureLoguru(logger) as caplog:
            logger.debug(message)

        regex = re.compile(f".*DEBUG.* - {message}")
        assert regex.match(caplog.out) is not None

    def test_init_logger(self):
        with pytest.raises(ballyregan.core.exceptions.InvalidDebugMode):
            init_logger(debug="Unknown Option")

        init_logger(debug=False)
        self.test_set_logger_level_debug()

        init_logger(debug=True)
        self.test_set_logger_level_info()