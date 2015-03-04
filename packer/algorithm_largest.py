from algorithm import PackingAlgorithm
from PIL import Image
from packer.geometry import Point, Rect, overlap
from packer.colours import colours


class AlgorithmLargest(PackingAlgorithm):
    def __init__(self, settings, file_manager):
        super(AlgorithmLargest, self).__init__(settings, file_manager)

        # locations
        self.loc = []

    def is_free(self, rect):

        for r in self.loc:
            if overlap(r, rect):
                return False

        return True

    def next_image(self):
    
        for f in self.file_manager.files_sorted:
            img = Image.open(self.settings.params['input'] + f)
            # print colours.OKBLUE + f + colours.ENDC
            
            s = img.size
            step = 20
            j = 0
            i = 0
            padding = 5

            added = False

            while i < 1000:
                if added: break

                j = 0

                while j < 1000:
                    if added: break

                    p1 = Point(i + padding, j + padding)
                    p2 = Point(i + s[0] + padding, j + s[1] + padding)
                    r1 = Rect(p1, p2)

                    if self.is_free(r1) and p2.x < 1000 and p2.y < 1000:
                        self.loc.append(r1)
                        self.output.paste(img, (p1.x, p1.y), None)
                        added = True

                    j += step

                i += step

            if i >= 1000 or j >= 1000:
                print f + ' didnt fit.'
