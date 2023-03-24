import asyncio

from src.ballyregan.core.utils import get_event_loop, has_internet_connection
from tests.ballyregan.disable_socket import disable_socket


def test_get_event_loop():
    assert get_event_loop() is not None


class TestInternetConnection():

    @disable_socket
    def test_offline(self):
        assert has_internet_connection() == False


    def test_online(self):
        assert has_internet_connection() == True