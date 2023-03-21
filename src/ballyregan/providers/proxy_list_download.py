import time
from typing import List
from dataclasses import dataclass

from ballyregan import Proxy
from ballyregan.models import Protocols
from ballyregan.providers import IProxyProvider
from ballyregan.core.exceptions import ProxyGatherException, ProxyParseException


@dataclass
class ProxyListDownloadProvider(IProxyProvider):

    url: str = "https://www.proxy-list.download/api/v1/get"

    def _get_raw_proxies(self) -> List[str]:
        proxies = []

        for protocol in Protocols.values():
            try:
                response = self._session.get(self.url, params={'type': protocol})
                if response.status_code == 429:
                    continue
                if not response.ok:
                    raise ProxyGatherException
            except Exception:
                raise ProxyGatherException
            else:
                proxies_result = response.text.splitlines()
                proxies_with_protocol = [f'{protocol}:{proxy}' for proxy in proxies_result]
                proxies += proxies_with_protocol
                
        return proxies

    @staticmethod
    def raw_proxy_to_object(raw_proxy: str) -> Proxy:
        try:
            protocol, ip, port = raw_proxy.split(':')
        except ValueError:
            raise ProxyParseException
        return Proxy(
            ip=ip,
            port=port,
            protocol=protocol.lower()
        )