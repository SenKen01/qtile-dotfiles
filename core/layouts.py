from libqtile import layout
from libqtile.config import Match
from core.colors import colors

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors["accent"],
    "border_normal": colors["inactive"],
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
]

floating_layout = layout.Floating(
    border_focus=colors["secondary"],
    border_normal=colors["inactive"],
    border_width=2,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
)
