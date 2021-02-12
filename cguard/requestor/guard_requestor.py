import requests
from os.path import expanduser, exists
import shutil
import hashlib

from cguard.util import home_dir, cguard_dir, log_level

DEFAULT_URL = "https://api.cased.com"


class HTTPClient:
    @classmethod
    def _cguard_hash(cls):
        filepath = shutil.which("cased")
        cguard = open(filepath, "rb")
        digest = hashlib.sha256(cguard.read()).hexdigest()
        cguard.close()
        return digest

    @classmethod
    def _check_for_server_error(cls, res):
        if res.status_code == 500:
            print(
                "Server error. Is a Slack channel configured for this Guard application?"
            )
            exit(1)

    @classmethod
    def make_request(cls, method, url, data=None, key=None):

        user_agent = "cased-guard"
        headers = {
            "User-Agent": user_agent,
            "X-Guard-Hash": cls._cguard_hash(),
            "Content-Type": "application/json",
        }

        if key:
            value = "Bearer " + key
            headers["Authorization"] = value

        if method == "get":
            res = requests.get(url, params=data, headers=headers, timeout=20)
        elif method == "post":
            res = requests.post(url, json=data, headers=headers, timeout=20)
        elif method == "put":
            res = requests.put(url, json=data, headers=headers, timeout=20)
        elif method == "patch":
            res = requests.patch(url, json=data, headers=headers, timeout=20)
        elif method == "head":
            res = requests.head(url, headers=headers, timeout=20)
        elif method == "delete":
            res = requests.delete(url, headers=headers, timeout=20)
        else:
            raise Exception(
                """Unsupported method given. This is likely a bug in the
                cased program. Please contact"""
            )

        cls._check_for_server_error(res)

        if log_level() == "debug":
            print(
                "Request sent. URL: {} | Params: {} | Headers: {}".format(
                    url, str(data), str(headers)
                )
            )

        return res


class GuardRequestor:
    def __init__(self, client=HTTPClient, url=None, *args, **kwargs):
        self.client = client
        self.url = url

    def _get_remote_url(self):
        final_url = None

        filepath = cguard_dir() + "/remote"
        if not exists(filepath):
            final_url = DEFAULT_URL
        else:
            with open(filepath, "r") as text_file:
                final_url = text_file.read()

        return final_url

    def _base_url(self):
        if self.url:
            return url
        else:
            return self._get_remote_url() + "/guard"

    def request_access(
        self, app_name, app_token, user_token, program_args, hostname, reason=None
    ):
        url = self._base_url() + "/sessions?user_token={}".format(user_token)
        data = {
            "guard_application_id": app_name,
            "command": program_args,
            "reason": reason,
            "metadata": {"hostname": hostname},
        }

        res = self.client.make_request("post", url, data=data, key=app_token)
        return res

    def get_session(self, app_name, app_token, session_id, user_token):
        url = self._base_url() + "/sessions/{}?user_token={}".format(
            session_id, user_token
        )
        data = {"guard_application_id": app_name}

        res = self.client.make_request("get", url, data=data, key=app_token)
        return res

    def cancel_session(self, app_token, session_id, user_token):
        url = self._base_url() + "/sessions/{}/cancel?user_token={}".format(
            session_id, user_token
        )

        res = self.client.make_request("post", url, key=app_token)
        return res

    def get_applications(self, user_token, environment):
        url = self._base_url() + "/applications?user_token={}&environment={}".format(
            user_token, environment
        )

        res = self.client.make_request("get", url)
        return res

    def identify_user(self):
        url = self._base_url() + "/applications/users/identify"

        res = self.client.make_request("post", url)
        return res

    def check_for_identification(self, identification_request_id):
        url = self._base_url() + "/applications/users/identify/{}".format(
            identification_request_id
        )

        res = self.client.make_request("get", url)
        return res
