from libqtile import bar, widget
from libqtile.config import Screen
from core.colors import colors

widget_defaults = dict(
    font="sans",
    fontsize=13,
    padding=6,
    foreground=colors["fg"],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    highlight_method="line",
                    highlight_color=[colors["bg"], colors["bg"]],
                    this_current_screen_border=colors["accent"],
                    active=colors["fg"],
                    inactive=colors["inactive"],
                ),
                widget.Prompt(prompt="Run: ", foreground=colors["secondary"]),
                widget.WindowName(max_chars=50),
                widget.Systray(),
                widget.KeyboardLayout(
                    configured_keyboards=["us", "ru"],
                    display_map={"us": "EN", "ru": "RU"},
                    foreground=colors["accent"],
                ),
                widget.Sep(linewidth=1, padding=10, foreground=colors["inactive"]),
                widget.Sep(linewidth=1, padding=10, foreground=colors["inactive"]),
                widget.Clock(format="%d.%m.%Y | %H:%M", foreground=colors["secondary"]),
                widget.QuickExit(default_text=" [Выход] ", countdown_format="[{}]", foreground=colors["urgent"]),
            ],
            28,
            background=colors["bg"],
            margin=[4, 8, 0, 8], # Отступы панели от краев экрана
        ),
    ),
]
