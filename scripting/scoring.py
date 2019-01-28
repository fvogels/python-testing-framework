from contextlib import contextmanager, ExitStack
from scripting.dynamic import create_dynamic_variable, dynamic_bind
from scripting.testing import observers, skip_if
from scripting.layering import create_layering


class Score:
    """
    Represents a score.

    Scores are not to be confused with fractions.
    For example, a score of 5/10 is not the same as a score of 1/2.
    Score addition also follows different rules.
    """
    def __init__(self, value, maximum):
        assert 0 <= value, "Score value must be positive"
        assert value <= maximum, f"Score value ({value}) must not be greater than maximum ({maximum})"

        self.__value = value
        self.__maximum = maximum

    @property
    def value(self):
        return self.__value

    @property
    def maximum(self):
        return self.__maximum

    def zero(self):
        return Score(0, self.__maximum)

    def __add__(self, other):
        """
        Adds two scores together.

        a/b + c/d = (a+c)/(b+d).
        """
        return Score(self.value + other.value, self.maximum + other.maximum)

    def rescale(self, maximum):
        """
        Rescales the score to a given maximum.
        """
        return Score(self.value / self.maximum * maximum, maximum)

    def __str__(self):
        return f"{self.value}/{self.maximum}"

    def __repr__(self):
        return str(self)

    def is_max_score(self):
        return self.value == self.maximum

    def __eq__(self, other):
        return self.value == other.value and self.maximum == other.maximum



_accumulated_score = create_dynamic_variable()
_layering = create_layering()

@contextmanager
def keep_score():
    with _layering.initialize(), dynamic_bind(_accumulated_score, Score(0,0)), cumulative():
        yield


def current_score():
    return _accumulated_score.value


@contextmanager
def scale(maximum):
    with dynamic_bind(_accumulated_score, Score(0,0)):
        yield
        score = current_score()

    _accumulated_score.value = score.rescale(maximum)


@contextmanager
def all_or_nothing():
    failure_detected = False

    def on_pass():
        _accumulated_score.value = _accumulated_score.value + Score(1, 1)

    def on_fail_or_skip():
        nonlocal failure_detected
        failure_detected = True
        _accumulated_score.value = _accumulated_score.value + Score(0, 1)

    def skip_predicate():
        return failure_detected

    with _layering.add(), _layering.observers(on_pass=on_pass, on_fail=on_fail_or_skip, on_skip=on_fail_or_skip), skip_if(skip_predicate):
        yield

        if not _accumulated_score.value.is_max_score():
            _accumulated_score.value = _accumulated_score.value.zero()


@contextmanager
def cumulative():
    def on_pass():
        _accumulated_score.value = _accumulated_score.value + Score(1, 1)

    def on_fail_or_skip():
        _accumulated_score.value = _accumulated_score.value + Score(0, 1)

    with _layering.add(), _layering.observers(on_pass=on_pass, on_fail=on_fail_or_skip, on_skip=on_fail_or_skip):
        yield