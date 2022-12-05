from typing import List, Any
from dataclasses import dataclass

import pytest

import ballyregan.core.exceptions
from src.ballyregan import Proxy
from src.ballyregan.fetcher import ProxyFetcher
from src.ballyregan.validator import ProxyValidator
from src.ballyregan.providers import IProxyProvider
from src.ballyregan.core.utils import get_event_loop
from tests.ballyregan.core.test_logger import TestLogger
from tests.ballyregan.disable_socket import disable_socket



class TestFetcherDebug:

    @pytest.fixture(autouse=True)
    def fetcher(self):
        return ProxyFetcher()

    @pytest.mark.parametrize('debug', [True, False])
    def test_fetcher_set_debug(self, fetcher: ProxyFetcher, debug: bool):
        fetcher.debug = debug
        assert fetcher.debug == debug
        
        test_logger = TestLogger()
        if debug:
            test_logger.test_set_logger_level_debug()
        else:
            test_logger.test_set_logger_level_info()


@disable_socket
def test_new_fetcher_no_connection():
    with pytest.raises(ballyregan.core.exceptions.NoInternetConnection):
        _ = ProxyFetcher()

        
def test_new_fetcher_with_loop():
    loop = get_event_loop()
    fetcher = ProxyFetcher(loop=loop)
    assert fetcher.loop == loop


class TestFetcherGet:

    @dataclass
    class FakeProvider(IProxyProvider):

        url: str = 'https://provider.fake.url'

        def _get_raw_proxies(self) -> List[Any]:
            fake_proxy = {
                'protocol': 'https',
                'ip': '1.1.1.1',
                'port': 8080
            }
            return [fake_proxy or _ in range(10)]

        @staticmethod
        def raw_proxy_to_object(raw_proxy: dict) -> Proxy:
            return Proxy(**raw_proxy)

    @dataclass
    class FakeValidator(ProxyValidator):

        def filter_valid_proxies(self, proxies: List[Proxy], limit: int = 0) -> List[Proxy]:
            return proxies[:limit] if limit > 0 else proxies


    @pytest.mark.parametrize('fetcher', [ProxyFetcher(_proxy_providers=[])])
    def test_get_with_no_providers(self, fetcher: ProxyFetcher):
        with pytest.raises(ballyregan.core.exceptions.NoProxiesFound):
            fetcher.get()


    @pytest.mark.parametrize('fetcher', [ProxyFetcher(_proxy_providers=[FakeProvider()], _proxy_validator=FakeValidator())])
    def test_get_with_providers(self, fetcher: ProxyFetcher):
        proxies = fetcher.get()
        assert len(proxies) > 0
        for proxy in proxies:
            assert isinstance(proxy, Proxy)


    @pytest.mark.parametrize('fetcher', [ProxyFetcher(_proxy_providers=[FakeProvider()], _proxy_validator=FakeValidator())])
    def test_get_one_with_providers(self, fetcher: ProxyFetcher):
        proxies = fetcher.get_one()
        assert len(proxies) == 1
        assert isinstance(proxies[0], Proxy)


    

