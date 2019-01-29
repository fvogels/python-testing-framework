from contextlib import contextmanager, ExitStack
from scripting.dynamic import create_dynamic_variable, dynamic_bind, dynamic_append
from scripting.testing import test, skip
from scripting.fileutils import load_code


_tested_module = create_dynamic_variable()


# @contextmanager
# def tested_file(filename):
#     module = load_code(filename, 'tested')

#     with dynamic_bind(_tested_module, module):
#         yield


# @contextmanager
# def tested_function(identifier):
#     if hasattr(_tested_module.value, identifier):
#         yield getattr(_tested_module.value, identifier)
#     else:
#         with skip():
#             yield None
