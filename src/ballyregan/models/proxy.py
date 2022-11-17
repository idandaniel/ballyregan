from enum import Enum
from typing import List, Optional, Union

from ballyregan.models import HashableBaseModel

UNKNOWN = 'unknown'

class Anonymities(str, Enum):
    ELITE: str = 'elite'
    TRANSPARENT: str = 'transparent'
    ANONYMOUS: str = 'anonymous'
    UNKNOWN: str = UNKNOWN

    @staticmethod
    def values() -> List[str]:
        return [anonymity.value for anonymity in Anonymities]

    
class Protocols(str, Enum):
    HTTP: str = 'http'
    HTTPS: str = 'https'
    SOCKS4: str = 'socks4'
    SOCKS5: str = 'socks5'

    @staticmethod
    def values() -> List[str]:
        return [protocol.value for protocol in Protocols]


class Proxy(HashableBaseModel):

    protocol: Protocols
    ip: str
    port: int
    country: Optional[str] = UNKNOWN
    anonymity: Optional[str] = Anonymities.UNKNOWN

    def __str__(self) -> str:
        return f"{self.protocol}://{self.ip}:{self.port}"

    def dict(
        self,
        *,
        include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> 'DictStrAny':
        attributes = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )

        # Iterate though attributes and convert enums to their values (strings)
        for attribute_key, attribute in attributes.items():
            if isinstance(attribute, Enum):
                attributes.update({attribute_key: attribute.value})

        return attributes
