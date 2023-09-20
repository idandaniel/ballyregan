from __future__ import annotations
from threading import Thread
import time
from typing import Any, List
from asyncio import AbstractEventLoop
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4
from faker import Generator

from loguru import logger

from ballyregan import Proxy
from ballyregan.backends import BaseBackend, DataframeBackend
from ballyregan.models import Protocols, Anonymities
from ballyregan.core.exceptions import NoProxiesFound, NoInternetConnection
from ballyregan.core.logger import init_logger
from ballyregan.core.utils import has_internet_connection, get_event_loop
from ballyregan.validator import ProxyValidator
from ballyregan.filterer import ProxyFilterer
from ballyregan.providers import (
    IProxyProvider,
    FreeProxyListProvider,
    GeonodeProvider,
    SSLProxiesProvider,
    USProxyProvider,
    ProxyListDownloadProvider,
    SocksProxyProvider
)


@dataclass
class ProxyFetcher:
    proxy_providers: List[IProxyProvider] = field(
        default_factory=lambda: [
            SSLProxiesProvider(),
            FreeProxyListProvider(),
            GeonodeProvider(),
            USProxyProvider(),
            ProxyListDownloadProvider(),
            SocksProxyProvider(),
        ]
    )
    proxy_validator: ProxyValidator = None
    proxy_filterer: ProxyFilterer = None
    backend: BaseBackend = None
    loop: AbstractEventLoop = None
    debug: bool = False
    background_gather: bool = False
    background_gather_interval: int = 0

    def __post_init__(self) -> None:
        if not has_internet_connection():
            raise NoInternetConnection

        if not self.proxy_filterer:
            self.proxy_filterer = ProxyFilterer()

        if not self.proxy_validator:
            self.proxy_validator = self.__new_validator()

        if not self.backend:
            self.backend = DataframeBackend()

        if self.background_gather:
            self._background_gather_thread = self.__new_background_gather_thread()
            self._background_gather_thread.start()
        else:
            self._background_gather_thread = None

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'debug':
            init_logger(__value)

        if __name == 'background_gather':
            if __value == True:
                self._background_gather_thread = self.__new_background_gather_thread()
                self._background_gather_thread.start()

        super().__setattr__(__name, __value)

    def __new_validator(self) -> ProxyValidator:
        if not self.loop:
            self.loop = get_event_loop()

        return ProxyValidator(loop=self.loop)
    
    def __new_background_gather_thread(self) -> Thread:
         return Thread(
            target=self._background_gather,
            daemon=True,
            name=f"ballyregan-background-gather-thread-{uuid4()}"
        )

    def gather(self) -> None:
        logger.debug('Gathering all proxies from providers')

        def gather_and_insert(provider: IProxyProvider) -> None:
            try:
                proxies = provider.gather()
                for proxy in proxies:
                    logger.debug("Inserting to backend", proxy=proxy)
                    self.backend.create_proxy(proxy)
            except (KeyboardInterrupt, SystemExit):
                pass

        providers_gather_threads = []

        for provider in self.proxy_providers:
            thread = Thread(daemon=True, target=gather_and_insert, args=(provider,))
            thread.start()
            providers_gather_threads.append(thread)
        
        for thread in providers_gather_threads:
            thread.join()

        logger.debug('Finished gathering all proxies from providers')

    def _background_gather(self) -> None:
        try:
            while self.background_gather:
                self.gather()
                time.sleep(self.background_gather_interval)
        except (KeyboardInterrupt, SystemExit):
            pass

    def get_nowait(
        self,
        protocols: List[Protocols] = [],
        anonymities: List[Anonymities] = [],
        limit: int = 0,
    ) -> List[Proxy]:
        stored_proxies = self.backend.read_proxies(protocols=protocols, anonymities=anonymities)
        valid_proxies = self.proxy_validator.filter_valid_proxies(
            proxies=stored_proxies,
            limit=limit,
        )
        logger.debug(
            f'Finished proxies validation, {len(valid_proxies)} valid proxies were found.'
        )
        if not valid_proxies:
            raise NoProxiesFound
        return valid_proxies

    def get(
        self,
        protocols: List[Protocols] = [],
        anonymities: List[Anonymities] = [],
        limit: int = 0,
        wait: bool = True
    ) -> List[Proxy]:
        if not wait:
            return self.get_nowait(protocols=protocols, anonymities=anonymities, limit=limit)
        
        if not limit and wait:
            raise ValueError(
                "Limit must be greater than zero when wait=True."
            )
        
        while wait:
            proxies = []
            try:
                proxies += self.get_nowait(
                    protocols=protocols,
                    anonymities=anonymities,
                    limit=limit
                )
            except NoProxiesFound:
                pass
            else:
                if limit and len(proxies) == limit:
                    return proxies
                limit -= len(proxies)


    def get_one(
        self,
        protocols: List[Protocols] = [],
        anonymities: List[Anonymities] = [],
        wait: bool = True
    ) -> Proxy:
        return self.get(
            protocols=protocols,
            anonymities=anonymities,
            limit=1,
            wait=wait
        )[0]