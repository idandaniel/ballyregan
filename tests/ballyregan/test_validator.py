from typing import List

import pytest
from urllib3 import ProxyManager
from urllib3.contrib.socks import SOCKSProxyManager

from src.ballyregan import Proxy
from src.ballyregan.models import Protocols
from src.ballyregan.validator import ProxyValidator, ProxyManagerFactory


@pytest.mark.parametrize("manager_factory", [ProxyManagerFactory()])
class TestProxyManagerFactory:
    
    @pytest.mark.parametrize("proxy", [
        Proxy(protocol=Protocols.HTTP, ip="1.1.1.1", port=8080),
        Proxy(protocol=Protocols.HTTPS, ip="1.1.1.1", port=8080),
    ])
    def test_create_http_proxy_manager(self, manager_factory: ProxyManagerFactory, proxy: Proxy):
        manager = manager_factory.create_manager(proxy)
        assert isinstance(manager, ProxyManager)

    @pytest.mark.parametrize("proxy", [
        Proxy(protocol=Protocols.SOCKS4, ip="1.1.1.1", port=8080),
        Proxy(protocol=Protocols.SOCKS5, ip="1.1.1.1", port=8080),
    ])
    def test_create_socks_proxy_manager(self, manager_factory: ProxyManagerFactory, proxy: Proxy):
        manager = manager_factory.create_manager(proxy)
        assert isinstance(manager, SOCKSProxyManager)

    @pytest.mark.parametrize("proxy", [
        "not a proxy"
    ])
    def test_create_proxy_manager_invalid_proxy(self, manager_factory: ProxyManagerFactory, proxy: Proxy):
        with pytest.raises(Exception, match=".* is not a valid proxy"):
            manager = manager_factory.create_manager(proxy)
            assert isinstance(manager, SOCKSProxyManager)


@pytest.mark.parametrize("validator", [ProxyValidator()])
class TestValidator:

    @pytest.mark.parametrize("proxies", [
        ["Not a proxy"],
        "Not a list",
    ])
    def test_filter_valid_proxies_with_invalid_proxies(self, validator: ProxyValidator, proxies: List[Proxy]):
        valid_proxies = validator.filter_valid_proxies(proxies)
        assert valid_proxies == []
        
    @pytest.mark.parametrize("proxies", [
        Proxy(protocol=Protocols.HTTP, ip="Change to valid ip", port=-1)
    ])
    def test_filter_valid_proxies_with_valid_proxies(self, validator: ProxyValidator, proxies: List[Proxy]):
        # TODO: mock valid proxy
        valid_proxies = validator.filter_valid_proxies(proxies)
        assert True

    @pytest.mark.parametrize("proxy", [
        "Not a proxy"
    ])
    def test_is_proxy_valid_with_invalid_proxies(self, validator: ProxyValidator, proxy: Proxy):
        # TODO: mock valid proxy
        is_proxy_valid = validator.is_proxy_valid(proxy)
        assert is_proxy_valid == False