import os

from src.ballyregan.providers import ProxyscrapeProvider
from src.ballyregan.models import Proxy, Anonymities, Protocols

class TestProxyscrapeProvider():
    def test_gather_success(self, requests_mock):
        cwd = os.path.join(os.getcwd(), 'tests', 'ballyregan', 'providers')
        provider=ProxyscrapeProvider()

        with open(os.path.join(cwd, 'mock_pages', 'proxyscrape.txt'), 'r', encoding="utf-8") as txt_file:
            requests_mock.get(
                url=provider.url,
                status_code=200,
                text=txt_file.read()
            )
            gather_response = provider.gather()

            assert len(gather_response) == 120
            assert gather_response[0] == Proxy(
                    protocol=Protocols.SOCKS5,
                    ip='69.194.181.6',
                    port=7497,
                    anonymity=Anonymities.ANONYMOUS,
                    country='unknown'
            )
            assert gather_response[119] == Proxy(
                    protocol=Protocols.HTTP,
                    ip='5.133.30.141',
                    port=5678,
                    anonymity=Anonymities.ELITE,
                    country='unknown'
            )
