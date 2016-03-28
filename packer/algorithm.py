from PIL import Image
from packer.colours import colours
import files

class PackingAlgorithm(object):
    def __init__(self, settings, file_manager):
        self.settings = settings
        self.file_manager = file_manager
        self.output = None
        self.errors = False
        self.record = {}

    def prepare(self):
        self.output = Image.new("RGBA", self.settings.params['output_size'], None)

    def print_output(self):
        if self.errors:
            print colours.FAIL + 'Packing completed with some errors.' + colours.ENDC
        else:
            print colours.OKGREEN + 'Packing completed successfully!' + colours.ENDC

    def check_for_errors(self, f, i, j):
        if i >= self.settings.params['output_size'][0] or j >= self.settings.params['output_size'][1]:
            self.errors = True
            print colours.FAIL + 'ERROR: file ' + f + " didn't fit." + colours.ENDC

    def close(self):
        self.output.save(self.settings.params['output'])
        self.print_output()
        files.save_output(
            self.settings.params['output'],
            self.record,
            self.settings.params['internal_path']
        )

        print colours.OKBLUE + 'Output should be available in ' + self.settings.params['output'] + ' and ' + self.settings.params['output']  + '.txt' + colours.ENDC