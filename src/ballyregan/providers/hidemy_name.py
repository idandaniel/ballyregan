from dataclasses import dataclass
from typing import List

import pandas

from ballyregan import Proxy
from ballyregan.models import Anonymities
from ballyregan.providers import IProxyProvider
from ballyregan.core.exceptions import ProxyGatherException

@dataclass
class HidemynameProvider(IProxyProvider):
    url: str = 'https://hidemy.name/en/proxy-list/?anon=234'

    def _get_raw_proxies(self) -> List[str]:
        proxies = pandas.DataFrame()
        for start in [0, 64, 128]:
            try:
                proxies_response = self._session.get(f'{self.url}', params={'start': start})
                if not proxies_response.ok:
                    raise ProxyGatherException
            except (IndexError, ValueError, ConnectionError) as e:
                raise ProxyGatherException from e
            else:
                proxies_table = pandas.read_html(proxies_response.text)[0]
                proxies = pandas.concat([proxies, proxies_table])

        proxies = proxies.drop_duplicates(keep='first')
        return proxies.to_dict(orient='records')

    @staticmethod
    def raw_proxy_to_object(raw_proxy: dict) -> Proxy:
        """
        Elite Proxy / Highly Anonymous Proxy: The web server can't detect whether you are using a proxy.
        Anonymous Proxy: The web server can know you are using a proxy, but it can't know your real IP.
        Transparent Proxy: The web server can know you are using a proxy and it can also know your real IP.
        """
        anonymity = Anonymities.TRANSPARENT
        if raw_proxy['Anonymity'] == 'High':
            anonymity = Anonymities.ELITE
        elif raw_proxy['Anonymity'] == 'Average':
            anonymity = Anonymities.ANONYMOUS

        protocol1, protocol2 = (raw_proxy['Type'].lower().split(', ') + [None] * 2)[:2]

        return Proxy(
            protocol=protocol2 or protocol1,
            ip=raw_proxy['IP address'],
            port=raw_proxy['Port'],
            anonymity=anonymity,
            country=raw_proxy['Country, City'],
        )
