from .settings import read_args
from .files import FileManager
from .algorithm_greedy import AlgorithmGreedy

if __name__ == '__main__':
    args = read_args()

    fm = FileManager(args)

    a = AlgorithmGreedy(args, fm)
    a.run()
