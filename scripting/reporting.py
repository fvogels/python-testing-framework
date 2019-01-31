from contextlib import contextmanager, ExitStack
from scripting.dynamic import create_dynamic_variable, dynamic_bind
from scripting.testing import observers, skip_if


_tested_index = create_dynamic_variable()


def _increment_index():
    _tested_index.value += 1


@contextmanager
def reporting():
    def on_pass():
        # print(f'[{_tested_index.value}] PASS')
        _increment_index()

    def on_fail(e):
        print(f'[{_tested_index.value}] FAIL {str(e)}')
        _increment_index()

    def on_skip():
        _increment_index()


    with dynamic_bind(_tested_index, 0), observers(on_pass=on_pass, on_fail=on_fail, on_skip=on_skip):
        yield
