from typing import List

import pytest
from aiohttp.client_exceptions import ClientConnectionError
from aioresponses import aioresponses

from src.ballyregan import Proxy
from src.ballyregan.models import Protocols, Anonymities
from src.ballyregan.validator import ProxyValidator


PROXIES = [
    Proxy(protocol=Protocols.HTTP, ip="1.1.1.1", port=8080,anonymity=Anonymities.ELITE, country='unknown'),
    Proxy(protocol=Protocols.HTTPS, ip="1.1.1.1", port=8080,anonymity=Anonymities.ELITE, country='unknown'),
    Proxy(protocol=Protocols.SOCKS4, ip="1.1.1.1", port=8080,anonymity=Anonymities.ELITE, country='unknown'),
    Proxy(protocol=Protocols.SOCKS5, ip="1.1.1.1", port=8080,anonymity=Anonymities.ELITE, country='unknown'),
]


@pytest.mark.parametrize("validator", [ProxyValidator()])
class TestFilterValidProxies:

    @pytest.mark.parametrize("proxies", [
        ["Not a proxy"],
        "Not a list",
    ])
    def test_filter_with_invalid_proxy_types(self, validator: ProxyValidator, proxies: List[Proxy]):
        valid_proxies = validator.filter_valid_proxies(proxies)
        assert valid_proxies == []

    @pytest.mark.parametrize("proxies", [PROXIES])
    def test_filter_with_invalid_proxies(self, validator: ProxyValidator, proxies: List[Proxy]):
        with aioresponses() as aio_mock:
            aio_mock.get(f'http://{validator._judge_domain}', exception=ClientConnectionError)
            aio_mock.get(f'https://{validator._judge_domain}', exception=ClientConnectionError)

            valid_proxies = validator.filter_valid_proxies(proxies)

            assert valid_proxies == []

    @pytest.mark.parametrize("proxies,limit", [(PROXIES, 1), (PROXIES, 0)])
    def test_filter_with_valid_proxies(self, validator: ProxyValidator, proxies: List[Proxy], limit: int):
        with aioresponses() as mocker:
            mocker.get(f'http://{validator._judge_domain}', status=200)
            mocker.get(f'https://{validator._judge_domain}', status=200)

            valid_proxies = validator.filter_valid_proxies(proxies, limit)

            assert len(valid_proxies) <= limit or limit == 0
