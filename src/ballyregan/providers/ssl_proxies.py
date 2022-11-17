from dataclasses import dataclass
from ballyregan.providers import FreeProxyListProvider


@dataclass
class SSLProxiesProvider(FreeProxyListProvider):
    url: str = "https://www.sslproxies.org/"
