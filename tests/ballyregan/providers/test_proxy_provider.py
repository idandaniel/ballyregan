from typing import Union
from dataclasses import dataclass

import pytest

from src.ballyregan import Proxy
from src.ballyregan.models import Anonymities, Protocols
from src.ballyregan.providers import IProxyProvider, FreeProxyListProvider, GeonodeProvider, ProxyListDownloadProvider, SSLProxiesProvider, USProxyProvider

IP = '1.1.1.1'
PORT = 8080
COUNTRY = 'Israel'
ANONYMITY = Anonymities.ELITE


@dataclass
class ProviderTestCase:
    provider: IProxyProvider
    expected_response: Union[str, dict]
    expected_proxies: Proxy

    def __post_init__(self) -> None:
        if isinstance(self.expected_response, dict):
            self.expected_response_type = 'json'
        else:
            self.expected_response_type = 'text'


provider_test_cases = [
    ProviderTestCase(
        provider=GeonodeProvider(),
        expected_response={
            'data': [
                {
                    'protocols': [Protocols.HTTPS],
                    'ip': IP,
                    'port': PORT,
                    'country': COUNTRY,
                    'anonymityLevel': ANONYMITY
                }
            ]
        },
        expected_proxies=[
            Proxy(
                protocol=Protocols.HTTPS,
                ip=IP,
                port=PORT,
                anonymity=ANONYMITY,
                country=COUNTRY
            )
        ]
    ),
    ProviderTestCase(
        provider=ProxyListDownloadProvider(),
        expected_response=f"{IP}:{PORT}",
        expected_proxies=[
            Proxy(
                protocol=Protocols.HTTP,
                ip=IP,
                port=PORT
            ),
            Proxy(
                protocol=Protocols.HTTPS,
                ip=IP,
                port=PORT
            ),
            Proxy(
                protocol=Protocols.SOCKS4,
                ip=IP,
                port=PORT
            ),
            Proxy(
                protocol=Protocols.SOCKS5,
                ip=IP,
                port=PORT
            )
        ]
    ),
]


@pytest.mark.parametrize('provider_test_case', provider_test_cases)
class TestProxyProvider:

    def test_gather_with_bad_status_codes(self, provider_test_case: ProviderTestCase, requests_mock):
        provider = provider_test_case.provider

        fail_status_codes = [400, 500]

        for code in fail_status_codes:
            requests_mock.get(
                url=provider.url,
                status_code=code
            )

            gather_response = provider.gather()
            assert gather_response == []

    def test_gather_with_bad_responses(self, provider_test_case: ProviderTestCase, requests_mock):
        provider = provider_test_case.provider

        bad_responses_to_mock = [
            dict(text=''),
            dict(text='should:faild:gather'),
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

    def test_gather_success(self, provider_test_case: ProviderTestCase, requests_mock):
        provider = provider_test_case.provider

        requests_mock.get(
            url=provider.url,
            status_code=200,
            **{provider_test_case.expected_response_type: provider_test_case.expected_response}
        )

        gather_response = provider.gather()
        assert gather_response == provider_test_case.expected_proxies
