import os
import sys
import json
import operator

from PIL import Image

from .utility import Logger

try:
    FileNotFoundError
except NameError:
    # Python2
    FileNotFoundError = IOError

logger = Logger(__name__)


def save_output(args, record):
    filename = args.output

    if args.json:
        logger.info('JSON output will be generated')

        _write_json(filename, record)

    if args.css:
        logger.info('CSS output will be generated')

        _write_css(filename, record)

def _write_json(filename, record):
    with open(filename + '.json', 'w') as f:
        f.write(json.dumps(record))


def _write_css(filename, record):
    fmt = ('.{selector} {{width: {w}px; height: {h}px;'
           'background: url({image}) {y1}px {y2}px;}}')

    with open(filename + '.css', 'w') as f:
        for selector, data in sorted(record.items()):
            f.write('{line}\n'.format(
                line=fmt.format(
                    selector=selector,
                    image=data['image'],
                    w=data['w'],
                    h=data['h'],
                    y1=-data['x'],
                    y2=-data['y'],
                )
            ))


class ParamsFile(object):
    def __init__(self, path):

        self._params = None

        params_path = path + '.params'

        if os.path.exists(params_path) and os.path.isfile(params_path):
            logger.info('Loading .params file for "%s"' % path)

            self._f = open(params_path, 'r')
            self._read()
            self._f.close()
        else:
            logger.warning('.params file for "%s" not found' % path)


    @property
    def params(self):
        return self._params


    def _read(self):
        content = self._f.read()

        if not content.strip():
            logger.warning('Params file "%s" is empty, it will be omitted',
                           self._f.name)

            return

        try:
            self._params = json.loads(content)
        except json.decoder.JSONDecodeError:
            logger.warning('Params file "%s" is not a valid JSON, it will be omitted',
                           self._f.name)


class FileManager(object):
    def __init__(self, args):
        self._args = args
        self._input = args.input

        if self._args.use_params:
            logger.info('.params files will be used')
        else:
            logger.info('.params files will no be used')

        # dictionary: name => size
        self._file_sizes = {}

        # name => ParamsFile
        self._params = {}

        # list of filenames sorted (desc)
        self._files_sorted = []

        self._read_input()


    @property
    def files_sorted(self):
        return self._files_sorted


    @property
    def params(self):
        return self._params


    def _create_params_files(self, path):
        """Create .params files for input images.

        The name of each file is the same as that of the image file, but with
        a .params extension. If file already exists it is left untouched."""

        params_path = path + '.params'

        if not os.path.exists(params_path):
            with open(params_path, 'w'):
                pass


    def _read_input(self):
        files = os.listdir(self._input)
        
        for f in files:
            if f.endswith('.params'):
                continue

            image_path = os.path.join(self._input, f)

            try:
                img = Image.open(image_path)
            except FileNotFoundError:
                logger.warning('File "%s" not found' % image_path)
                continue
            except OSError as e:
                logger.warning('%s' % e)
                continue

            if self._args.create_params_files:
                self._create_params_files(image_path)

            if self._args.use_params:
                self._load_params_file(f, image_path)

            width, height = img.size
            area = width * height

            self._file_sizes[f] = (area, width, height)

            if self._args.sort_alphabetically:
                self._sort_alphabetically()
            else:
                self._sort_by_area()

        if self._args.create_params_files:
            logger.info('.params files were created, quitting')
            sys.exit(0)

    def _load_params_file(self, f, image_path):
        self._params[f] = ParamsFile(image_path)


    def _sort_by_area(self):
        self._files_sorted = list(
            name
            for name, _ in sorted(
                self._file_sizes.items(), key=operator.itemgetter(1),
                reverse=True,
            ))


    def _sort_alphabetically(self):
        self._files_sorted = sorted(self._file_sizes.keys())
