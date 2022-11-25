import asyncio
from asyncio import AbstractEventLoop
from queue import Full, Queue
from typing import List
from dataclasses import dataclass

import aiohttp
from aiohttp.client import ClientTimeout
from aiohttp_proxy import ProxyConnector as HTTPConnector

from loguru import logger
import urllib3
from urllib3.connectionpool import InsecureRequestWarning

from ballyregan import Proxy
from ballyregan.models import Protocols


@dataclass
class ProxyValidator:

    urllib3.disable_warnings(InsecureRequestWarning)

    loop: AbstractEventLoop
    _judge_domain: str = 'httpheader.net/azenv.php'
    _default_timeout: ClientTimeout = ClientTimeout(total=30)

    async def _aiohttp_validation(self, proxy: Proxy) -> bool:

        judge_protocol = Protocols.HTTPS if proxy.protocol==Protocols.HTTPS else Protocols.HTTP
        
        async with aiohttp.ClientSession(
            timeout=self._default_timeout,
            connector=HTTPConnector.from_url(str(proxy))
        ) as session:
            try:
                async with session.get(f"{judge_protocol}://{self._judge_domain}", ssl=False) as response:
                    return response.ok
            except Exception:
                return False

    async def is_proxy_valid(self, proxy: Proxy) -> bool:
        """Wrapper function uses the validation function

        Args:
            proxy (Proxy): Proxy to validate.

        Returns:
            bool: Whether or not the proxy is valid.
        """
        logger.debug(f'Validating proxy {proxy}')

        try:
            is_proxy_valid = await self._aiohttp_validation(proxy)
        except Exception as e:
            logger.error(
                f'Unknown exception has occured while validating proxy: {e}'
            )
            return False
        else:
            logger.debug(
                f'Proxy {proxy} is {"valid" if is_proxy_valid else "invalid"}'
            )
            return is_proxy_valid

    def filter_valid_proxies(self, proxies: List[Proxy], limit: int = 0) -> List[Proxy]:
        """Gets a list of proxies, filters them and returns only the valid ones.
        The filter uses Greenlets to make the process more efficient.

        Args:
            proxies (List[Proxy]): Proxy list to filter
            limit (int, optional): The amount of valid proxies to get.
            When 0 the validator will validate all the proxies in the list. Defaults to 0.

        Returns:
            List[Proxy]: The filter list contains only valid proxies
        """
        logger.debug('Filtering valid proxies')

        valid_proxies = Queue(maxsize=limit)

        async def put_proxy_in_queue_if_valid(proxy: Proxy):
            nonlocal valid_proxies

            if valid_proxies.qsize() >= limit and limit != 0:
                raise Full

            is_proxy_valid = await self.is_proxy_valid(proxy)
            if not is_proxy_valid:
                return

            valid_proxies.put_nowait(proxy)

        futures = asyncio.gather(*[
            put_proxy_in_queue_if_valid(proxy)
            for proxy in proxies
        ])
        try:
            self.loop.run_until_complete(futures)
        except Full:
            pass

        logger.debug('Finished filtering valid proxies')

        return list(valid_proxies.queue)
