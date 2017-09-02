# simplepacker

Simplepacker is a command-line tool that can create sprite sheets/sprite atlases.

[![codecov](https://codecov.io/gh/lchsk/simplepacker/branch/master/graph/badge.svg)](https://codecov.io/gh/lchsk/simplepacker)
[![Build Status](https://travis-ci.org/lchsk/simplepacker.svg?branch=master)](https://travis-ci.org/lchsk/simplepacker)

# Installation

```
$ pip install simplepacker
```

# Basic use

Pack images from `./examples` directory.

```
$ simplepacker -i ./examples -o output1.jpg
```

[![simplepacker output1](./examples/output/output1.1.jpg)]

Set maximum height, padding and generate a json file with metadata.

```
$ simplepacker -i ./examples -o output2.jpg --height 200 --padding 5 --json
```

[![simplepacker output1](./examples/output/output2.1.jpg)]

Resulting json file:

```
{"feynman": {"x": 0, "y": 0, "w": 100, "h": 141, "name": "feynman", "ext": ".jpg", "image": "output2.1.jpg"}, "curie_sklodowska": {"x": 105, "y": 0, "w": 100, "h": 132, "name": "curie_sklodowska", "ext": ".jpg", "image": "output2.1.jpg"}, "einstein": {"x": 210, "y": 0, "w": 100, "h": 131, "name": "einstein", "ext": ".jpg", "image": "output2.1.jpg"}}
```

With `--css` argument it can also generate CSS output.

# Arguments

|Argument|Description|
|---|---|
|`-h, --help`|See help screen|
|`-i, --input`|Input directory|
|`--width`|Maximum output width|
|`--height`|Maximum output height|
|`-p, --padding`|Padding|
|`-m, --margin`|Margin|
|`--css`|Generate CSS output|
|`--json`|Generate JSON output|
|`--use-params`|Use `.params` JSON files to add metadata to output JSONs|
|`--create-params-files`|Create an empty `.params` file for each input image|
|`--dont-resize-output`|Output images will always be equal to parameters set by `--width` and `--height`|
|`--sort-alphabetically`|Sort input images by name|