from contextlib import contextmanager
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append
from scripting.testing import test, skip
from scripting.assertions import assert_equal_results
from scripting.tested import tested_implementation
from scripting.reference import reference_implementation
import scripting.reference


@contextmanager
def reference_based_test(identifier):
    with reference_implementation(identifier) as ref, tested_implementation(identifier) as tested, scripting.reference.reference_based_test(ref, tested) as testcase:
        yield testcase