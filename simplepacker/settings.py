import argparse

from simplepacker.utility import Logger, CURRENT_TIME

logger = Logger(__name__)

def read_args():
    parser = argparse.ArgumentParser(description='simplepacker')

    parser.add_argument(
        '-i',
        '--input',
        type=str,
        required=True,
        help='Input directory',
    )

    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default=CURRENT_TIME + '.png',
        help='Output image filename',
    )

    parser.add_argument(
        '--width',
        type=int,
        default=1024,
        help='Width of the output image',
    )

    parser.add_argument(
        '--height',
        type=int,
        default=1024,
        help='Height of the output image',
    )

    parser.add_argument(
        '-s',
        '--step',
        type=int,
        default=20,
        help='Step size',
    )

    parser.add_argument(
        '-p',
        '--padding',
        type=int,
        default=5,
        help='Padding',
    )

    args = parser.parse_args()

    log_args = ', '.join(
        '{}={}'.format(param, value)
        for param, value in vars(args).items()
    )

    logger.info('Parameters: ' + log_args)

    return args
