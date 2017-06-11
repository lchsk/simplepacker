import os

from PIL import Image

from .utility import split_filename, Logger
from .algorithm import PackingAlgorithm
from .geometry import Point, Rect, overlap


logger = Logger(__name__)


class AlgorithmGreedy(PackingAlgorithm):
    def __init__(self, args, file_manager):
        super(AlgorithmGreedy, self).__init__(args, file_manager)

        self._images_left = []

        self._width = args.width
        self._height = args.height
        self._margin = args.margin
        self._step = args.step


    def _pack(self):
        self._images_left = self._file_manager.files_sorted[:]

        while self._images_left:
            f = self._images_left.pop(0)

            img = Image.open(os.path.join(self._args.input, f))

            w, h = img.size

            if w > self._width or h > self._height:
                logger.error(
                    'File "%s" is too large to fit into the output, '
                    'it will be skipped' % f
                )

                continue

            j = i = 0
            added = False

            for loc_i, loc in enumerate(self._locs):
                j = i = 0

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

                        if (self._is_free(r1, loc) and p2.x < self._width
                            and p2.y < self._height):
                            loc.append(r1)
                            self._get_output(loc_i).paste(img, (p1.x, p1.y), None)

                            filename, ext = split_filename(f)

                            data = {
                                'x': p1.x,
                                'y': p1.y,
                                'w': w,
                                'h': h,
                                'name': filename,
                                'ext': ext,
                                'image': self._get_output_name(loc_i + 1),
                            }

                            if self._args.use_params:
                                data.update(
                                    params=self._file_manager.params.get(f).params,
                                )

                            self._record[filename] = data

                            added = True

                            break

                        j += self._step

                    i += self._step

            if self._check_for_errors(f, i, j):
                self._images_left.append(f)


    def _is_free(self, rect, loc):
        for r in loc:
            if overlap(r, rect):
                return False

        return True
