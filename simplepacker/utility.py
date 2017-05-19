import os.path
from PIL import Image

def split_filename(filename):
    return os.path.splitext(filename)

def is_image(path):
    try:
        im = Image.open(path)
        return True
    except:
        return False
