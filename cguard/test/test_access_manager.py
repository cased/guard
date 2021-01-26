import cguard

from cguard.access_manager import CasedGuardAccessManager
from cguard.requestor import GuardRequestor
from cguard.test.util import mock_response


requested_json = {
    "id": "guard_session_123",
    "state": "requested",
    "requester": {"id": "user_123", "email": "user@example.com"},
    "guard_application": {
        "id": "guard_application_abc",
        "name": "abc",
        "settings": {"message_of_the_day": None, "reason_required": True},
    },
}

approvial_json = {
    "id": "guard_session_123",
    "state": "approved",
    "requester": {"id": "user_123", "email": "user@example.com"},
    "guard_application": {
        "id": "guard_application_abc",
        "name": "abc",
        "settings": {"message_of_the_day": None, "reason_required": True},
    },
}

denial_json = {
    "id": "guard_session_123",
    "state": "denied",
    "requester": {"id": "user_123", "email": "user@example.com"},
    "guard_application": {
        "id": "guard_application_abc",
        "name": "abc",
        "settings": {"message_of_the_day": None, "reason_required": True},
    },
}


class TestAccessManager(object):
    def test_access_manager_creation(self):
        access_manager = CasedGuardAccessManager()
        assert access_manager.requestor.__class__ == GuardRequestor

    def test_access_manager_check_access_requested(self):
        with mock_response(json_data=requested_json):
            access_manager = CasedGuardAccessManager()

            assert (
                access_manager.check_access(
                    "app_123", "token_123", "session_abc", "user_abc"
                )
                == "requested"
            )

    def test_access_manager_check_access_approval(self):
        with mock_response(json_data=approvial_json):
            access_manager = CasedGuardAccessManager()

            assert (
                access_manager.check_access(
                    "app_123", "token_123", "session_abc", "user_abc"
                )
                == "approved"
            )

    def test_access_manager_check_access_denied(self):
        with mock_response(json_data=denial_json):
            access_manager = CasedGuardAccessManager()

            assert (
                access_manager.check_access(
                    "app_123", "token_123", "session_abc", "user_abc"
                )
                == "denied"
            )