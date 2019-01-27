from contextlib import contextmanager


class DynamicVariable:
    def __init__(self):
        self.__stack = []

    def bind(self, value):
        self.__stack.append(value)

    def unbind(self):
        self.__stack.pop()

    @property
    def value(self):
        return self.__stack[len(self.__stack) - 1]

    @value.setter
    def value(self, value):
        self.__stack[len(self.__stack) - 1] = value


def create_dynamic_variable():
    return DynamicVariable()


@contextmanager
def dynamic_bind(var, val):
    try:
        var.bind(val)
        yield
    finally:
        var.unbind()

@contextmanager
def dynamic_append(var, val):
    new_value = var.value + [val]

    with dynamic_bind(var, new_value):
        yield