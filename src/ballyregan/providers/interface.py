from typing import Any, List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod, abstractstaticmethod

from faker import Faker
from requests import Session
from loguru import logger

from ballyregan import Proxy
from ballyregan.core.exceptions import ProxyGatherException


@dataclass
class IProxyProvider(ABC):
    """An interface for provider class. Provider is source which provides us the proxy, for example freeproxieslists.net
    """
    url: str
    _session: Session = field(init=False)

    def __post_init__(self) -> None:
        self._session = Session()
        # uses fake user agent to prevent providers from blocking you.
        self._session.headers = {'User-agent': Faker().user_agent()}

    @abstractmethod
    def _get_raw_proxies(self) -> List[Any]:
        """The provider's way to retrieve the proxies as is from the source.

        Returns:
            List[Any]: List of proxies. the proxies could be either dict, string, etc...
        """
        pass

    @abstractstaticmethod
    def raw_proxy_to_object(raw_proxy: Any) -> Proxy:
        """Gets a proxy and converts it to Proxy class object

        Args:
            raw_proxy (Any): The proxy to convert. could be any type.

        Returns:
            Proxy: The proxy converted to a Proxy model.
        """
        pass

    def gather(self) -> List[Proxy]:
        """The function that returns all the gathered proxies from the source.

        Returns:
            List[Proxy]: The returned proxies. a List of Proxy objects. 
        """
        logger.debug(f'Gathering proxies from {self.__class__.__name__}')
        try:
            raw_proxies = self._get_raw_proxies()
            return list(map(self.raw_proxy_to_object, raw_proxies))                
        except ProxyGatherException:
            logger.warning(
                f'Failed to gather proxies from {self.__class__.__name__}, skipping.'
            )
            return []
