from unittest.mock import ANY
from unittest.mock import patch

import pytest

from os.path import expanduser

from cguard.util import home_dir, cguard_dir, shims_dir


class TestUtil(object):
    def test_home_dir(self):
        d = home_dir()
        assert d == expanduser("~")

    def test_cguard_dir(self):
        target = expanduser("~") + "/.cguard"
        d = cguard_dir()
        assert d == target

    def test_shims_dir(self):
        target = expanduser("~") + "/.cguard/shims"
        d = shims_dir()
        assert d == target
