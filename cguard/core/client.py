import sys
import os
import getpass
import socket

from requests.exceptions import Timeout
from requests import get

from cguard.requestor.guard_requestor import GuardRequestor
from cguard.core.approval import Approval
from cguard.util import log_level, output, debug


class Client:
    def __init__(self, bin_name):
        self.bin_name = bin_name

    def _environment(self):
        username = getpass.getuser()
        hostname = socket.gethostname()

        return (username, hostname)

    def _hostname(self):
        return socket.gethostname()

    def _prompt_for_reason(self):
        output("Running under Cased Guard.")
        reason = input("[guard 🔒] Please enter a reason for access: ")
        return reason

    def _handle_response(
        self, res, command, app_name, program_args, app_token, user_token
    ):
        status_code = res.status_code
        body = res.json()

        if status_code == 200:
            # approved: either the session is active or auto-approval is on
            output("Logging action to Cased audit trail.")

        elif status_code == 201:
            # approval required
            session_id = body.get("id")
            application_settings = body.get("guard_application").get("settings")
            waiting_message = (
                application_settings.get("message_of_the_day")
                or "Approval request sent.."
            )

            Approval().wait_for_approval(
                app_name, app_token, session_id, user_token, waiting_message
            )

        elif status_code == 400:
            # Either malformed or reason is required
            error = body.get("error")
            if error == "reason_required":
                reason = self._prompt_for_reason()
                self.execute(program_args, app_token, False, user_token, reason)
                return
            else:
                output("Request error: {}".format(error))
                debug(str(status_code) + " " + str(body))
                exit(1)

        elif status_code == 401:
            # Unauthorized
            output("Running under Cased Guard.")
            output("Access denied: {}".format(body.get("message")))

            if log_level() == "debug":
                debug(str(status_code) + " " + str(body))
            exit(0)

        elif status_code == 404:
            # App not found
            output(str(status_code) + " " + str(body))
            exit(0)

        elif status_code == 410:
            # Session request was cancelled
            output("Session request has already been cancelled.")
            exit(0)

        # call underlying
        os.system(command)

    def execute(
        self, program_args, app_token, deny_if_unreachable, user_token, reason=None
    ):
        username, hostname = self._environment()

        # Send request to API
        requestor = GuardRequestor()

        app_name = os.path.basename(os.path.normpath(self.bin_name))

        command = self.bin_name + " " + program_args

        # We wont have a session id (this is just an invocation of the program),
        # so we still need to request a new session. However, if we receive a
        # 200 (the server controls the session time) we'll be auto-approved.
        try:
            res = requestor.request_access(
                app_name, app_token, user_token, command, hostname, reason
            )
        except Timeout as e:
            if deny_if_unreachable == "1":
                output("Request timed-out. Per configuration, denying the request.")
                exit(0)
            else:
                output("Request timed-out. Per configuration, allowing the request.")
                os.system(command)

        if log_level() == "debug":
            debug(res.text)

        self._handle_response(
            res,
            command,
            app_name,
            program_args,
            app_token,
            user_token,
        )
