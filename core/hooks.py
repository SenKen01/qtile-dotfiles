import os
import sys
import json
import subprocess
from libqtile import hook, qtile

sys.path.append(os.path.expanduser("~/.config/qtile"))
from scripts.session_manager import (
    SESSION_FILE,
    save_session,
    load_session,
    restore_workspace,
    apply_expected_geometry,
)

PENDING_SESSION = load_session()
RESTORED_GROUPS = set()
EXPECTED_WINDOWS = []


def smart_save():
    save_session(qtile)
    if PENDING_SESSION:
        current = load_session()
        for grp, apps in PENDING_SESSION.items():
            if grp not in current:
                current[grp] = apps
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2)


@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    subprocess.Popen([script])
    restore_workspace("1", PENDING_SESSION, RESTORED_GROUPS, EXPECTED_WINDOWS)


@hook.subscribe.startup
def setup_keyboard():
    subprocess.Popen(["killall", "-q", "ibus-daemon"])
    subprocess.Popen(["setxkbmap", "-layout", "us,ru", "-option", ""])


@hook.subscribe.setgroup
def on_group_change():
    grp = qtile.current_group.name
    restore_workspace(grp, PENDING_SESSION, RESTORED_GROUPS, EXPECTED_WINDOWS)


@hook.subscribe.client_new
def on_client_new(win):
    apply_expected_geometry(win, EXPECTED_WINDOWS)
    smart_save()


@hook.subscribe.client_killed
@hook.subscribe.float_change
def on_window_change(*args):
    smart_save()


@hook.subscribe.shutdown
def on_shutdown():
    smart_save()
