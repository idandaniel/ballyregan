from src.ballyregan.providers import USProxyProvider
from src.ballyregan.models import Proxy, Anonymities, Protocols
from tests.ballyregan.providers.common import ProviderTestData, ProviderTestCase


html_response = """<html>
<head>
    <div class="table-responsive fpl-list">
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>IP Address</th>
                    <th>Port</th>
                    <th>Code</th>
                    <th class="hm">Country</th>
                    <th>Anonymity</th>
                    <th class="hm">Google</th>
                    <th class="hx">Https</th>
                    <th class="hm">Last Checked</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1.1.1.1</td>
                    <td>8080</td>
                    <td>IL</td>
                    <td class="hm">Israel</td>
                    <td>elite proxy</td>
                    <td class="hm">no</td>
                    <td class="hx">yes</td>
                    <td class="hm">16 secs ago</td>
                </tr>
            </tbody>
        </table>
    </div>
</html>"""

test_data = ProviderTestData(
    provider=USProxyProvider(),
    expected_response=html_response,
    expected_proxies=[Proxy(
        protocol=Protocols.HTTPS,
        ip="1.1.1.1",
        port=8080,
        anonymity=Anonymities.ELITE,
        country="Israel"
    )]
)


class TestFreeProxyListProvider(ProviderTestCase):

    test_data: ProviderTestData = test_data

    def test_gather_with_bad_responses(self, requests_mock):
        bad_responses = [
            dict(text='invalid proxy result'),
            dict(
                text="""<html>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th>I</th>
                                <th>P</th>
                                <th>C</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th>I</th>
                                <th>I</th>
                                <th>I</th>
                            </tr>
                        </tbody>
                    </table>
                </div>
                </html>"""
            ),
        ]

        super().test_gather_with_bad_responses(bad_responses, requests_mock)
