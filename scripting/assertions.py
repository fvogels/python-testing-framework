class AssertionFailure(Exception):
    def __init__(self, message, **extra):
        super().__init__(message)
        self.__extra = extra

    @property
    def extra(self):
        return self.__extra


def fail(message = '', **kwargs):
    raise AssertionFailure(message, kwargs)
