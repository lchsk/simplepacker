from PIL import Image

class PackingAlgorithm(object):
    def __init__(self, settings, file_manager):
        self.settings = settings
        self.file_manager = file_manager
        self.output = None

    def prepare(self):
        self.output = Image.new("RGBA", self.settings.params['output_size'], None)

    def close(self):
        self.output.save(self.settings.params['output'])