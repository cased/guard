import cguard

import pytest

from cguard.core.approval import Approval
from cguard.requestor import GuardRequestor
from cguard.test.util import mock_response

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


class TestApproval(object):
    def test_wait_for_approval_approved(self):
        with mock_response(json_data=approvial_json):
            approval = Approval()
            assert (
                approval.wait_for_approval(
                    "abc",
                    "token_123",
                    "guard_session_123",
                    "user_123",
                    "Waiting for approval..",
                )
                == True
            )


class TestApproval(object):
    def test_wait_for_approval_denied(self):
        with mock_response(json_data=denial_json):
            approval = Approval()
            with pytest.raises(SystemExit):
                # Assert the program exits on denied
                approval.wait_for_approval(
                    "abc",
                    "token_123",
                    "guard_session_123",
                    "user_123",
                    "Waiting for approval..",
                )
