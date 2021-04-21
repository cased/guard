import requests
from os.path import expanduser, exists
import shutil
import hashlib
from git import Repo

from cguard.util import (
    home_dir,
    cguard_dir,
    log_level,
    output,
    get_program_from_git_config,
)

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
            return self._get_remote_url() + "/cli"

    def _get_heroku_metadata(self, directory, program_args):
        program = None
        result = None
        repo = Repo(directory)

        arg_arr = program_args.split()

        # Check the program args to see if any details were given specifically
        target_commands = ["--app", "-a", "--remote", "-r"]
        if any(x in target_commands for x in arg_arr):

            if "--app" in arg_arr:
                target = "--app"
            elif "-a" in arg_arr:
                target = "-a"
            elif "--remote" in arg_arr:
                target = "--remote"
            elif "-r" in arg_arr:
                target = "-r"

            target_index = arg_arr.index(target)
            index = target_index + 1

            if target == "-a" or target == "--app":
                # use the app name
                result = arg_arr[index]
            elif target == "-r" or target == "--remote":
                # remote was given, so look at the git config and get
                # the app name from the specific remote
                result = get_program_from_git_config(repo, arg_arr[index])

        else:
            # Program was not specified in any way, so get the name from
            # the default remote
            try:
                result = get_program_from_git_config(repo, "heroku")
            except:
                result = "unknown"

        return result

    def request_access(
        self,
        app_name,
        app_token,
        user_token,
        program_args,
        hostname,
        directory=None,
        reason=None,
    ):
        url = self._base_url() + "/sessions?user_token={}".format(user_token)

        metadata = {"hostname": hostname}
        if directory:
            metadata["directory"] = directory

        cased_metadata = {}

        # Special heroku metadata (todo: add as a generic plugin system). We try to get the
        # data through all options; if we fail, we still proceed with the operation.
        if app_name == "heroku":
            try:
                result = self._get_heroku_metadata(directory, program_args)
                heroku_app_name = result
                if heroku_app_name:
                    metadata["heroku_application"] = heroku_app_name
                    cased_metadata["heroku_application"] = heroku_app_name

            except Exception as e:
                output("Error getting heroku metadata: {}".format(e))

        data = {
            "guard_application_id": app_name,
            "command": program_args,
            "reason": reason,
            "metadata": metadata,
            "cased_metadata": cased_metadata,
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

    def record_session(self, session_id, app_token, user_token, recording):
        url = self._base_url() + "/sessions/{}/record?user_token={}".format(
            session_id, user_token
        )

        res = self.client.make_request(
            "put", url, data={"recording": recording}, key=app_token
        )
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
