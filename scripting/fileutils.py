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