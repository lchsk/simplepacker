from setuptools import setup, find_packages


setup(
    name = 'simplepacker',
    version = '0.2',
    description = 'Simplepacker packs many images into one or several files',
    license = 'GPL',
    packages = find_packages(),
    author = 'Maciej Lechowski',
    author_email = 'mjlechowski@gmail.com',
    url = 'https://github.com/lchsk/simplepacker',
    download_url = 'https://github.com/lchsk/simplepacker/archive/v0.2.tar.gz',
    keywords = [
        'images', 'graphics', 'packing', 'packer', 'texture', 'textures', 'games'
    ],
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics',
    ],
    install_requires=[
        'Pillow==8.2.0',
    ],
    entry_points={
        'console_scripts': [
            'simplepacker=simplepacker.simplepacker:main',
        ],
    },
)
