from src.ballyregan.providers import GeonodeProvider
from src.ballyregan.models import Proxy, Anonymities, Protocols

from tests.ballyregan.providers.common import ProviderTestData, ProviderTestCase

test_data = ProviderTestData(
    provider=GeonodeProvider(),
    expected_response={
        "data": [{
            "protocols": [Protocols.HTTP],
            "ip": "1.1.1.1",
            "port": 8080,
            "anonymityLevel": Anonymities.ELITE,
            "country": "Israel"
        }]
    },
    expected_proxies=[Proxy(
        protocol=Protocols.HTTP,
        ip="1.1.1.1",
        port=8080,
        anonymity=Anonymities.ELITE,
        country="Israel"
    )]
)


class TestGeonodeProvider(ProviderTestCase):

    test_data: ProviderTestData = test_data

    def test_gather_with_bad_responses(self, requests_mock):
        bad_responses = [
            dict(text='invalid proxy result'),
            dict(json={'invalid': {'proxy': {'result': 'schema'}}})
        ]

        super().test_gather_with_bad_responses(bad_responses, requests_mock)
