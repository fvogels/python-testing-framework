from contextlib import contextmanager
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append
from scripting.testing import test, skip_unless
from scripting.assertions import assert_truthy, assert_falsey
from scripting.tested import fetch_tested_implementation
from scripting.reference import fetch_reference_implementation
from scripting.scoring import scale
import scripting.reference


@contextmanager
def reference_based_test(identifier):
    ref = fetch_reference_implementation(identifier)
    tested = fetch_tested_implementation(identifier)

    with scale(1), scripting.reference.reference_based_test(ref, tested) as testcase, skip_unless(bool(tested)):
        yield testcase


@contextmanager
def regex_test(identifier):
    tested = fetch_tested_implementation(identifier)

    def match(string):
        nonlocal tested
        assert_truthy(tested(string), message=f"{id}: '{string}' should match regex")

    def no_match(string):
        nonlocal tested
        assert_falsey(tested(string), message=f"{id}: '{string}' should not match regex")

    with skip_unless(bool(tested)):
        yield (match, no_match)