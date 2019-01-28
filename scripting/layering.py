from contextlib import contextmanager
from scripting.dynamic import create_dynamic_variable, dynamic_bind
from scripting.testing import observers, skip_if


__layer = create_dynamic_variable()




@contextmanager
def initialize_layering():
    with dynamic_bind(__layer, 0):
        yield


@contextmanager
def layer():
    with dynamic_bind(__layer, __layer.value + 1):
        yield


@contextmanager
def layer_observers(on_pass=None, on_fail=None, on_skip=None):
    observer_layer = __layer.value

    def wrap(f):
        def observer():
            if __layer.value == observer_layer:
                f()

        return observer

    on_pass = wrap(on_pass) if on_pass else None
    on_fail = wrap(on_fail) if on_fail else None
    on_skip = wrap(on_skip) if on_skip else None

    with observers(on_pass=on_pass, on_fail=on_fail, on_skip=on_skip):
        yield

