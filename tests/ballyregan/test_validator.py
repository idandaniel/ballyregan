from typing import List

import pytest

from src.ballyregan import Proxy
from src.ballyregan.models import Protocols
from src.ballyregan.validator import ProxyValidator


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
    @pytest.mark.asyncio
    async def test_is_proxy_valid_with_invalid_proxies(self, validator: ProxyValidator, proxy: Proxy):
        # TODO: mock valid proxy
        is_proxy_valid = await validator.is_proxy_valid(proxy)
        assert is_proxy_valid == False
