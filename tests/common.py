import glob
import subprocess

from PIL import Image


def get_output(fmt='jpg'):
    output = glob.glob('*.' + fmt)

    return {
        f: Image.open(f).size
        for f in output
    }


def clean_output():
    subprocess.run(['make', 'clean-all'])
