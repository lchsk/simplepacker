import os
import glob
import subprocess

from PIL import Image


try:
    subprocess_run = subprocess.run
except AttributeError:
    subprocess_run = subprocess.call


def get_output(fmt='jpg'):
    output = glob.glob('*.' + fmt)

    return {
        f: Image.open(f).size
        for f in output
    }


def get_files(*fmts):
    files = set()

    for f in os.listdir('.'):
        if f.split('.')[-1] in fmts:
            files.add(f)

    return files


def group_files(files):
    grouped = {}

    for f in files:
        grouped[f.split('.')[-1]] = f

    return grouped


def clean_output():
    subprocess_run(['make', 'clean-all'])
