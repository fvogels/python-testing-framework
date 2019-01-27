from contextlib import contextmanager
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
    def do_nothing():
        pass

    on_pass = on_pass or do_nothing
    on_fail = on_fail or do_nothing
    on_skip = on_skip or do_nothing

    with dynamic_append(__pass_observers, on_pass), dynamic_append(__fail_observers, on_fail), dynamic_append(__skip_observers, on_skip):
        yield

@contextmanager
def skip_if(predicate):
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
    for observer in __pass_observers.value:
        observer()


def __test_failed():
    for observer in __fail_observers.value:
        observer()


def __test_skipped():
    for observer in __skip_observers.value:
        observer()


def test():
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
