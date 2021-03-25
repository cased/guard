import time

import time
import sys
import signal
from random import randint

from cguard.access_manager import CasedGuardAccessManager
from cguard.requestor import GuardRequestor
from cguard.util import read_settings, poll_interval, output


class Approval:
    def __init__(self):
        self.access_manager = CasedGuardAccessManager()
        self.settings = read_settings()

    def wait_for_approval(
        self, app_name, app_token, session_id, user_token, waiting_message
    ):
        def signal_handler(sig, frame):
            output("\nExiting and cancelling request: {}\n".format(session_id))
            requestor = GuardRequestor()
            requestor.cancel_session(app_token, session_id, user_token)
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        wait_text = waiting_message + " (id: {})".format(session_id)
        output(wait_text)
        while True:
            # poll the API for access granted
            state = self.access_manager.check_access(
                app_name, app_token, session_id, user_token
            )
            if state == "approved":
                msg = "✅ ACCESS APPROVED"
                output(msg)
                break
            elif state == "denied":
                msg = "🛑 ACCESS DENIED"
                output(msg)
                exit(1)
            elif state == "timed_out":
                msg = "🛑 TIME OUT"
                output(msg)
                exit(1)

            interval = poll_interval()
            time.sleep(interval)

        return True
