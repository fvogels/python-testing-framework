from contextlib import contextmanager, ExitStack
from scripting.assertions import AssertionFailure
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append

__pass_observers = create_dynamic_variable()
__skip_observers = create_dynamic_variable()
__fail_observers = create_dynamic_variable()
__skip_predicate = create_dynamic_variable()


@contextmanager
def initialize_testing_environment():
    with dynamic_bind(__pass_observers, []), dynamic_bind(__skip_observers, []), dynamic_bind(__fail_observers, []), dynamic_bind(__skip_predicate, lambda: False):
        yield

@contextmanager
def observers(on_pass=None, on_fail=None, on_skip=None):
    with ExitStack() as stack:
        if on_pass:
            stack.enter_context(dynamic_append(__pass_observers, on_pass))
        if on_fail:
            stack.enter_context(dynamic_append(__fail_observers, on_fail))
        if on_skip:
            stack.enter_context(dynamic_append(__skip_observers, on_skip))

        yield

@contextmanager
def skip_if(predicate):
    '''
    Given a boolean or predicate returning a boolean,
    if True the tests in this group will be skipped.
    '''
    # If necessary, turn boolean into predicate
    if type(predicate) == bool:
        value = predicate
        predicate = lambda: value

    previous = __skip_predicate.value

    def new_predicate():
        result = previous() or predicate()
        return result

    with dynamic_bind(__skip_predicate, new_predicate):
        yield

@contextmanager
def skip_unless(predicate):
    '''
    Given a boolean or predicate returning a boolean,
    if False the tests in this group will be skipped.
    '''
    # If necessary, turn boolean into predicate
    if type(predicate) == bool:
        value = predicate
        predicate = lambda: value

    def negated_predicate():
        return not predicate()

    with skip_if(negated_predicate):
        yield

def __should_test_run():
    # pylint: disable=E1102
    should_skip = (__skip_predicate.value)()
    return not should_skip


def __test_passed():
    '''
    Called whenever a test passes.
    Notifies pass-observers.
    '''
    for observer in reversed(__pass_observers.value):
        observer()


def __test_failed():
    '''
    Called whenever a test fails.
    Notifies fail-observers.
    '''
    for observer in reversed(__fail_observers.value):
        observer()


def __test_skipped():
    '''
    Called whenever a test is skipped.
    Notifies skip-observers.
    '''
    for observer in reversed(__skip_observers.value):
        observer()


def test():
    '''
    Decorator for tests
    '''
    def receiver(f):
        if __should_test_run():
            try:
                f()
                __test_passed()

            except AssertionFailure:
                __test_failed()
        else:
            __test_skipped()

    return receiver
