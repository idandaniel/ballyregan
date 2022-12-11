from dataclasses import dataclass
from typing import List

import pandas

from ballyregan import Proxy
from ballyregan.models import Protocols
from ballyregan.providers import IProxyProvider
from ballyregan.core.exceptions import ProxyGatherException
from ballyregan import ProxyFetcher


@dataclass
class ProxyscrapeProvider(IProxyProvider):
    # https://docs.proxyscrape.com/
    url: str = 'https://api.proxyscrape.com/v2/?request=getproxies&country=all&ssl=all'

    def _get_raw_proxies(self) -> List[str]:
        proxies = pandas.DataFrame(columns=['protocol','ip','port','anonymity'])

        for anonymity in ['elite', 'transparent', 'anonymous']:
            for protocol in Protocols.values():
                try:
                    proxies_response = self._session.get(f'{self.url}', params={'protocol': protocol, 'anonymity': anonymity})
                    if not proxies_response.ok:
                        raise ProxyGatherException
                except (IndexError, ValueError, ConnectionError) as e:
                    raise ProxyGatherException from e
                else:
                    for proxy in proxies_response.text.splitlines():
                        ip, port = proxy.split(':')
                        proxies = pandas.concat(
                            [
                                pandas.DataFrame([[protocol, ip, port, anonymity]],
                                columns=proxies.columns),
                                proxies
                            ], ignore_index=True)

        proxies = proxies.drop_duplicates(keep='first')
        return proxies.to_dict(orient='records')

    @staticmethod
    def raw_proxy_to_object(raw_proxy: dict) -> Proxy:
        return Proxy(
            protocol=raw_proxy['protocol'],
            ip=raw_proxy['ip'],
            port=raw_proxy['port'],
            anonymity=raw_proxy['anonymity']
        )
