from typing import List

from tests.ballyregan.providers.common import ProviderTestCase


class ProviderTest:

    test_case: ProviderTestCase

    def test_gather_with_bad_responses(self, bad_responses: List[dict], requests_mock):
        provider = self.test_case.provider

        for bad_response in bad_responses:
            requests_mock.get(
                url=provider.url,
                status_code=200,
                **bad_response
            )

            gather_response = provider.gather()
            assert gather_response == []

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
