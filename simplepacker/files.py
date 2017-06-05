import os
import json
import operator

from PIL import Image

from utility import Logger

logger = Logger(__name__)


def save_output(args, record):
    filename = args.output

    if args.json:
        logger.info('Writing JSON file for "%s"' % filename)

        _write_json(filename, record)
    else:
        logger.info('No JSON file for "%s"' % filename)

    if args.css:
        logger.info('Writing CSS file for "%s"' % filename)

        _write_css(filename, record)
    else:
        logger.info('No CSS file for "%s"' % filename)

def _write_json(filename, record):
    with open(filename + '.json', 'w') as f:
        f.write(json.dumps(record))


def _write_css(filename, record):
    fmt = ('.{selector} {{width: {w}px; height: {h}px;'
           'background: url({filename}) {y1}px {y2}px;}}')

    with open(filename + '.css', 'w') as f:
        for selector, data in sorted(record.items()):
            f.write('{line}\n'.format(
                line=fmt.format(
                    selector=selector,
                    filename=filename,
                    w=data['w'],
                    h=data['h'],
                    y1=-data['x'],
                    y2=-data['y'],
                )
            ))


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
    def __init__(self, args):
        self._args = args
        self._input = args.input

        # just a list of filename
        self._files = []

        # dictionary: name => size
        self._file_sizes = {}

        # name => InfoFile
        self._info = {}

        # list of filenames sorted (desc)
        self._files_sorted = []

        self._read_input()


    @property
    def files_sorted(self):
        return self._files_sorted


    @property
    def info(self):
        return self._info


    def synchronise_info_files(self):
        '''Creates text files in input folder. The name of each file is the same as 
        that of the image file, but with a txt extension. If file already exists
        it is left untouched.'''
        
        # if self.settings.params['synchronise']:
            # files = os.listdir(self._input)

            # for f in files:
                # if utility.is_image(self.input + f):
                    # h = open(self.input + f + '.json', 'a')
                    # h.close()


    def _read_input(self):
        self._files = os.listdir(self._input)
        
        for f in self._files:
            image_path = os.path.join(self._input, f)

            try:
                img = Image.open(image_path)
            except FileNotFoundError:
                logger.warning('File "%s" not found' % image_path)
                continue
            except OSError as e:
                logger.warning('%s' % e)
                continue

            self._info[f] = InfoFile(image_path + '.txt')

            width, height = img.size
            area = width * height

            self._file_sizes[f] = (area, width, height)
            self._sort_by_area()


    def _sort_by_area(self):
        self._files_sorted = (
            name
            for name, _ in sorted(
                self._file_sizes.items(), key=operator.itemgetter(1),
                reverse=True,
            ))
