from ringer import __version__
import ringer.main as main
from unittest import TestCase


class Test(TestCase):
    @staticmethod
    def test_version():
        assert __version__ == '0.1.0'

    def test_expires_at_to_datetime(self):
        rv = main.expires_at_to_datetime(1602956389.7934)

        self.assertEqual('2020-10-17 17:39:49', rv)

