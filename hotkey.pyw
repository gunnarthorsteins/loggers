"""Adapted from: https://bit.ly/39aEzrl
"""

from pynput import keyboard
import importlib

import worklog

global run_worklog

# The key combination to monitor
# See documentation: https://bit.ly/3pW0I2z
combinations = [{keyboard.Key.cmd, keyboard.Key.esc}]

# The currently active modifiers
current = set()


def reload_worklog():
    global run_worklog
    importlib.reload(worklog)
    run_worklog = worklog.Setup()


def on_press(key):
    if any([key in combo for combo in combinations]):
        current.add(key)
        if any(all(k in current for k in combo) for combo in combinations):
            pass


def on_release(key):
    if any(all(k in current for k in combo) for combo in combinations):
        current.remove(key)
        reload_worklog()
        run_worklog()


run_worklog = worklog.Setup()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
