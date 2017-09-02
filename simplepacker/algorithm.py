import os

from PIL import Image

from . import files
from .utility import Logger, Color, split_filename

logger = Logger(__name__)


class PackingAlgorithm(object):
    def __init__(self, args, file_manager):
        self._args = args
        self._file_manager = file_manager

        self._output_i = -1
        self._output = []
        self._locs = []

        self._record = {}


    def run(self):
        self._add_new_output()
        self._pack()
        self._close()


    def _pack(self):
        """Must be overriden in child classes"""

        raise NotImplementedError()


    def _get_output(self, i):
        assert i >= 0 and i < len(self._output)

        return self._output[i]


    def _add_new_output(self):
        self._output_i += 1

        self._locs.append(list())

        if self._args.output.endswith('png'):
            color = 'RGBA'
        else:
            color = 'RGB'

        self._output.append(Image.new(
            color,
            (self._args.width, self._args.height),
            None,
        ))


    def _check_for_errors(self, f, i, j):
        if i == self._args.width or j == self._args.height:
            self._add_new_output()

            return True
        elif i > self._args.width or j > self._args.height:
            logger.warning('File "%s" did not fit, creating a new image' % f)

            self._add_new_output()

            return True

        logger.info('File "%s" placed in the output image' % f)

        return False


    def _resize_output(self, output, output_index):
        x, y, w, h = 0, 0, 0, 0

        for rect in self._locs[output_index - 1]:
            if rect.left < x:
                x = rect.left

            if rect.bottom < y:
                y = rect.bottom

            if rect.right > w:
                w = rect.right

            if rect.top > h:
                h = rect.top

        return output.crop((x, y, w, h))


    def _close(self):
        output_files = []

        for i, output in enumerate(self._output, 1):
            output_file = self._get_output_name(i)

            if os.path.exists(output_file):
                logger.error('File "%s" already exists, will not be saved',
                             output_file)

                continue

            output_files.append(output_file)

            if not self._args.dont_resize_output:
                output = self._resize_output(output, i)

            if 0 in output.size:
                logger.error('Output "%s" is empty, will not be saved', output_file)

                continue

            output.save(output_file)

            logger.info('Output %d/%d "%s" saved'
                        % (i, len(self._output), output_file),
                        Color.OKGREEN)

        files.save_output(
            args=self._args,
            record=self._record,
        )


    def _get_output_name(self, index):
        path = split_filename(self._args.output)
        filename = path[:-1]
        ext = path[-1]

        return '{path}.{num}{ext}'.format(
            path=''.join(filename),
            num=index,
            ext=ext,
        )
