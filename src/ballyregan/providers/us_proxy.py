from ballyregan.providers.free_proxy_list import FreeProxyListProvider


from dataclasses import dataclass


@dataclass
class USProxyProvider(FreeProxyListProvider):
    url = "https://us-proxy.org/"