# The following import is to let tests run in Python 2.7 which does not have
# unittest.mocks which was introduced in Python 3.3. Some of our projects still run
# Python 2.7 so support is necessary for now
try:
    from unittest import mock
except ImportError:
    import mock
from unittest import TestCase

from mercuryclient.api import MercuryApi


class ExperianMixinTest(TestCase):
    def setUp(self):
        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)
        self.get_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._get_json_http_request"
        ).start()
        self.addCleanup(self.get_api_mock.stop)
        self.sleep_mock = mock.patch("mercuryclient.mixins.experian.time.sleep").start()
        self.sleep_mock.return_value = None
        self.addCleanup(self.get_api_mock.stop)

    def test_request_experian_report(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        application_data = {"enquiry_reason": "AUTO_LOAN", "amount_financed": 23000}
        client.request_experian_report(application_data, "some_profile")

        self.post_api_mock.assert_called_with(
            "api/v1/experian/",
            data={
                "profile": "some_profile",
                "enquiry_reason": "AUTO_LOAN",
                "amount_financed": 23000,
            },
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        application_data = {"enquiry_reason": "AUTO_LOAN", "amount_financed": 23000}
        with self.assertRaises(Exception):
            client.request_experian_report(application_data, "some_profile")

    def test_request_api_succeeds_if_status_code_success(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)

        application_data = {"enquiry_reason": "AUTO_LOAN", "amount_financed": 23000}
        response = client.request_experian_report(application_data, "some_profile")
        self.assertEqual(response["request_id"], "random_string")
        self.assertEqual(response["status"], "Success")

    def test_response_experian_report(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        self.get_api_mock.return_value = ("random_string", mock_response)
        client.get_experian_response("random_string")

        self.get_api_mock.assert_called_with(
            "api/v1/experian/",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )

    def test_response_exception_raised_if_status_code_error(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.get_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            client.get_experian_response("random_string")

    def test_response_api_succeeds_if_status_code_success(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json = mock.MagicMock()
        mock_response.json.return_value = {"status": "SUCCESS"}
        self.get_api_mock.return_value = ("random_string", mock_response)

        response = client.get_experian_response("random_string")
        self.assertEqual(response["request_id"], "random_string")
        self.assertEqual(response["status"], "Success")
        self.assertEqual(response["response"]["status"], "SUCCESS")

    def test_entire_request_response_flow(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "SUCCESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        application_data = {"enquiry_reason": "AUTO_LOAN", "amount_financed": 23000}
        response = client.fetch_experian_report(application_data, "some_profile")

        self.post_api_mock.assert_called_with(
            "api/v1/experian/",
            data={
                "profile": "some_profile",
                "enquiry_reason": "AUTO_LOAN",
                "amount_financed": 23000,
            },
            send_request_id=True,
            add_bearer_token=True,
        )
        self.get_api_mock.assert_called_with(
            "api/v1/experian/",
            headers={"X-Mercury-Request-Id": "random_string"},
            send_request_id=False,
            add_bearer_token=True,
        )
        self.sleep_mock.assert_called_with(15)
        self.assertEqual(response["status"], "SUCCESS")

    def test_entire_request_response_flow_failure(self):
        client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        mock_post_response = mock.MagicMock()
        mock_post_response.status_code = 201
        mock_get_response = mock.MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.json = mock.MagicMock()
        mock_get_response.json.return_value = {"status": "IN_PROGRESS"}
        self.post_api_mock.return_value = ("random_string", mock_post_response)
        self.get_api_mock.return_value = ("random_string", mock_get_response)

        application_data = {"enquiry_reason": "AUTO_LOAN", "amount_financed": 23000}
        with self.assertRaises(Exception):
            response = client.fetch_experian_report(application_data, "some_profile")
