import os
from PIL import Image
import operator
import json
import utility
import os.path

def save_output(filename, record, internal_path):
    '''Saves record file to a file as a json'''
    to_save = json.dumps(record)

    f = open(filename + '.txt', 'w')
    f.write(to_save)
    f.close()

    # css output
    with open(filename + '.css', 'w') as f:
        for file, data in sorted(record.items()):
            css = '''.{file} {{width: {w}px; height: {h}px; background: url({filename}) {y1}px {y2}px;}}'''.format(
                file=file,
                filename=internal_path + filename,
                # l=data['x'],
                # w=data['w'],
                w=data['w'],
                h=data['h'],
                y1=-data['x'],
                y2=-data['y'],
            )
            f.write('{line}\n'.format(line=css))

class InfoFile(object):
    def __init__(self, path):

        self.params = {}

        if os.path.isfile(path):
            self._f = open(path, 'r')
            self._read()
            self._f.close()

    def _read(self):

        try:
            for line in self._f:
                if line and not line.startswith('#'):
                    key, value = line.split('=')
                    self.params[key] = value
        except:
            # no need to output this to the user
            pass

class FileManager(object):
    def __init__(self, settings):

        self.settings = settings
        self.input = self.settings.params['input']

        # just a list of filename
        self.files = []

        # dictionary: name => size
        self.file_sizes = {}

        # name => InfoFile
        self.info = {}

        # list of filenames sorted (desc)
        self.files_sorted = []

        self._read_input()

    def sort_by_area(self):
        pass

    def synchronise_info_files(self):
        '''Creates text files in input folder. The name of each file is the same as 
        that of the image file, but with a txt extension. If file already exists
        it is left untouched.'''
        
        if self.settings.params['synchronise']:
            files = os.listdir(self.input)

            for f in files:
                if utility.is_image(self.input + f):
                    h = open(self.input + f + '.json', 'a')
                    h.close()

    def _read_input(self):
        self.files = os.listdir(self.input)
        
        for f in self.files:
            try:
                im = Image.open(self.input + f)
                self.info[f] = InfoFile(self.input + f + '.txt')
                s = im.size
                area = s[0] * s[1]
            except Exception as e:
                print(str(e))
                continue

            # list: image area, width, height
            self.file_sizes[f] = [area, s[0], s[1]]

        self.files_sorted = [name for name, _ in sorted(self.file_sizes.items(), key=operator.itemgetter(1), reverse=True)]
