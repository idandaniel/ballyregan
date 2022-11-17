from queue import Full, Queue

import gevent
from gevent import monkey, Greenlet
from gevent.exceptions import GreenletExit

from loguru import logger
from typing import List, Union

monkey.patch_all(thread=False, select=False)
import urllib3
from urllib3.connectionpool import InsecureRequestWarning
from urllib3 import PoolManager, ProxyManager
from urllib3.contrib.socks import SOCKSProxyManager
from urllib3.util import Timeout, Retry
from urllib3.exceptions import HTTPError

from ballyregan import Proxy
from ballyregan.models import Protocols


class ProxyManagerFactory:
    """Factory for creating urllib3's ProxyManager for either http or socks
    """
    def create_manager(self, proxy: Proxy) -> PoolManager:
        _protocols_to_pool_manager_creators: dict = {
            Protocols.SOCKS4: self._create_socks_manager,
            Protocols.SOCKS5: self._create_socks_manager,
            Protocols.HTTP: self._create_http_manager,
            Protocols.HTTPS: self._create_http_manager
        }
        try:
            pool_manager_creator = _protocols_to_pool_manager_creators[proxy.protocol]
        except KeyError:
            raise Exception(f'Protocol {proxy.protocol} has no pool creator')
        return pool_manager_creator(proxy)

    def _create_http_manager(self, proxy: Proxy) -> PoolManager:
        manager_args = dict(proxy_url=f'http://{proxy.ip}:{proxy.port}')
        ignore_ssl_args = dict(
            cert_reqs='CERT_NONE',
            assert_hostname=False
        )

        if proxy.protocol == Protocols.HTTPS:
            manager_args.update(**ignore_ssl_args)

        return ProxyManager(**manager_args)

    def _create_socks_manager(self, proxy: Proxy) -> PoolManager:
        socks_protocols_mapper = {
            Protocols.SOCKS5: 'socks5h',
            Protocols.SOCKS4: 'socks4a'
        }
        manager_protocol = socks_protocols_mapper[proxy.protocol]
        return SOCKSProxyManager(
            f'{manager_protocol}://{proxy.ip}:{proxy.port}'
        )


class ProxyValidator:
    """The ProxyValidator is responsible for validating proxies in ThreadPoolExecutor for efficiency.
    """

    urllib3.disable_warnings(InsecureRequestWarning)

    _judge_domain: str = 'httpheader.net/azenv.php'
    _default_timeout: Timeout = Timeout(connect=10, read=2)
    _default_retry: Union[bool, Retry] = Retry(connect=1, read=5)

    def _urllib_validation(self, proxy: Proxy) -> bool:
        """Validated proxy with urllib3 PoolManager objects.

        Args:
            proxy (Proxy): Proxy to validate.

        Returns:
            bool: Whether or not the proxy is valid.
        """
        pool_manager = ProxyManagerFactory().create_manager(proxy)
        judge_protocol = Protocols.HTTPS if proxy.protocol == Protocols.HTTPS else Protocols.HTTP
        try:
            response = pool_manager.request(
                method='GET',
                url=f'{judge_protocol}://{self._judge_domain}',
                timeout=self._default_timeout,
                retries=self._default_retry
            )
            return response.status == 200
        except HTTPError:
            return False

    def is_proxy_valid(self, proxy: Proxy) -> bool:
        """Wrapper function uses the validation function

        Args:
            proxy (Proxy): Proxy to validate.

        Returns:
            bool: Whether or not the proxy is valid.
        """
        logger.debug(f'Validating proxy {proxy}')

        try:
            is_proxy_valid = self._urllib_validation(proxy)
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

    def _create_proxy_validation_greenlets(self, proxies: List[Proxy], proxies_queue: Queue, limit: int) -> List[Greenlet]:
        """Creates greenlets for proxy validation.
        Each greenlet will loop through a bunch of proxies and run put_proxy_if_valid/

        Args:
            proxies (List[Proxy]): List of proxies to validate.
            proxies_queue (Queue): Queue of proxies to append valid proxies to.
            limit (int): Maximum of proxies to validate.

        Raises:
            Full: Proxies Raised when queue is full
            GreenletExit: Raised when want to kill greenlet gracefully

        Returns:
            List[Greenlet]: List of proxy validation greenlets
        """

        def put_proxy_if_valid(proxy: Proxy) -> None:
            nonlocal proxies_queue, limit

            if proxies_queue.qsize() >= limit and limit != 0:
                raise Full

            if not self.is_proxy_valid(proxy):
                raise GreenletExit

            proxies_queue.put_nowait(proxy)
            logger.success(f'Found {proxy}')

        return [
            gevent.spawn(put_proxy_if_valid, proxy)
            for proxy in proxies
        ]


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
        greenlets = self._create_proxy_validation_greenlets(
            proxies=proxies,
            proxies_queue=valid_proxies,
            limit=limit
        )

        def errors_handler(context, type, value, tb):

            if isinstance(value, Full):
                gevent.killall(greenlets)
                return list(valid_proxies.queue)

        gevent.get_hub().handle_error = errors_handler
        gevent.joinall(greenlets)

        logger.debug('Finished filtering valid proxies')

        return list(valid_proxies.queue)
