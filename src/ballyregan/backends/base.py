from abc import ABC, abstractmethod
from typing import List

from ballyregan.models import Proxy, Protocols, Anonymities

class BaseBackend(ABC):
    @abstractmethod
    def create_proxy(self, proxy: Proxy) -> None:
        pass

    @abstractmethod
    def read_proxies(self, protocols: List[Protocols] = [], anonymities: List[Anonymities] = [], limit: int = 0) -> List[Proxy]:
        pass

    @abstractmethod
    def update_proxy(self, proxy_to_update: Proxy, new_proxy: Proxy, insert_if_not_exist: bool = True) -> None:
        pass

    @abstractmethod
    def delete_proxy(self, proxy_to_delete: Proxy) -> None:
        pass

    @abstractmethod
    def export_to_csv(self, file_path: str) -> None:
        pass

    @abstractmethod
    def import_from_csv(self, file_path: str) -> None:
        pass