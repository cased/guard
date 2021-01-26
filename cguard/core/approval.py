import time

import time
import sys
import signal
from random import randint
from yaspin import yaspin

from cguard.access_manager import CasedGuardAccessManager
from cguard.requestor import GuardRequestor
from cguard.util import read_settings, poll_interval


class Approval:
    def __init__(self):
        self.access_manager = CasedGuardAccessManager()
        self.settings = read_settings()

    def wait_for_approval(
        self, app_name, app_token, session_id, user_token, waiting_message
    ):
        def signal_handler(sig, frame):
            print("\nExiting and cancelling request: {}\n".format(session_id))
            requestor = GuardRequestor()
            requestor.cancel_session(app_token, session_id, user_token)
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        wait_text = waiting_message + " (id: {})".format(session_id)
        with yaspin(text=wait_text, color="white") as spinner:
            while True:
                # poll the API for access granted
                state = self.access_manager.check_access(
                    app_name, app_token, session_id, user_token
                )
                if state == "approved":
                    msg = "✅ ACCESS APPROVED"
                    spinner.ok(msg)
                    break
                elif state == "denied":
                    spinner.fail("🛑 ACCESS DENIED")
                    exit(1)

                interval = poll_interval()
                time.sleep(interval)

        return True
