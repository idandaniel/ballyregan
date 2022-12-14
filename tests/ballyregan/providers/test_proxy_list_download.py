from src.ballyregan.providers import ProxyListDownloadProvider
from src.ballyregan.models import Proxy, Protocols

from tests.ballyregan.providers.common import ProviderTestData, ProviderTestCase

test_data = ProviderTestData(
    provider=ProxyListDownloadProvider(),
    expected_response="1.1.1.1:8080",
    expected_proxies=[
        Proxy(
            protocol=Protocols.HTTP,
            ip="1.1.1.1",
            port=8080
        ),
        Proxy(
            protocol=Protocols.HTTPS,
            ip="1.1.1.1",
            port=8080
        ),
        Proxy(
            protocol=Protocols.SOCKS4,
            ip="1.1.1.1",
            port=8080
        ),
        Proxy(
            protocol=Protocols.SOCKS5,
            ip="1.1.1.1",
            port=8080
        )
    ]
)


class TestProxyListDownloadProvider(ProviderTestCase):

    test_data: ProviderTestData = test_data

    def test_gather_with_bad_responses(self, requests_mock):
        bad_responses = [
            dict(text=''),
            dict(text='invalidproxyresultshouldfail'),
            dict(text='invalid:proxy:result:should:fail')
        ]

        super().test_gather_with_bad_responses(bad_responses, requests_mock)
