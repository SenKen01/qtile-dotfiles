from libqtile.config import Group, Key
from libqtile.lazy import lazy
from core.keys import mod, keys

groups = [Group(i) for i in "123456"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Перейти на стол {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Перенести окно на стол {i.name}"),
    ])