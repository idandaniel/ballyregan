from typing import List
from dataclasses import dataclass

import pandas
from requests.exceptions import ConnectionError
from aiohttp import ClientSession

from ballyregan import Proxy
from ballyregan.models import Protocols
from ballyregan.providers import IProxyProvider
from ballyregan.core.exceptions import ProxyGatherException, ProxyParseException


@dataclass
class FreeProxyListProvider(IProxyProvider):

    url: str = 'https://free-proxy-list.net/'

    async def _get_raw_proxies(self) -> List[dict]:
        try:
            async with ClientSession(headers=self._session_headers) as session:
                async with session.get(self.url) as proxies_response:
                    if not proxies_response.ok:
                        raise ProxyGatherException
                    
                    response_text = await proxies_response.text()
                    proxies_table = pandas.read_html(response_text)[0]
        except (IndexError, ValueError, ConnectionError):
            raise ProxyGatherException
        else:
            return proxies_table.to_dict(orient='records')

    @staticmethod
    def raw_proxy_to_object(raw_proxy: dict) -> Proxy:
        try:
            protocol = Protocols.HTTPS if raw_proxy['Https'].lower() == 'yes' else Protocols.HTTP
            anonymity = raw_proxy['Anonymity'].split()[0].lower()
            return Proxy(
                protocol=protocol,
                ip=raw_proxy['IP Address'],
                port=raw_proxy['Port'],
                country=raw_proxy['Country'],
                anonymity=anonymity
            )
        except KeyError:
            raise ProxyParseException



