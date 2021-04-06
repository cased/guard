from os.path import expanduser
import os

import json


def home_dir():
    return expanduser("~")


def cguard_dir():
    return home_dir() + "/.cguard"


def shims_dir():
    return cguard_dir() + "/shims"


def read_settings():
    try:
        filepath = cguard_dir() + "/" + "settings"
        with open(filepath, "r") as json_file:
            settings = json.load(json_file)

        return settings
    except:
        return {}


def poll_interval():
    settings = read_settings()
    interval = settings.get("poll") or 1
    return interval


def log_level():
    settings = read_settings()
    level = settings.get("log_level") or "info"
    return level


def environment():
    settings = read_settings()
    level = settings.get("environment") or "local"
    return level


def autosync():
    settings = read_settings()
    sync = settings.get("autosync") or True
    return sync


def output(msg):
    print("[cased 🔒] " + msg)


def debug(msg):
    print("[cased debug] " + msg)


def recording_enabled():
    state = os.getenv("CASED_RECORDING_ENABLED", False)
    if state == "1":
        return True
    else:
        return False


def get_program_from_git_config(repo, origin):
    sections = repo.config_reader().sections()
    header = 'remote "{}"'.format(origin)

    if header in sections:
        url = repo.config_reader().get_value(header, "url")
        result = url.split("/")[-1].replace(".git", "")
        return result
    else:
        raise Exception("No origin found.")