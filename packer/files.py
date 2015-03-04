import os
from PIL import Image
import operator

class FileManager(object):
    def __init__(self, settings):

        self.settings = settings
        self.input = self.settings.params['input']

        # just a list of filename
        self.files = []

        # dictionary: name => size
        self.file_sizes = {}

        # list of filenames sorted (desc)
        self.files_sorted = []

        self._read_input()

    def sort_by_area(self):
        pass

    def _read_input(self):
        self.files = os.listdir(self.input)
        
        for f in self.files:
            im = Image.open(self.input + f)
            s = im.size
            area = s[0] * s[1]

            # list: image area, width, height
            self.file_sizes[f] = [area, s[0], s[1]]

        self.files_sorted = [name for name, _ in sorted(self.file_sizes.items(), key=operator.itemgetter(1), reverse=True)]
