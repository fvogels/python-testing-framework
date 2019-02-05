from contextlib import contextmanager, ExitStack
from scripting.dynamic import create_dynamic_variable, dynamic_bind
from scripting.testing import observers, skip_if


_context = create_dynamic_variable()


@contextmanager
def reporting(on_pass, on_fail, on_skip):
    with observers(on_pass=on_pass, on_fail=on_fail, on_skip=on_skip):
        yield


@contextmanager
def context(key, value):
    new_context = { **_context.value, key: value }

    with dynamic_bind(_context, new_context):
        yield