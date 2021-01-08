import os
import subprocess

from typing import List  
from libqtile.layout import MonadTall, MonadWide, Max, Floating, bsp
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Screen, Match
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook

mod = "mod4"
terminal = "alacritty"
browser = "chromium"

keys = [
    # launch and kill programs
    Key([mod],"Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod],"b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod],"f", lazy.spawn("nemo"), desc="Launch filemanager"),
    Key([mod],"p", lazy.spawn("pavucontrol"), desc="Launch pulseaudio manager"),
    
    Key([mod],"q", lazy.window.kill(), desc="Kill focused windows"),

    # qtile commands
    Key([mod],"r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "shift"],"q", lazy.shutdown(), desc="Quit qtile"),

    # run prompts 
    Key([mod],"d", lazy.spawn("rofi -show drun"), desc="Launch program launcher"),
    Key([mod],"Tab", lazy.spawn("rofi -show window"), desc="Launch rofi window mode"),

    # shift window focus
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    # move windows
    Key([mod, "control"], "j", lazy.layout.shuffle_down()),
    Key([mod, "control"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.shuffle_left()),
    Key([mod, "control"], "l", lazy.layout.shuffle_right()),
    # resize windows
    Key([mod, "shift"], "h", lazy.layout.shrink()),
    Key([mod, "shift"], "l", lazy.layout.grow()),
    Key([mod, "shift"], "m", lazy.layout.maximize()),
    Key([mod, "shift"], "r", lazy.layout.normalize()),
    # layout modifires
    Key([mod], "n", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "control"], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "control"], "t", lazy.window.toggle_floating()),
    # Change to other screen
    Key([mod], "u",      lazy.to_screen(0)),
    Key([mod], "i",      lazy.to_screen(1)),

]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod], 
                i.name, 
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name)
            ),

            Key(
                [mod, "shift"], 
                i.name, 
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name)
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                # bar
                desc="move focused window to group {}".format(i.name),
            ),
        ]
    )

# borders
border_focus = "#5af78e"
border_width = 2
margin = 6
single_border_width = 0
single_margin = 6

# bar
layouts = [
    MonadTall(
        border_focus=border_focus,
        border_width=border_width,
        margin=margin,
        single_border_width=single_border_width,
        single_margin=single_margin,
        name="Tall",
    ),
    MonadWide(
        border_focus=border_focus,
        border_width=border_width,
        margin=margin,
        single_border_width=single_border_width,
        single_margin=single_margin,
        name="wide",
    ),
    bsp.Bsp(
        border_focus=border_focus,
        border_width=border_width,
        margin=margin,
        single_border_width=single_border_width,
        single_margin=single_margin,
        name="Grid",
    ),
    Max(
        border_focus=border_focus,
        border_width=border_width,
        margin=single_margin,
        single_border_width=0,
        single_margin=0,
        name="Full",
    ),
]

widget_defaults = dict(
    font="Hack Regular",
    fontsize=13,
    padding=3,
)


screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                widget.QuickExit(),
            ],
            30,
        ),
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(),
                widget.WindowName(),
                widget.Clock(),
            ],
            30,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# auto shifting programs to specified groups
groups = [
    Group("1"),
    Group("2", matches=[Match(wm_class=["chromium"])]),
    #Group("3", matches=[Match(wm_class=["Alacritty"])]),
    Group("4", matches=[Match(wm_class=["discord"])]),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
    Group("9"),
]

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
