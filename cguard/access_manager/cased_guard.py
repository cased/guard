from cguard.access_manager.access_manager import AccessManager
from cguard.requestor import GuardRequestor


class CasedGuardAccessManager(AccessManager):
    def __init__(self):
        self.requestor = GuardRequestor()

    def check_access(self, app_name, app_token, session_id, user_token):
        res = self.requestor.get_session(app_name, app_token, session_id, user_token)
        state = res.json().get("state")
        return state
