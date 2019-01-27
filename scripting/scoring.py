from contextlib import contextmanager
from scripting.dynamic import create_dynamic_variable, dynamic_bind
from scripting.testing import observers


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

        self.value = value
        self.maximum = maximum

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
        return "{}/{}".format(self.value, self.maximum)

    def is_max_score(self):
        return self.value == self.maximum



__accumulated_score = create_dynamic_variable()

@contextmanager
def keep_score(receiver):
    def on_pass():
        __accumulated_score.value = __accumulated_score.value + Score(1, 1)

    def on_fail_or_skip():
        __accumulated_score.value = __accumulated_score.value + Score(0, 1)

    with dynamic_bind(__accumulated_score, Score(0,0)):
        with observers(on_pass=on_pass, on_fail=on_fail_or_skip, on_skip=on_fail_or_skip):
            yield

        receiver(__accumulated_score.value)


@contextmanager
def scale(maximum):
    with dynamic_bind(__accumulated_score, Score(0,0)):
        yield
        score = __accumulated_score.value

    __accumulated_score.value = score.rescale(maximum)