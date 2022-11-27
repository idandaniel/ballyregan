from dataclasses import dataclass

from ballyregan import Proxy
from ballyregan.providers import FreeProxyListProvider
from ballyregan.core.exceptions import ProxyParseException


@dataclass
class SocksProxyProvider(FreeProxyListProvider):

    url: str = 'https://socks-proxy.net/'

    @staticmethod
    def raw_proxy_to_object(raw_proxy: dict) -> Proxy:
        proxy = FreeProxyListProvider.raw_proxy_to_object(raw_proxy)
        try:
            proxy.protocol = raw_proxy['Version'].lower()
        except KeyError:
            raise ProxyParseException
        else:
            return proxy