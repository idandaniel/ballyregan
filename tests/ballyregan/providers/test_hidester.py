import os

from src.ballyregan.providers import HidesterProvider
from src.ballyregan.models import Proxy, Anonymities, Protocols

class TestHidesterProvider():
    def test_gather_success(self, requests_mock):
        cwd = os.path.join(os.getcwd(), 'tests', 'ballyregan', 'providers')
        provider=HidesterProvider()

        with open(os.path.join(cwd, 'mock_pages', 'hidester.json'), 'r', encoding="utf-8") as html_file:
            requests_mock.get(
                url=provider.url,
                status_code=200,
                text=html_file.read()
            )
            gather_response = provider.gather()

            assert len(gather_response) == 5
            assert gather_response[0] == Proxy(
                    protocol=Protocols.SOCKS5,
                    ip='207.118.141.33',
                    port=54685,
                    anonymity=Anonymities.ELITE,
                    country='UNITED STATES'
            )
            assert gather_response[4] == Proxy(
                    protocol=Protocols.HTTP,
                    ip='207.154.230.96',
                    port=3128,
                    anonymity=Anonymities.TRANSPARENT,
                    country='UNITED STATES'
            )
