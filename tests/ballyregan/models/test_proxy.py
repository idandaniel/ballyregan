import pytest

from src.ballyregan import Proxy
from src.ballyregan.models import Anonymities, Protocols


IP = '1.1.1.1'
PORT = 8080


@pytest.mark.parametrize('proxy', [
    Proxy(
        protocol=Protocols.HTTPS,
        ip=IP,
        port=PORT,
        anonymity=Anonymities.ELITE
    )
])
def test_proxy_to_string(proxy: Proxy):
    assert str(proxy) == f"{proxy.protocol}://{proxy.ip}:{proxy.port}"


def test_proxy_anonymities_values():
    anonymities = [
        'elite', 'transparent', 'unknown', 'anonymous'
    ]
    assert Anonymities.values().sort() == anonymities.sort()
