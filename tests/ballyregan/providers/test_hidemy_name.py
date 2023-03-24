import os

from src.ballyregan.providers import HidemynameProvider
from src.ballyregan.models import Proxy, Anonymities, Protocols

class TestHidemyNameProvider():
    def test_gather_success(self, requests_mock):
        cwd = os.path.join(os.getcwd(), 'tests', 'ballyregan', 'providers')
        provider=HidemynameProvider()

        with open(os.path.join(cwd, 'mock_pages', 'hidemy_name.html'), 'r', encoding="utf-8") as html_file:
            requests_mock.get(
                url=provider.url,
                status_code=200,
                text=html_file.read()
            )
            gather_response = provider.gather()

            assert len(gather_response) == 64
            assert gather_response[0] == Proxy(
                    protocol=Protocols.HTTP,
                    ip='37.32.22.223',
                    port=80,
                    anonymity=Anonymities.ELITE,
                    country='Iran'
            )
            assert gather_response[63] == Proxy(
                    protocol=Protocols.HTTP,
                    ip='152.67.64.111',
                    port=80,
                    anonymity=Anonymities.ANONYMOUS,
                    country='Switzerland Zurich'
            )
