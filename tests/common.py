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


def clean_output():
    subprocess_run(['make', 'clean-all'])
