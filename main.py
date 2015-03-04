from packer.settings import Settings
from packer.files import FileManager

from packer.algorithm_largest import AlgorithmLargest

if __name__ == '__main__':
    s = Settings()
    s.read_parameters()
    s.print_parameters()

    fm = FileManager(s)

    a = AlgorithmLargest(s, fm)
    a.prepare()
    a.next_image()
    a.close()