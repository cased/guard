import pytest

import cguard
from cguard.requestor import GuardRequestor
from cguard.test.util import mock_response


app_name = "test-app"
app_token = "12345"
user_token = "abcdefg"
program_args = "run"


class TestAPIRequestor(object):
    def test_request_access(self):
        requestor = GuardRequestor()

        with mock_response():
            assert (
                requestor.request_access(
                    app_name,
                    app_token,
                    user_token,
                    program_args,
                    "hostname",
                ).status_code
                == 200
            )

    def test_request_access_is_called_correctly(self):
        requestor = GuardRequestor()

        with mock_response():
            assert requestor.request_access(
                app_name,
                app_token,
                user_token,
                program_args,
                hostname="hostname",
            )

            cguard.requestor.HTTPClient.make_request.assert_called_with(
                "post",
                "https://api.cased.com/cli/sessions?user_token=abcdefg",
                data={
                    "guard_application_id": "test-app",
                    "metadata": {"hostname": "hostname"},
                    "cased_metadata": {},
                    "command": "run",
                    "reason": None,
                },
                key="12345",
            )

    def test_request_access_is_called_correctly_for_heroku_app(self):
        requestor = GuardRequestor()

        with mock_response():
            assert requestor.request_access(
                "heroku",
                app_token,
                user_token,
                program_args,
                hostname="hostname",
            )

            cguard.requestor.HTTPClient.make_request.assert_called_with(
                "post",
                "https://api.cased.com/cli/sessions?user_token=abcdefg",
                data={
                    "guard_application_id": "heroku",
                    "metadata": {
                        "hostname": "hostname",
                        "heroku_application": "unknown",
                    },
                    "cased_metadata": {
                        "heroku_application": "unknown",
                    },
                    "command": "run",
                    "reason": None,
                },
                key="12345",
            )

    def test_request_access_is_called_correctly_with_reason(self):
        requestor = GuardRequestor()

        with mock_response():
            assert requestor.request_access(
                app_name,
                app_token,
                user_token,
                program_args,
                "hostname",
                reason="reason for access",
            )

            cguard.requestor.HTTPClient.make_request.assert_called_with(
                "post",
                "https://api.cased.com/cli/sessions?user_token=abcdefg",
                data={
                    "guard_application_id": "test-app",
                    "metadata": {
                        "hostname": "hostname",
                    },
                    "cased_metadata": {},
                    "command": "run",
                    "reason": "reason for access",
                },
                key="12345",
            )

    def test_request_access_is_called_correctly_with_reason_and_directory(self):
        requestor = GuardRequestor()

        with mock_response():
            assert requestor.request_access(
                app_name,
                app_token,
                user_token,
                program_args,
                "hostname",
                directory="/Users/test/terraform",
                reason="reason for access",
            )

            cguard.requestor.HTTPClient.make_request.assert_called_with(
                "post",
                "https://api.cased.com/cli/sessions?user_token=abcdefg",
                data={
                    "guard_application_id": "test-app",
                    "metadata": {
                        "hostname": "hostname",
                        "directory": "/Users/test/terraform",
                    },
                    "cased_metadata": {},
                    "command": "run",
                    "reason": "reason for access",
                },
                key="12345",
            )

    def test_get_session(self):
        requestor = GuardRequestor()
        with mock_response():
            assert (
                requestor.get_session(
                    app_name, app_token, "session_1234", "user_12345"
                ).status_code
                == 200
            )

    def test_get_session_is_called_correctly(self):
        requestor = GuardRequestor()
        with mock_response():
            assert requestor.get_session(
                app_name, app_token, "session_1234", "user_12345"
            )

            cguard.requestor.HTTPClient.make_request.assert_called_with(
                "get",
                "https://api.cased.com/cli/sessions/session_1234?user_token=user_12345",
                data={
                    "guard_application_id": "test-app",
                },
                key="12345",
            )

    def test_cancel_session(self):
        requestor = GuardRequestor()
        with mock_response():
            assert (
                requestor.cancel_session(
                    app_token, "session_1234", "user_12345"
                ).status_code
                == 200
            )

    def test_cancel_session_is_called_correctly(self):
        requestor = GuardRequestor()
        with mock_response():
            assert requestor.cancel_session(app_token, "session_1234", "user_12345")

            cguard.requestor.HTTPClient.make_request.assert_called_with(
                "post",
                "https://api.cased.com/cli/sessions/session_1234/cancel?user_token=user_12345",
                key="12345",
            )

    def test_get_applications(self):
        requestor = GuardRequestor()
        with mock_response():
            assert requestor.get_applications(user_token, "local").status_code == 200

    def test_get_applications_is_called_correctly(self):
        requestor = GuardRequestor()
        with mock_response():
            assert requestor.get_applications(user_token, "local")

            cguard.requestor.HTTPClient.make_request.assert_called_with(
                "get",
                "https://api.cased.com/cli/applications?user_token=abcdefg&environment=local",
            )
