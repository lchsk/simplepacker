import sys
import unittest

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from simplepacker.settings import read_args
from simplepacker.files import FileManager
from simplepacker.algorithm_greedy import AlgorithmGreedy

from .common import get_output, clean_output


class TestGreedyPacking(unittest.TestCase):
    TEST_DATA = 'tests/data/'

    def setUp(self):
        super(TestGreedyPacking, self).setUp()

        clean_output()

    def tearDown(self):
        clean_output()

    def test_run(self):
        sys.argv = [
            'simplepacker',
            '-i', self.TEST_DATA,
            '-o', 'output.jpg',
            '--dont-resize-output',
        ]

        args = read_args()
        fm = FileManager(args)

        a = AlgorithmGreedy(args, fm)
        a.run()

        output = get_output()

        # Check output image was not resized
        self.assertEqual(output, {'output.1.jpg': (1024, 1024)})

    def test_multiple_output_files(self):
        sys.argv = [
            'simplepacker',
            '-i', self.TEST_DATA,
            '-o', 'output.jpg',
            '--width', '600',
            '--height', '600',
        ]

        args = read_args()
        fm = FileManager(args)

        a = AlgorithmGreedy(args, fm)
        a.run()

        output = get_output()

        # Check output images were resized
        self.assertEqual(output, {
            'output.2.jpg': (100, 102),
            'output.1.jpg': (520, 599),
        })


    def test_omit_large_files(self):
        sys.argv = [
            'simplepacker',
            '-i', self.TEST_DATA,
            '-o', 'output.jpg',
            '--width', '50',
            '--height', '50',
        ]

        args = read_args()
        fm = FileManager(args)

        a = AlgorithmGreedy(args, fm)
        a.run()

        output = get_output()

        self.assertEqual(output, {})
