from contextlib import contextmanager, ExitStack
from scripting.testing import observers, skip_if
from scripting.layering import create_layering
from collections import namedtuple


class Counts:
    def __init__(self, npass, nfail, nskip):
        self.__npass = npass
        self.__nfail = nfail
        self.__nskip = nskip

    @property
    def test_index(self):
        return self.__npass + self.__nfail + self.__nskip

    @property
    def npass(self):
        return self.__npass

    @property
    def nfail(self):
        return self.__nfail

    @property
    def nskip(self):
        return self.__nskip

    def __eq__(self, other):
        return self.npass == other.npass and self.nfail == other.nfail and self.nskip == other.nskip


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
        return Counts(npass=npass, nfail=nfail, nskip=nskip)

    with observers(on_pass=on_pass, on_fail=on_fail, on_skip=on_skip):
        yield current_counts
