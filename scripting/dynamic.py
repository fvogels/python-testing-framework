from contextlib import contextmanager
import inspect
import sys


class DynamicVariable:
    def __init__(self):
        frame = inspect.stack()[2]
        self.__creation_location = (frame.filename, frame.lineno)
        self.__stack = []

    def bind(self, value):
        self.__stack.append(value)
        return self

    def unbind(self):
        if self.__stack:
            self.__stack.pop()
            return self
        else:
            self.__fatal_failure()

    @property
    def value(self):
        if self.__stack:
            return self.__stack[len(self.__stack) - 1]
        else:
            self.__fatal_failure()

    @value.setter
    def value(self, value):
        if self.__stack:
            self.__stack[len(self.__stack) - 1] = value
        else:
            self.__fatal_failure()

    def __fatal_failure(self):
        sys.stderr.write(f'Dynamic variable failure\nDynamic variable was created on line {self.__creation_location[1]} of file {self.__creation_location[0]}')
        sys.exit(-1)



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