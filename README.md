# sibunlabs

## Contents
1. [About](#about)
2. [Modules](#modules)

## About
sibunlabs is a python package containing methods for use in biology and chemistry.

## Requirements
sibunlabs needs the following packages:
* numpy
* cv2

## Installation
Run setup.py

## Modules
### Pathfinder
The Pathfinder-Module can be used get a list of points describing the path of an object, like a cell. It makes use of the (Sobel operator)[http://en.wikipedia.org/wiki/Sobel_operator] to emphasize the edges and then looks for the highest intensity on a hair cross to use as a starting point. Then, it uses a primitive algorithm to find the path or raises an Exception if it is unable to to so.

It is best suited for bright field microscopy images of cells.

![Red Blood Cell](https://github.com/sibunlabs/sibunlabs/blob/master/bin/example-cells/cell_real_1.png)
![Red Blood Cell: Sobel image with found Path](https://github.com/sibunlabs/sibunlabs/blob/master/bin/example-cells/cell_real_1_found_path.png)
![Red Blood Cell: Path overlay](https://github.com/sibunlabs/sibunlabs/blob/master/bin/example-cells/cell_real_1_found_path_overlay.png)

#### Example
```python
import os

from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt

import sibunlabs

im = Image.open(os.path.join(*["bin", "example-cells", "cell_real_1.png"])).convert("I")
imarr = np.array(im, dtype = np.float32)

pathfinder = sibunlabs.Pathfinder(im)
path = pathfinder.getPath(centered = False).tolist()

for point in path:
    imarr[point[1],point[0]] = 0


plt.imshow(imarr, interpolation = "nearest")
plt.show()
```
