from contextlib import contextmanager, ExitStack
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append
from scripting.testing import test, skip
from scripting.fileutils import load_code_from_file_into_module


_tested_module = create_dynamic_variable()


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
