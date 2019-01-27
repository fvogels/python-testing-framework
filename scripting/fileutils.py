import os


def find_files_recursively(predicate = lambda file: True, root = '.'):
    for entry in os.listdir(root):
        if os.path.isdir(entry):
            yield from find_files_recursively(predicate, root=os.path.join(root, entry))
        else:
            if predicate(entry):
                yield entry
