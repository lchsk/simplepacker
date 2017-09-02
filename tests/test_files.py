import os
import sys
import unittest

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from simplepacker.settings import read_args
from simplepacker.files import FileManager
from simplepacker.algorithm_greedy import AlgorithmGreedy
from .common import get_output, clean_output, get_files, group_files


class TestTestData(unittest.TestCase):
    """Check we have correct data for testing."""

    TEST_DATA = 'tests/data/'

    def setUp(self):
        super(TestTestData, self).setUp()


    def test_loading_files(self):
        sys.argv = ['simplepacker', '-i', self.TEST_DATA]

        args = read_args()
        fm = FileManager(args)

        self.assertEqual(list(fm._files_sorted), ['cat2.jpg', 'cat1.jpg'])


    def test_params_files_creation(self):
        sys.argv = ['simplepacker', '-i', self.TEST_DATA, '--create-params-files']

        expected = set(['cat1.jpg', 'cat1.jpg.params', 'cat2.jpg', 'cat2.jpg.params'])

        self.assertFalse(expected.issubset(set(os.listdir(self.TEST_DATA))))

        try:
            _ = FileManager(read_args())
        except SystemExit:
            self.assertTrue(expected.issubset(set(os.listdir(self.TEST_DATA))))
        else:
            self.fail()

        # Clean up after this test
        os.remove(self.TEST_DATA + 'cat2.jpg.params')


    def test_sort_files_alphabetically(self):
        sys.argv = ['simplepacker', '-i', self.TEST_DATA]

        fm = FileManager(read_args())

        # Larger files first
        self.assertEqual(fm._files_sorted, ['cat2.jpg', 'cat1.jpg'])

        sys.argv = ['simplepacker', '-i', self.TEST_DATA, '--sort-alphabetically']

        fm = FileManager(read_args())

        # Alphabetically
        self.assertEqual(fm._files_sorted, ['cat1.jpg', 'cat2.jpg'])
