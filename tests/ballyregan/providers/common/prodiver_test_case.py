from typing import Union
from dataclasses import dataclass

from src.ballyregan import Proxy
from src.ballyregan.providers import IProxyProvider


@dataclass
class ProviderTestCase:
    provider: IProxyProvider
    expected_response: Union[str, dict]
    expected_proxies: Proxy

    def __post_init__(self) -> None:
        if isinstance(self.expected_response, dict):
            self.expected_response_type = 'json'
        else:
            self.expected_response_type = 'text'