import os
import inspect
import json
import icon
import pkexec

server = None
cert = None
keep_passwd = False
elevate = None
TRAY_ICON = os.path.dirname(inspect.getfile(icon)) + '/lockWithe.png'
TRAY_ICON_OK = os.path.dirname(inspect.getfile(icon)) + '/lockGreen.png'
TRAY_ICON_ERROR = os.path.dirname(inspect.getfile(icon)) + '/lockRed.png'
POST_UP = os.path.dirname(inspect.getfile(pkexec)) + '/post-up.policy'
UP = os.path.dirname(inspect.getfile(pkexec)) + '/up.policy'
POST_DOWN = os.path.dirname(inspect.getfile(pkexec)) + '/post-down.policy'
DOWN = os.path.dirname(inspect.getfile(pkexec)) + '/down.policy'
USER_POST_UP = None
USER_POST_DOWN = None


def init():
    with open(os.environ["HOME"] + "/.config/snxtray.json") as json_file:
        data = json.load(json_file)
        globals()["server"] = data["server"]
        globals()["cert"] = data["cert"]
        if "keep_passwd" in data.keys():
            globals()["keep_passwd"] = data["keep_passwd"]
        if "elevate" in data.keys():
            globals()["elevate"] = data["elevate"]
        if "post-up" in data.keys():
            globals()["USER_POST_UP"] = data["post-up"]
        if "post-down" in data.keys():
            globals()["USER_POST_DOWN"] = data["post-down"]
