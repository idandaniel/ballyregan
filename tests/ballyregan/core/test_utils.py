import pytest

from src.ballyregan.models import Proxy, Protocols, Anonymities
from src.ballyregan.core.utils import make_requests_proxies_dict_from_proxy

FAKE_PROXY_DATA = dict(
    ip="1.1.1.1",
    port=8080,
    anonymity=Anonymities.ELITE
)

@pytest.mark.parametrize("proxy", [
    Proxy(protocol=Protocols.HTTP, **FAKE_PROXY_DATA),
    Proxy(protocol=Protocols.HTTPS, **FAKE_PROXY_DATA),
    Proxy(protocol=Protocols.SOCKS4, **FAKE_PROXY_DATA),
    Proxy(protocol=Protocols.SOCKS5, **FAKE_PROXY_DATA)
])
def test_make_requests_proxies_dict_from_proxy(proxy: Proxy) -> dict:
    proxies_dict = make_requests_proxies_dict_from_proxy(proxy)

    if proxy.protocol in [Protocols.SOCKS4, Protocols.SOCKS5]:
        assert proxies_dict == {
            Protocols.HTTP: str(proxy),
            Protocols.HTTPS: str(proxy)
        }

    else:
        assert proxies_dict == {proxy.protocol: str(proxy)}