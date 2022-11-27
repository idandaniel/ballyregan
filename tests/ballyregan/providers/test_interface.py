from abc import ABCMeta
from dataclasses import dataclass

from src.ballyregan.providers import IProxyProvider


def test_iproxy_provider():
    IProxyProvider.__abstractmethods__ = frozenset()

    @dataclass
    class Dummy(IProxyProvider):
        url: str

    test_url = "https://iproxy-provider-dummy-url.com"
    dummy = Dummy(url=test_url)

    raw_proxies = dummy._get_raw_proxies()
    proxies = dummy.raw_proxy_to_object("raw_proxy")

    assert isinstance(IProxyProvider, ABCMeta)
    assert raw_proxies is None
    assert proxies is None