from contextlib import contextmanager
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append
from scripting.testing import test, skip
from scripting.fileutils import load_code
from scripting.assertions import assert_equal_results
from scripting.call_results import call_function
import sys


_reference_module = create_dynamic_variable()


@contextmanager
def reference_file(filename):
    module = load_code(filename, 'tested')

    with dynamic_bind(_reference_module, module):
        yield


def fetch_reference_implementation(identifier):
    if hasattr(_reference_module.value, identifier):
        return getattr(_reference_module.value, identifier)
    else:
        print(f'Could not find {identifier} in solution module')
        sys.exit(-1)


@contextmanager
def reference_based_testing(reference_implementation, tested_implementation):
    def testcase(*args):
        expected = call_function(reference_implementation, *args)

        @test()
        def _():
            actual = call_function(tested_implementation, *args)

            assert

    yield testcase
