from .settings import read_args
from .files import FileManager
from .algorithm_largest import AlgorithmLargest

if __name__ == '__main__':
    args = read_args()

    fm = FileManager(args)
    fm.synchronise_info_files()

    a = AlgorithmLargest(args, fm)
    a.run()
