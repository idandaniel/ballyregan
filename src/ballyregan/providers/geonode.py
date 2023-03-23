from typing import List
from dataclasses import dataclass

from requests.exceptions import ConnectionError, JSONDecodeError
from aiohttp import ClientSession

from ballyregan import Proxy
from ballyregan.providers import IProxyProvider
from ballyregan.core.exceptions import ProxyGatherException


@dataclass
class GeonodeProvider(IProxyProvider):
    url: str = "https://proxylist.geonode.com/api/proxy-list"

    async def _get_raw_proxies(self, amount: int = 500) -> List[dict]:
        try:
            async with ClientSession(headers=self._session_headers) as session:
                async with session.get(
                    self.url,
                    params={
                        'page': 1,
                        'limit': amount,
                        'sort_by': 'lastChecked',
                        'sort_type': 'desc',
                        'filterUpTime': 80
                    }
                ) as proxies_response:

                    if not proxies_response.ok:
                        raise ProxyGatherException

                    response_data = await proxies_response.json()
                    proxies_data = response_data['data']

        except (ConnectionError, KeyError, JSONDecodeError):
            raise ProxyGatherException
        else:
            return proxies_data

    @staticmethod
    def raw_proxy_to_object(raw_proxy: dict) -> Proxy:
        return Proxy(
            protocol=raw_proxy['protocols'][0].lower(),
            ip=raw_proxy['ip'],
            port=raw_proxy['port'],
            country=raw_proxy['country'],
            anonymity=raw_proxy['anonymityLevel']
        )
