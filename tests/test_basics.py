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
        self.assertIsNone(self._algo._output)

        self._algo._prepare()

        self.assertIsInstance(self._algo._output, Image)

        width, height = self._algo._output.size

        self.assertEqual(width, self._args.width)
        self.assertEqual(height, self._args.height)
