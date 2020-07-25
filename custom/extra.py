from contextlib import redirect_stdout
from functools import wraps
from itertools import cycle
from libqtile.command import lazy
from os import system
from subprocess import check_output
from threading import Thread
import time


def one_call(func):
    """
    Makes function call just once,
    getting its return value and caching it.

    WARNING: No matter which parameters you modify,
    function return is function call. Can be used for
    avoiding the initialization of new objects.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return wrapper.return_value
        except AttributeError:
            wrapper.return_value = func(*args, **kwargs)
            return wrapper.return_value

    return wrapper


class InfiniteTimer(Thread):
    """
    A timer that runs again and again,
    indifinetly
    """

    def __init__(
        self, timeout, callback, *args, **kwargs,
    ):
        super(InfiniteTimer, self).__init__()
        self.kwargs = kwargs
        self.args = args
        self.timeout = timeout
        self.callback = callback
        self.running = True

    def cancel(self):
        self.running = False

    def run(self):
        while self.running:
            time.sleep(self.timeout)
            self.callback(
                *self.args, **self.kwargs,
            )
