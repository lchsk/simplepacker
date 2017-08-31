import argparse

from .utility import Logger, CURRENT_TIME

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
        '-m',
        '--margin',
        type=int,
        default=0,
        help='Margin',
    )

    parser.add_argument(
        '--css',
        action='store_true',
        help='If set, CSS file will be generated',
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='If set, JSON file will be generated',
    )

    parser.add_argument(
        '--use-params',
        action='store_true',
        help='If set, .params files will be used',
    )

    parser.add_argument(
        '--create-params-files',
        action='store_true',
        help='If set, .params files will be created and the application will quit',
    )

    parser.add_argument(
        '--dont-resize-output',
        action='store_true',
        help='If set, output images will not be resized to match the content',
    )

    args = parser.parse_args()

    log_args = ', '.join(
        '{}={}'.format(param, value)
        for param, value in vars(args).items()
    )

    logger.info('Parameters: ' + log_args)

    return args
