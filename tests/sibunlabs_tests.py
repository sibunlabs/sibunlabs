from nose.tools import *

import os

from PIL import Image, ImageSequence
import numpy as np
import scipy as sp

import sibunlabs

def setup():
    pass

def teardown():
    pass

def example_files():
    files_to_test = [
        (os.path.join(*["bin", "example-cells", "cell_tetragon.png"]), {
            'points' : [(201,127)],
            'nopoints' : [],
        }),
        (os.path.join(*["bin", "example-cells", "cell_real_1.png"]), {
            'points' : [(102, 29), (169,92)],
            'nopoints' : [(0,0), (29, 102)]
        }),
    ]

    return files_to_test

def test_imageProperty():
    for file, conditions in example_files():
        im = Image.open(file)
        im = im.convert("I")

        pathfinder = sibunlabs.Pathfinder(im)
        assert im.size == (pathfinder.width, pathfinder.height)

        im.close()

def test_sobel():
    for file, conditions in example_files():
        im = Image.open(file)
        im = im.convert("I")

        pathfinder = sibunlabs.Pathfinder(im, sobel = False)
        im_before = pathfinder._image

        assert im_before.sum() == pathfinder._image.sum()

        pathfinder.applySobel()

        assert im_before.sum() != pathfinder._image.sum()
        assert 0.0 == pathfinder._image.min()
        assert 1.0 == pathfinder._image.max()

        im.close()

def test_pathfinding():
    for file, conditions in example_files():
        print(file)

        im = Image.open(file)
        im = im.convert("I")

        pathfinder = sibunlabs.Pathfinder(im)

        path = pathfinder.getPath()
        pathlist = path.tolist()
        for point in conditions['points']:
            assert list(point) in pathlist
        for point in conditions['nopoints']:
            assert list(point) not in pathlist

        #assert 1 == 0

        im.close()
