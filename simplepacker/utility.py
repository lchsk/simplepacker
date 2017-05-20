import os
import sys
import logging
from datetime import datetime

from PIL import Image


log_filename = ('{d.year}_{d.month}_{d.day}_'
               '{d.hour}_{d.minute}_{d.second}.log'.format(d=datetime.now()))

log_format = '%(levelname)s - %(name)s - %(message)s'
formatter = logging.Formatter(log_format)

root = logging.getLogger()
root.setLevel(logging.INFO)

stdoutlog = logging.StreamHandler(sys.stdout)
stdoutlog.setLevel(logging.INFO)
stdoutlog.setFormatter(formatter)
root.addHandler(stdoutlog)

filelog = logging.FileHandler(filename=log_filename)
filelog.setLevel(logging.INFO)
filelog.setFormatter(formatter)

root.addHandler(filelog)


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger(object):
    def __init__(self, name):
        self._logger = logging.getLogger(name)


    def info(self, message, color=None):
        self._logger.info(self._get_message(message, color))


    def warning(self, message):
        self._logger.warning(self._get_message(message, Color.WARNING))


    def error(self, message):
        self._logger.error(self._get_message(message, Color.FAIL))


    @staticmethod
    def _get_message(message, color=None):
        if color:
            return color + message + Color.ENDC

        return message


def split_filename(filename):
    return os.path.splitext(filename)


def is_image(path):
    try:
        Image.open(path)
    except OSError:
        return False
    else:
        return True
