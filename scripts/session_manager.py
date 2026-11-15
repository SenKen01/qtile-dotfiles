import os
import json
import subprocess

SESSION_FILE = os.path.expanduser("~/.cache/qtile-session.json")

APP_MAP = {
    "firefox": "firefox",
    "firefox-esr": "firefox",
    "google-chrome": "google-chrome",
    "chromium": "chromium",
    "obsidian": "obsidian",
    "telegramdesktop": "telegram-desktop",
    "telegram-desktop": "telegram-desktop",
    "code": "code",
    "alacritty": "alacritty",
    "kitty": "kitty",
    "thunar": "thunar",
    "pavucontrol": "pavucontrol",
}


def resolve_cmd(win):
    wm_class = win.get_wm_class()
    if not wm_class:
        return None
    for cls in wm_class:
        key = cls.lower()
        if key in APP_MAP:
            return APP_MAP[key]
    return next(iter(wm_class)).lower()


def save_session(qtile):
    data = {}
    for group in qtile.groups:
        if not group.name.isdigit():
            continue
        win_list = []
        for win in group.windows:
            cmd = resolve_cmd(win)
            if not cmd:
                continue
            win_list.append({
                "cmd": cmd,
                "floating": win.floating,
                "x": win.x,
                "y": win.y,
                "width": win.width,
                "height": win.height,
            })
        if win_list:
            data[group.name] = win_list

    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
    tmp_file = f"{SESSION_FILE}.tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_file, SESSION_FILE)


def load_session():
    if not os.path.exists(SESSION_FILE):
        return {}
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def restore_workspace(group_name, pending_data, restored_groups, expected_windows):
    if group_name in restored_groups or group_name not in pending_data:
        return

    restored_groups.add(group_name)
    apps = pending_data.pop(group_name, [])

    for item in apps:
        cmd = item.get("cmd")
        if not cmd:
            continue
        item["target_group"] = group_name
        expected_windows.append(item)
        try:
            subprocess.Popen(cmd.split(), start_new_session=True)
        except Exception:
            pass


def apply_expected_geometry(win, expected_windows):
    cmd = resolve_cmd(win)
    if not cmd:
        return False

    for idx, item in enumerate(expected_windows):
        if item.get("cmd") == cmd:
            expected_windows.pop(idx)
            target = item.get("target_group")
            if target:
                win.togroup(target, switch_group=False)
            if item.get("floating"):
                win.floating = True
                win.place(
                    item.get("x", 100),
                    item.get("y", 100),
                    item.get("width", 800),
                    item.get("height", 600),
                    2,
                    None,
                )
            return True
    return False
