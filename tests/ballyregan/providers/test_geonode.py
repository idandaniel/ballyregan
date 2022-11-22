import pytest

from src.ballyregan.providers import GeonodeProvider
from src.ballyregan.models import Proxy, Anonymities, Protocols

from tests.ballyregan.providers.common import IProviderTest, ProviderTestCase

provider_test_case = ProviderTestCase(
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


class TestGeonodeProvider(IProviderTest):

    test_case: ProviderTestCase = provider_test_case

    def test_gather_with_bad_responses(self, requests_mock):
        provider = self.test_case.provider

        bad_responses_to_mock = [
            dict(text='invalid proxy result'),
            dict(json={'invalid': {'proxy': {'result': 'schema'}}})
        ]

        for bad_response in bad_responses_to_mock:
            requests_mock.get(
                url=provider.url,
                status_code=200,
                **bad_response
            )

            gather_response = provider.gather()
            assert gather_response == []
