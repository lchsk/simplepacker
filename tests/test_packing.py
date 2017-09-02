import json
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
            '--json',
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

        files = get_files('css', 'json')

        self.assertEqual(files, set(['output.jpg.json']))

        grouped = group_files(files)

        json_file = json.load(open(grouped['json']))

        # cat2 is the larger one so it's in output.1
        self.assertEqual(json_file['cat2']['image'], 'output.1.jpg')
        self.assertEqual(json_file['cat1']['image'], 'output.2.jpg')


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


    def test_dont_overwrite_output_files(self):
        sys.argv = [
            'simplepacker',
            '-i', self.TEST_DATA,
            '-o', 'output.jpg',
        ]

        args = read_args()
        fm = FileManager(args)

        a = AlgorithmGreedy(args, fm)
        a.run()

        output = get_output()

        self.assertEqual(len(output), 1)

        with open(list(output)[0], 'rb') as f:
            first_file = f.read()

        a = AlgorithmGreedy(args, fm)
        a.run()

        output = get_output()

        with open(list(output)[0], 'rb') as f:
            second_file = f.read()

        self.assertEqual(first_file, second_file)


    def test_output_data(self):
        sys.argv = [
            'simplepacker',
            '-i', self.TEST_DATA,
            '-o', 'output.jpg',
            '--json',
            '--css',
            '--use-params',
        ]

        args = read_args()
        fm = FileManager(args)

        a = AlgorithmGreedy(args, fm)
        a.run()

        output = get_output()

        files = get_files('css', 'json')

        self.assertEqual(files, set(['output.jpg.json', 'output.jpg.css']))

        grouped = group_files(files)

        json_file = json.load(open(grouped['json']))

        # Check params
        self.assertEqual(json_file['cat1']['params']['name'], 'cat-name')
        self.assertEqual(json_file['cat1']['params']['likes'],
                         ['cat-food', 'sleeping'])

        for value in json_file.values():
            self.assertEqual(value['image'], 'output.1.jpg')

        self.assertIn('cat1', json_file)
        self.assertIn('cat2', json_file)

        self.assertEqual(output, {'output.1.jpg': (520, 701)})


    def test_exact_image_size_no_padding(self):
        sys.argv = [
            'simplepacker',
            '-i', self.TEST_DATA,
            '-o', 'output.png',
            '--width', '100',
            '--height', '102',
        ]

        args = read_args()
        fm = FileManager(args)

        a = AlgorithmGreedy(args, fm)
        a.run()

        output = get_output('png')

        self.assertEqual(output, {'output.1.png': (100, 102)})


    def test_exact_image_size_with_padding(self):
        sys.argv = [
            'simplepacker',
            '-i', self.TEST_DATA,
            '-o', 'output.png',
            '--width', '520',
            '--height', '707',
            '--padding', '5',
        ]

        args = read_args()
        fm = FileManager(args)

        a = AlgorithmGreedy(args, fm)
        a.run()

        output = get_output('png')

        self.assertEqual(output, {'output.1.png': (520, 707)})
