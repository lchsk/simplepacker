from algorithm import PackingAlgorithm
from PIL import Image
from packer.geometry import Point, Rect, overlap
from packer.colours import colours


class AlgorithmLargest(PackingAlgorithm):
    def __init__(self, settings, file_manager):
        super(AlgorithmLargest, self).__init__(settings, file_manager)

        # locations
        self.loc = []
        self.width = self.settings.params['output_size'][0]
        self.height = self.settings.params['output_size'][1]
        self.padding = self.settings.params['padding']
        self.step = self.settings.params['step']



    def is_free(self, rect):

        for r in self.loc:
            if overlap(r, rect):
                return False

        return True

    def pack(self):

        errors = False
    
        for f in self.file_manager.files_sorted:
            img = Image.open(self.settings.params['input'] + f)
            
            s = img.size
            j = 0
            i = 0
            added = False

            while i < self.width:
                if added: break

                j = 0

                while j < self.height:
                    if added: break

                    p1 = Point(i + self.padding, j + self.padding)
                    p2 = Point(i + s[0] + self.padding, j + s[1] + self.padding)
                    r1 = Rect(p1, p2)

                    if self.is_free(r1) and p2.x < self.width and p2.y < self.height:
                        self.loc.append(r1)
                        self.output.paste(img, (p1.x, p1.y), None)
                        added = True

                    j += self.step

                i += self.step

            if i >= self.width or j >= self.height:
                errors = True
                print colours.FAIL + 'ERROR: file ' + f + " didn't fit." + colours.ENDC

        if errors:
            print colours.FAIL + 'Packing completed with some errors.' + colours.ENDC
        else:
            print colours.OKGREEN + 'Packing completed successfully!' + colours.ENDC

