from contextlib import contextmanager
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append
from scripting.testing import test, skip_unless
from scripting.assertions import assert_truthy, assert_falsey
from scripting.tested import fetch_tested_implementation
from scripting.reference import fetch_reference_implementation
from scripting.scoring import scale, all_or_nothing
import scripting.reference


@contextmanager
def reference_based_test(identifier):
    ref = fetch_reference_implementation(identifier)
    tested = fetch_tested_implementation(identifier)

    with scale(1), all_or_nothing(), scripting.reference.reference_based_test(ref, tested) as testcase, skip_unless(bool(tested)):
        yield testcase


@contextmanager
def regex_test(identifier):
    tested = fetch_tested_implementation(identifier)

    def match(string, message=None):
        @test()
        def _():
            nonlocal tested, message
            message = message or f"{identifier}: '{string}' should match regex"
            assert_truthy(tested(string), message=message)

    def no_match(string, message=None):
        @test()
        def _():
            nonlocal tested, message
            message = message or f"{identifier}: '{string}' should not match regex"
            assert_falsey(tested(string), message=message)

    with scale(1), all_or_nothing(), skip_unless(bool(tested)):
        yield (match, no_match)