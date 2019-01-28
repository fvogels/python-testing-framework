from contextlib import contextmanager
from scripting.dynamic import create_dynamic_variable, dynamic_bind
from scripting.testing import observers, skip_if
from scripting.layering import create_layering


_layering = create_layering()


@contextmanager
def skip_after_fail():
    failure_detected = False

    def on_fail_or_skip(*_):
        nonlocal failure_detected
        failure_detected = True

    def skip_predicate():
        return failure_detected

    with _layering.add(), _layering.observers(on_fail=on_fail_or_skip, on_skip=on_fail_or_skip), skip_if(skip_predicate):
        yield


@contextmanager
def continue_after_fail():
    with _layering.add():
        yield
