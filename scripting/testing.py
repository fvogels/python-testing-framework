from contextlib import contextmanager
from scripting.assertions import AssertionFailure
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append


__pass_observers = create_dynamic_variable()
__skip_observers = create_dynamic_variable()
__fail_observers = create_dynamic_variable()


@contextmanager
def initialize_testing_environment():
    with dynamic_bind(__pass_observers, []), dynamic_bind(__skip_observers, []), dynamic_bind(__fail_observers, []):
        yield

@contextmanager
def observers(on_pass=None, on_fail=None, on_skip=None):
    def do_nothing():
        pass

    on_pass = on_pass or do_nothing
    on_fail = on_fail or do_nothing
    on_skip = on_skip or do_nothing

    with dynamic_append(__pass_observers, on_pass), dynamic_append(__fail_observers, on_fail), dynamic_bind(__skip_observers, on_skip):
        yield


def __shouldTestRun():
    return True


def __testPassed():
    for observer in __pass_observers.value:
        observer()


def __testFailed():
    for observer in __fail_observers.value:
        observer()


def __testSkipped():
    for observer in __skip_observers.value:
        observer()


def test():
    def receiver(f):
        if __shouldTestRun():
            try:
                f()
                __testPassed()

            except AssertionFailure:
                __testFailed()
        else:
            __testSkipped()

    return receiver
