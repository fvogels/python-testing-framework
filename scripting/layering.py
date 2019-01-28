from contextlib import contextmanager
from scripting.dynamic import create_dynamic_variable, dynamic_bind
from scripting.testing import observers, skip_if


@contextmanager
def _layer_observers(counter, on_pass=None, on_fail=None, on_skip=None):
    observer_layer = counter.value

    def wrap(f):
        def observer():
            if counter.value == observer_layer:
                f()

        return observer

    on_pass = wrap(on_pass) if on_pass else None
    on_fail = wrap(on_fail) if on_fail else None
    on_skip = wrap(on_skip) if on_skip else None

    with observers(on_pass=on_pass, on_fail=on_fail, on_skip=on_skip):
        yield


@contextmanager
def _add_layer(counter):
    with dynamic_bind(counter, counter.value + 1):
        yield


class _Layering:
    def __init__(self):
        self.__counter = create_dynamic_variable().bind(0)

    def add(self):
        return _add_layer(self.__counter)

    def observers(self, on_pass=None, on_fail=None, on_skip=None):
        return _layer_observers(self.__counter, on_pass=on_pass, on_fail=on_fail, on_skip=on_skip)


def create_layering():
    return _Layering()

