from typing import List

from loguru import logger

from ballyregan import Proxy
from ballyregan.models import Protocols, Anonymities


class ProxyFilterer:

    @staticmethod
    def filter(proxies: List[Proxy], protocols: List[Protocols] = [], anonymities : List[Anonymities] = []) -> List[Proxy]:
        logger.debug(f'Filtering proxies')
        return ProxyFilterer._filter(
            proxies=proxies,
            protocols=protocols,
            anonymities=anonymities
        )

    @staticmethod
    def _is_proxy_field_in_filter_attribute(proxy: Proxy, proxy_field: str, filter_attribute: list) -> bool:
        return proxy.__getattribute__(proxy_field) in filter_attribute

    @staticmethod
    def _filter(proxies: List[Proxy], protocols: List[Protocols] = [], anonymities : List[Anonymities] = []) -> List[Proxy]:
        filter_attributes_proxy_fields = {
            tuple(protocols): 'protocol',
            tuple(anonymities): 'anonymity'
        }

        for filter_attribute, proxy_field in filter_attributes_proxy_fields.items():
            if not filter_attribute:
                continue

            logger.debug(f'Filtering by "{proxy_field}": {filter_attribute}')
            proxies = list(filter(
                lambda proxy: ProxyFilterer._is_proxy_field_in_filter_attribute(
                    proxy=proxy,
                    proxy_field=proxy_field,
                    filter_attribute=filter_attribute
                ),
                proxies
            ))

        return proxies
