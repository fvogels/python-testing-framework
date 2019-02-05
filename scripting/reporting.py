from contextlib import contextmanager, ExitStack
from scripting.dynamic import create_dynamic_variable, dynamic_bind
from scripting.testing import observers, skip_if


_context = create_dynamic_variable()


def _do_nothing():
    pass


@contextmanager
def reporting(on_pass = _do_nothing, on_fail = _do_nothing, on_skip = _do_nothing):
    with dynamic_bind(_context, {}), observers(on_pass=on_pass, on_fail=on_fail, on_skip=on_skip):
        yield


@contextmanager
def context(key, value):
    new_context = { **_context.value, key: value }

    with dynamic_bind(_context, new_context):
        yield


def current_context():
    return _context.value


def format_context(context = None):
    context = context or current_context()

    return "".join( f'{key}: {value}\n' for key, value in context.items() )