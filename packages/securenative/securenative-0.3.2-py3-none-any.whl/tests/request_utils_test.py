import unittest

import requests_mock

from securenative.config.securenative_options import SecureNativeOptions
from securenative.utils.request_utils import RequestUtils


class RequestUtilsTest(unittest.TestCase):

    def test_proxy_headers_extraction_from_request(self):
        options = SecureNativeOptions(proxy_headers=['CF-Connecting-IP'])

        with requests_mock.Mocker(real_http=True) as request:
            request.headers = {
                "CF-Connecting-IP": "203.0.113.1"}

            client_ip = RequestUtils.get_client_ip_from_request(request, options)

            self.assertEqual(client_ip, "203.0.113.1")
