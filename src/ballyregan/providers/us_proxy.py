from dataclasses import dataclass

from ballyregan.providers.free_proxy_list import FreeProxyListProvider


@dataclass
class USProxyProvider(FreeProxyListProvider):
    url = "https://us-proxy.org/"