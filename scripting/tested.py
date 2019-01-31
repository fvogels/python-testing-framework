from contextlib import contextmanager, ExitStack
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append
from scripting.testing import test, skip
from scripting.fileutils import load_code_from_file_into_module
from scripting.testing import skip_unless


_tested_module = create_dynamic_variable()
_active_tested_implementation = create_dynamic_variable()
_active_tested_implementation_id = create_dynamic_variable()


@contextmanager
def tested_module(module):
    with dynamic_bind(_tested_module, module):
        yield


@contextmanager
def tested_file(filename):
    module = load_code_from_file_into_module(filename, 'tested')

    with tested_module(module):
        yield


def fetch_tested_implementation(identifier):
    if hasattr(_tested_module.value, identifier):
        return getattr(_tested_module.value, identifier)
    else:
        with skip():
            return None


@contextmanager
def active_tested_implementation(implementation):
    with dynamic_bind(_active_tested_implementation, implementation):
        yield


@contextmanager
def active_tested_implementation_from_id(identifier):
    tested_implementation = fetch_tested_implementation(identifier)

    with dynamic_bind(_active_tested_implementation, tested_implementation), dynamic_bind(_active_tested_implementation_id, identifier), skip_unless(bool(tested_implementation)):
        yield


def current_active_tested_implementation():
    return _active_tested_implementation.value


def current_active_tested_implementation_id():
    return _active_tested_implementation_id.value
