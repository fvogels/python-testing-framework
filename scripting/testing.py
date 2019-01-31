from contextlib import contextmanager, ExitStack
from scripting.assertions import AssertionFailure
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append


_pass_observers = create_dynamic_variable().bind([])
_skip_observers = create_dynamic_variable().bind([])
_fail_observers = create_dynamic_variable().bind([])
_skip_condition = create_dynamic_variable().bind(lambda: False)


@contextmanager
def observers(on_pass=None, on_fail=None, on_skip=None):
    with ExitStack() as stack:
        if on_pass:
            stack.enter_context(dynamic_append(_pass_observers, on_pass))
        if on_fail:
            stack.enter_context(dynamic_append(_fail_observers, on_fail))
        if on_skip:
            stack.enter_context(dynamic_append(_skip_observers, on_skip))

        yield

@contextmanager
def skip_if(condition):
    '''
    Given a boolean or function returning a boolean,
    if True the tests in this group will be skipped.
    '''
    # If necessary, turn boolean into function
    if type(condition) == bool:
        value = condition
        condition = lambda: value

    previous = _skip_condition.value

    def new_condition():
        result = previous() or condition()
        return result

    with dynamic_bind(_skip_condition, new_condition):
        yield


@contextmanager
def skip_unless(condition):
    '''
    Given a boolean or function returning a boolean,
    if False the tests in this group will be skipped.
    '''
    # If necessary, turn boolean into function
    if type(condition) == bool:
        value = condition
        condition = lambda: value

    def negated_condition():
        return not condition()

    with skip_if(negated_condition):
        yield


@contextmanager
def skip():
    with skip_if(True):
        yield


def _should_test_run():
    # pylint: disable=E1102
    should_skip = (_skip_condition.value)()
    return not should_skip


def _test_passed():
    '''
    Called whenever a test passes.
    Notifies pass-observers.
    '''
    for observer in reversed(_pass_observers.value):
        observer()


def _test_failed(exception):
    '''
    Called whenever a test fails.
    Notifies fail-observers.
    '''
    for observer in reversed(_fail_observers.value):
        observer(exception)


def _test_skipped():
    '''
    Called whenever a test is skipped.
    Notifies skip-observers.
    '''
    for observer in reversed(_skip_observers.value):
        observer()


def test():
    '''
    Decorator for tests
    '''
    def receiver(f):
        if _should_test_run():
            try:
                f()
                _test_passed()

            except AssertionFailure as e:
                _test_failed(e)

            except Exception as e:
                _test_failed(AssertionFailure(f'Unexpected exception {e}', exception=e))
        else:
            _test_skipped()

    return receiver
