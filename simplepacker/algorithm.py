from PIL import Image
from simplepacker import files
from simplepacker.utility import Logger, Color

logger = Logger(__name__)


class PackingAlgorithm(object):
    def __init__(self, args, file_manager):
        self._args = args
        self._file_manager = file_manager
        self._output = None
        self._errors = False
        self._record = {}


    def run(self):
        self._prepare()
        self._pack()
        self._close()


    def _pack(self):
        """Must be overriden in child classes"""

        raise NotImplementedError()


    def _prepare(self):
        self._output = Image.new(
            "RGBA",
            (self._args.width, self._args.height),
            None,
        )


    def _print_output(self):
        if self._errors:
            logger.warning('Packing completed with some errors')
        else:
            logger.info('Packing completed successfully!', Color.OKGREEN)


    def _check_for_errors(self, f, i, j):
        if i >= self._args.width or j >= self._args.height:
            self._errors = True

            logger.error('File "{f}" did not fit')


    def _close(self):
        self._output.save(self._args.output)
        self._print_output()
        files.save_output(
            self._args.output,
            self._record,
            './'
            # self.settings.params['internal_path']
        )

        logger.info('Output is available in "{}"'.format(self._args.output),
                    Color.OKGREEN)
