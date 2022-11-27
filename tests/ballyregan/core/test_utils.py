import asyncio

from src.ballyregan.core.utils import get_event_loop, has_internet_connection
from tests.ballyregan.disable_socket import run_offline


def test_get_event_loop():
    assert get_event_loop() == asyncio.get_event_loop()


class TestInternetConnection():

    @run_offline
    def test_offline(self):
        assert has_internet_connection() == False


    def test_online(self):
        assert has_internet_connection() == True