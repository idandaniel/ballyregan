import json
from dataclasses import dataclass
from typing import List

import pandas

from ballyregan import Proxy
from ballyregan.models import Anonymities
from ballyregan.providers import IProxyProvider
from ballyregan.core.exceptions import ProxyGatherException

@dataclass
class HidesterProvider(IProxyProvider):
    url: str = 'https://hidester.com/proxydata/php/data.php'

    def _get_raw_proxies(self) -> List[str]:
        proxies = pandas.DataFrame()

        try:
            proxies_response = self._session.get(
                    url=self.url,
                    headers= {
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Host': 'hidester.com',
                        'Referer': 'https://hidester.com/ru/public-proxy-ip-list/',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'TE': 'trailers',
                        'User-agent':self._session.headers['User-agent']
                    },
                    params={
                        'mykey': 'data',
                        'offset': 0,
                        'limit': 500,
                        'orderBy': 'latest_check',
                        'sortOrder': 'DESC',
                        'country': '',
                        'port': '',
                        'type': 'undefined',
                        'anonymity': 'undefined',
                        'ping': 'undefined',
                        'gproxy': 2,
                    }
            )
        except Exception as ex:
            raise ProxyGatherException from ex

        proxies = pandas.read_json(proxies_response.content.decode("utf-8"))
        proxies = proxies.drop_duplicates(keep='first')
        return proxies.to_dict(orient='records')

    @staticmethod
    def raw_proxy_to_object(raw_proxy: dict) -> Proxy:
        return Proxy(
            protocol=raw_proxy['type'],
            ip=raw_proxy['IP'],
            port=raw_proxy['PORT'],
            anonymity=raw_proxy['anonymity'].lower(),
            country=raw_proxy['country']
        )
