import sys
import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

import os

from PIL.Image import Image

from simplepacker.settings import read_args
from simplepacker.algorithm import PackingAlgorithm
from simplepacker.files import FileManager


class TestSettingsBase(unittest.TestCase):

    def setUp(self):
        self._listdir = os.listdir

        os.listdir = MagicMock()
        sys.argv = ['simplepacker', '-i', 'inputdir/']

        self._args = read_args()

    def tearDown(self):
        os.listdir = self._listdir


class TestAlgorithm(TestSettingsBase):
    def setUp(self):
        super(TestAlgorithm, self).setUp()

        self._fm = FileManager(self._args)
        self._algo = PackingAlgorithm(self._args, self._fm)

    def test_prepare(self):
        self.assertEqual(self._algo._output, [])
        self.assertEqual(self._algo._output_i, -1)

        self._algo._add_new_output()

        self.assertEqual(self._algo._output_i, 0)
        self.assertEqual(len(self._algo._output), 1)

        self.assertIsInstance(self._algo._output[0], Image)

        width, height = self._algo._output[0].size

        self.assertEqual(width, self._args.width)
        self.assertEqual(height, self._args.height)
