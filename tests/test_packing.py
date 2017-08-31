import glob
import sys
import unittest

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from simplepacker.settings import read_args
from simplepacker.files import FileManager
from simplepacker.algorithm_greedy import AlgorithmGreedy

class TestGreedyPacking(unittest.TestCase):
    TEST_DATA = 'tests/data/'

    def setUp(self):
        super(TestGreedyPacking, self).setUp()

        sys.argv = [
            'simplepacker',
            '-i', self.TEST_DATA,
            '-o', 'output.jpg',
        ]

        self._args = read_args()

        self._fm = FileManager(self._args)

    def test_run(self):
        a = AlgorithmGreedy(self._args, self._fm)
        a.run()

        output = glob.glob('*.jpg')

        self.assertEqual(len(output), 1)

