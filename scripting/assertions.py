class AssertionFailure(Exception):
    pass


def fail():
    raise AssertionFailure()
