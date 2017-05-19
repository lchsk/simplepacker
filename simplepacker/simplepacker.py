from settings import Settings
from files import FileManager

from algorithm_largest import AlgorithmLargest

if __name__ == '__main__':
    s = Settings()
    s.read_parameters()
    s.print_parameters()

    fm = FileManager(s)
    fm.synchronise_info_files()

    a = AlgorithmLargest(s, fm)
    a.prepare()
    a.pack()
    a.close()
