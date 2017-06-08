import sys
import unittest

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from simplepacker.settings import read_args
from simplepacker.files import FileManager


class TestTestData(unittest.TestCase):
    """Check we have correct data for testing."""

    TEST_DATA = 'tests/data/'

    def setUp(self):
        super(TestTestData, self).setUp()

        sys.argv = ['simplepacker', '-i', self.TEST_DATA]

        self._args = read_args()

        self._fm = FileManager(self._args)

    def test_loading_files(self):
        self.assertEqual(list(self._fm._files_sorted), ['cat1.jpg', 'cat2.jpg'])
