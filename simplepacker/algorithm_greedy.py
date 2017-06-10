import os

from PIL import Image

from .utility import split_filename
from .algorithm import PackingAlgorithm
from .geometry import Point, Rect, overlap


class AlgorithmGreedy(PackingAlgorithm):
    def __init__(self, args, file_manager):
        super(AlgorithmGreedy, self).__init__(args, file_manager)

        self._loc = []

        self._width = args.width
        self._height = args.height
        self._margin = args.margin
        self._step = args.step


    def _pack(self):
        for f in self._file_manager.files_sorted:
            img = Image.open(os.path.join(self._args.input, f))
            w, h = img.size
            j = i = 0
            added = False

            while i < self._width:
                if added:
                    break

                j = 0

                while j < self._height:
                    if added:
                        break

                    p1 = Point(i + self._margin, j + self._margin)
                    p2 = Point(i + w + self._margin, j + h + self._margin)
                    r1 = Rect(p1, p2)

                    if (self._is_free(r1) and p2.x < self._width
                        and p2.y < self._height):
                        self._loc.append(r1)
                        self._output.paste(img, (p1.x, p1.y), None)

                        filename, ext = split_filename(f)

                        data = {
                            'x': p1.x,
                            'y': p1.y,
                            'w': w,
                            'h': h,
                            'name': filename,
                            'ext': ext,
                        }

                        if self._args.use_params:
                            data.update(
                                params=self._file_manager.params.get(f).params,
                            )

                        self._record[filename] = data

                        added = True

                    j += self._step

                i += self._step

            self._check_for_errors(f, i, j)


    def _is_free(self, rect):
        for r in self._loc:
            if overlap(r, rect):
                return False

        return True
