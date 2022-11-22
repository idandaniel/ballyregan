from abc import ABC, abstractmethod

from tests.ballyregan.providers.common import ProviderTestCase


class IProviderTest(ABC):

    test_case: ProviderTestCase

    @abstractmethod
    def test_gather_with_bad_responses(self, requests_mock):
        pass

    def test_gather_with_bad_status_codes(self, requests_mock):
        provider = self.test_case.provider

        fail_status_codes = [400, 500]

        for code in fail_status_codes:
            requests_mock.get(
                url=provider.url,
                status_code=code
            )

            gather_response = provider.gather()
            assert gather_response == []


    def test_gather_success(self, requests_mock):
        provider = self.test_case.provider

        requests_mock.get(
            url=provider.url,
            status_code=200,
            **{self.test_case.expected_response_type: self.test_case.expected_response}
        )

        gather_response = provider.gather()
        assert gather_response == self.test_case.expected_proxies
