from os.path import expanduser

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
    print("[guard 🔒] " + msg)


def debug(msg):
    print("[guard debug] " + msg)