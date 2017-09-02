from .settings import read_args
from .files import FileManager
from .algorithm_greedy import AlgorithmGreedy

def main():
    args = read_args()

    fm = FileManager(args)

    a = AlgorithmGreedy(args, fm)
    a.run()


if __name__ == '__main__':
    main()
