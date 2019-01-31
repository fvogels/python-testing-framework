class AssertionFailure(Exception):
    def __init__(self, message, **extra):
        super().__init__(message)
        self.__extra = extra

    @property
    def extra(self):
        return self.__extra


def fail(message = '', **kwargs):
    raise AssertionFailure(message, **kwargs)


def assert_equal(expected, actual, **kwargs):
    if expected != actual:
        kwargs = { **kwargs, 'message': f'Expected {expected}, received {actual}' }
        fail(**kwargs)


def assert_truthy(actual, **kwargs):
    if not actual:
        kwargs = { **kwargs, 'message': f'Expected truthy value, received {actual}' }
        fail(**kwargs)


def assert_falsey(actual, **kwargs):
    if actual:
        kwargs = { **kwargs, 'message': f'Expected falsey value, received {actual}' }
        fail(**kwargs)


def assert_equal_results(expected, actual):
    assert_equal(expected=expected.return_value, actual=actual.return_value, message=f"Expected return value is {expected.return_value}, actual is {actual.return_value}")

    for expected_argument, actual_argument in zip(expected.output_arguments, actual.output_arguments):
        assert_equal(expected=expected_argument, actual=actual_argument, message=f"Expected paremeter value is {expected_argument}, actual is {actual_argument}")