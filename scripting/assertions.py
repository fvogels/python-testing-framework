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
        kwargs = { 'message': f'Expected {expected}, received {actual}', **kwargs }
        fail(**kwargs)


def assert_truthy(actual, **kwargs):
    if not actual:
        kwargs = { 'message': f'Expected truthy value, received {actual}', **kwargs }
        fail(**kwargs)


def assert_falsey(actual, **kwargs):
    if actual:
        kwargs = { 'message': f'Expected falsey value, received {actual}', **kwargs }
        fail(**kwargs)


def assert_equal_results(expected, actual):
    assert_equal(expected=expected.return_value, actual=actual.return_value, message=f"Expected return value is {expected.return_value}, actual is {actual.return_value}")

    for index, (expected_argument, actual_argument) in enumerate(zip(expected.output_arguments, actual.output_arguments)):
        assert_equal(expected=expected_argument, actual=actual_argument, message=f"Expected positional parameter {index+1} value is {expected_argument}, actual is {actual_argument}")

    for name in expected.output_kwargs.keys():
        expected_argument = expected.output_kwargs[name]
        actual_argument = actual.output_kwargs[name]
        assert_equal(expected=expected_argument, actual=actual_argument, message=f"Expected keyword parameter {name} value is {expected_argument}, actual is {actual_argument}")