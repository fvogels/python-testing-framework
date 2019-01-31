from contextlib import contextmanager
import types
import os


def find_files_recursively(predicate = lambda file: True, root = '.'):
    for entry in os.listdir(root):
        path = os.path.join(root, entry)

        if os.path.isdir(path):
            yield from find_files_recursively(predicate, root=path)
        else:
            if predicate(path):
                yield path


def has_extension(extension):
    def predicate(path):
        _, ext = os.path.splitext(path)
        return ext == extension

    return predicate


def has_name(name):
    def predicate(path):
        return os.path.basename(path) == name

    return predicate


def load_code_from_string_into_module(string, module_name):
    '''
    Executes code from string and puts it into module.
    Does not interfere without outside environment.
    '''
    module = types.ModuleType(module_name)
    exec(string, module.__dict__)

    return module


def load_code_from_file_into_module(filename, module_name):
    '''
    Loads code from .py module and puts it into module.
    Does not interfere without outside environment.
    '''
    with open(filename, 'r') as file:
        code = file.read()

    return load_code_from_string_into_module(code, module_name)


def execute_code(filename):
    '''
    Executes code in given file.
    Does not interfere with outside environment.
    '''
    load_code_from_file_into_module(filename, 'run')


@contextmanager
def inside_directory(path):
    current = os.getcwd()

    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(current)