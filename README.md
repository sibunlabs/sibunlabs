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
![Red Blood Cell with found Path](https://github.com/sibunlabs/sibunlabs/blob/master/bin/example-cells/cell_real_1_found_path.png)

#### Example
