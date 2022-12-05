from typing import List

import pytest

from src.ballyregan import Proxy
from src.ballyregan.filterer import ProxyFilterer
from src.ballyregan.models import Anonymities, Protocols


IP = '1.1.1.1'
PORT = 8080


@pytest.mark.parametrize('filterer', [ProxyFilterer()])
class TestFilterer:

    @pytest.fixture(scope='module')
    def proxies(self) -> List[Proxy]:
        return [
            Proxy(ip=IP, port=PORT, protocol=Protocols.HTTP, anonymity=Anonymities.ELITE),
            Proxy(ip=IP, port=PORT, protocol=Protocols.HTTPS, anonymity=Anonymities.ELITE),
            Proxy(ip=IP, port=PORT, protocol=Protocols.SOCKS4, anonymity=Anonymities.ELITE),
            Proxy(ip=IP, port=PORT, protocol=Protocols.SOCKS5, anonymity=Anonymities.ELITE),
            Proxy(ip=IP, port=PORT, protocol=Protocols.HTTP, anonymity=Anonymities.ANONYMOUS),
            Proxy(ip=IP, port=PORT, protocol=Protocols.HTTPS, anonymity=Anonymities.ANONYMOUS),
            Proxy(ip=IP, port=PORT, protocol=Protocols.SOCKS4, anonymity=Anonymities.ANONYMOUS),
            Proxy(ip=IP, port=PORT, protocol=Protocols.SOCKS5, anonymity=Anonymities.ANONYMOUS),
            Proxy(ip=IP, port=PORT, protocol=Protocols.HTTP, anonymity=Anonymities.TRANSPARENT),
            Proxy(ip=IP, port=PORT, protocol=Protocols.HTTPS, anonymity=Anonymities.TRANSPARENT),
            Proxy(ip=IP, port=PORT, protocol=Protocols.SOCKS4, anonymity=Anonymities.TRANSPARENT),
            Proxy(ip=IP, port=PORT, protocol=Protocols.SOCKS5, anonymity=Anonymities.TRANSPARENT),
        ]

    @pytest.mark.parametrize('anonymity', Anonymities.values())
    def test_filter_by_anonymities(self, filterer: ProxyFilterer, proxies: List[Proxy], anonymity):
        filtered_proxies = filterer.filter(proxies, anonymities=[anonymity])
        for proxy in filtered_proxies:
            assert proxy.anonymity == anonymity


    @pytest.mark.parametrize('protocol', Protocols.values())
    def test_filter_by_protocols(self, filterer: ProxyFilterer, proxies: List[Proxy], protocol):
        filtered_proxies = filterer.filter(proxies, protocols=[protocol])
        for proxy in filtered_proxies:
            assert proxy.protocol == protocol

