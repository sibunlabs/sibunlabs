#   This file is part of sibunlabs.
#
#   sibunlabs is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   sibunlabs is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with sibunlabs.  If not, see <http://www.gnu.org/licenses/>.

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
            'nopoints' : [(0,0)],
            'center' : (197, 196),
        }),
        (os.path.join(*["bin", "example-cells", "cell_real_1.png"]), {
            'points' : [(102, 29), (169,92)],
            'nopoints' : [(0,0), (29, 102)],
            'center' : (97, 99),
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

        radial_path = pathfinder.getRadialPath()

        assert path.shape == radial_path.shape
        assert pathfinder.getRadialPath()[:,0].min() > 0
        assert pathfinder.getRadialPath()[:,1].min() > 0
        assert pathfinder.getRadialPath()[:,1].max() < 360
        assert pathfinder.getRadialPath()[:,1].mean()/180 > 0.9

        centroid = pathfinder.getCentroid()
        assert abs(centroid[0] - conditions['center'][0]) <= 1
        assert abs(centroid[1] - conditions['center'][1]) <= 1

        im.close()
