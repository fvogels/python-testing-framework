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


def load_code(filename, module_name):
    '''
    Loads code from .py module and puts it into module.
    Does not interfere without outside environment.
    '''
    module = types.ModuleType(module_name)

    with open(filename, 'r') as file:
        code = file.read()
        exec(code, module.__dict__)

    return module


def execute_code(filename):
    '''
    Executes code in given file.
    Does not interfere with outside environment.
    '''
    load_code(filename, 'tested')


