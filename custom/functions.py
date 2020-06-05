from libqtile.command import lazy
from libqtile import hook
from libqtile.config import Group
from custom.extra import TmuxSessionManager, InfiniteTimer
from threading import Timer
from time import sleep
import os

globals()['tmux_session_manager'] = TmuxSessionManager('alacritty -e')



def next_keyboard_layout(keyboard):
    def __inner(qtile_session):
        keyboard = __inner.__getattribute__('keyboard')
        if keyboard is not None:
            keyboard.cmd_next_keyboard()
        else:
            qtile_session.restart()
    __inner.keyboard = keyboard
    return lazy.function(__inner)

def poweroff(poff_widget, timeout = 5):
    def t(qtile):
        if t.started:
            t.timer.cancel()
        else:
            t.timer = Timer(t.timeout, qtile.stop)
            t.timer.start()
    t.timer = None
    t.started = False
    t.timeout = timeout
    return t

@lazy.function
def quit_qtile(qtile_session):
    try:
        # os.system('tmux kill-server')
        pass
    finally:
        lazy.shutdown()


@hook.subscribe.addgroup
def on_group_add(qtile, group):
    groups = globals().get('groups', None)
    if groups is None:
        groups = []
        globals()['groups'] = groups
    groups.append(group)


def change_wallpaper(wallpaper_obj, timeout):
    InfiniteTimer(
        timeout, wallpaper_obj.next_wallpaper).start()
