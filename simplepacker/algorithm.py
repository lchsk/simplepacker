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


    def _get_current_loc(self):
        assert self._output_i >= 0 and self._output_i < len(self._output)

        return self._locs[self._output_i]


    def _get_loc(self, i):
        assert i >= 0 and i < len(self._output)

        return self._locs[i]


    def _get_current_output(self):
        assert self._output_i >= 0 and self._output_i < len(self._output)

        return self._output[self._output_i]


    def _get_output(self, i):
        assert i >= 0 and i < len(self._output)

        return self._output[i]


    def _add_new_output(self):
        self._output_i += 1

        self._locs.append(list())

        self._output.append(Image.new(
            "RGBA",
            (self._args.width, self._args.height),
            None,
        ))


    def _print_output(self):
        logger.info('Packing completed successfully!', Color.OKGREEN)


    def _check_for_errors(self, f, i, j):
        if i >= self._args.width or j >= self._args.height:
            logger.warning('File "%s" did not fit, creating a new image' % f)

            self._add_new_output()

            return True

        logger.info('File "%s" placed in the output image' % f)

        return False


    def _close(self):
        for i, output in enumerate(self._output, 1):
            logger.info('Saving output %d/%d' % (i, len(self._output)))

            path = split_filename(self._args.output)
            filename = path[:-1]
            ext = path[-1]

            output.save('{path}.{num}{ext}'.format(
                path=''.join(filename),
                num=i,
                ext=ext,
            ))

        self._print_output()

        files.save_output(
            args=self._args,
            record=self._record,
        )

        logger.info('Output is available in "{}"'.format(self._args.output),
                    Color.OKGREEN)
