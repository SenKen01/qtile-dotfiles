from core.keys import keys, mouse
from core.groups import groups
from core.layouts import layouts, floating_layout
from core.screens import screens, widget_defaults, extension_defaults
import core.hooks

# Системные настройки Qtile
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"