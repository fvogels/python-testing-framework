from contextlib import contextmanager, ExitStack
from scripting.testing import observers, skip_if
from scripting.layering import create_layering
from collections import namedtuple


Counts = namedtuple('Counts', ['npass', 'nfail', 'nskip', 'test_index'])


@contextmanager
def keep_counts():
    npass = 0
    nfail = 0
    nskip = 0

    def on_pass():
        nonlocal npass
        npass += 1

    def on_fail(e):
        nonlocal nfail
        nfail += 1

    def on_skip():
        nonlocal nskip
        nskip += 1

    def current_counts():
        return Counts(npass=npass, nfail=nfail, nskip=nskip, test_index=npass + nfail + nskip)

    with observers(on_pass=on_pass, on_fail=on_fail, on_skip=on_skip):
        yield current_counts
