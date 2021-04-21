import sys
import os
import io
import getpass
import socket
import time
import random
import signal
import subprocess
from subprocess import PIPE, STDOUT
import subprocess


from requests.exceptions import Timeout
from requests import get

from cguard.requestor.guard_requestor import GuardRequestor
from cguard.core.approval import Approval
from cguard.util import log_level, output, debug, recording_enabled


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
        output("Running under Cased.")

        def signal_handler(sig, frame):
            print("\n[cased 🔒] Exited.")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        reason = input("[cased 🔒] Please enter a reason for access: ")
        return reason

    def _handle_response(
        self, res, command, app_name, program_args, app_token, user_token
    ):
        status_code = res.status_code
        if status_code == 204:
            # ignored: no cased request required
            return

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
            elif error == "reauthenticate":
                requestor = GuardRequestor()
                res = requestor.identify_user()
                if res.status_code == 201:
                    data = res.json()
                    code = data.get("code")
                    url = data.get("url")

                    output(
                        "A new integration has been added to your Cased settings that requires authorization."
                    )
                    output(
                        "Please re-authorize your account to continue. Just visit and follow the integration instructions:"
                    )
                    print(url)
                    while True:
                        # poll the API for confirmation of connection
                        res = requestor.check_for_identification(code)
                        if res.status_code == 200:
                            msg = "✅ Authorized! Continuing.."
                            output(msg)
                            self.execute(program_args, app_token, False, user_token)
                            return
                        else:
                            time.sleep(2)
            else:
                output("Request error: {}".format(error))
                debug(str(status_code) + " " + str(body))
                sys.exit(1)

        elif status_code == 401:
            # Unauthorized
            output("Running under Cased.")
            output("Access denied: {}".format(body.get("message")))

            if log_level() == "debug":
                debug(str(status_code) + " " + str(body))
            sys.exit(0)

        elif status_code == 404:
            # App not found
            output(str(status_code) + " " + str(body))
            sys.exit(0)

        elif status_code == 408:
            # Session request was timed out
            output("Session request has already timed out. Please request a new one.")
            sys.exit(0)

        elif status_code == 410:
            # Session request was cancelled
            output("Session request has already been cancelled.")
            sys.exit(0)

        cmd = command.split(" ")

        # check if we should record the session
        application_settings = body.get("guard_application").get("settings")
        should_record = application_settings.get("record_output", False)

        if should_record and recording_enabled():
            output("Recording command output per configuration.")
            with subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            ) as res, io.BytesIO() as logfile:
                while True:
                    byte = res.stdout.read(1)
                    if byte:
                        sys.stdout.buffer.write(byte)
                        sys.stdout.flush()
                        logfile.write(byte)
                    else:
                        break

                logfile.seek(0)
                recording = logfile.read().decode("utf-8").replace("\n", "\r\n")

                session_id = body.get("id")

                requestor = GuardRequestor()
                requestor.record_session(session_id, app_token, user_token, recording)
        else:
            res = subprocess.run(cmd)

        return res.returncode

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
            cwd = os.getcwd()
            res = requestor.request_access(
                app_name, app_token, user_token, command, hostname, cwd, reason
            )
        except Timeout as e:
            if deny_if_unreachable == "1":
                output("Request timed-out. Per configuration, denying the request.")
                sys.exit(0)
            else:
                output("Request timed-out. Per configuration, allowing the request.")
                os.system(command)

        if log_level() == "debug":
            debug(res.text)

        retval = self._handle_response(
            res,
            command,
            app_name,
            program_args,
            app_token,
            user_token,
        )

        # run error hooks
        if retval != 0:
            # run registered error hooks
            pass

        return retval
