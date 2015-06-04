# sibunlabs

## Contents
1. [About](#about)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Modules](#modules)
  1. [Pathfinder](#pathfinder)

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
The Pathfinder-Module can be used get a list of points describing the path of an object, like a cell. It makes use of the [Sobel operator](http://en.wikipedia.org/wiki/Sobel_operator) to emphasize the edges and then looks for the highest intensity on a hair cross to use as a starting point. Then, it uses a primitive algorithm to find the path or raises an Exception if it is unable to to so.

It is best suited for bright field microscopy images of cells.

![Red Blood Cell](https://github.com/sibunlabs/sibunlabs/blob/master/bin/example-cells/cell_real_1.png)
![Red Blood Cell: Sobel image with found Path](https://github.com/sibunlabs/sibunlabs/blob/master/bin/example-cells/cell_real_1_found_path.png)
![Red Blood Cell: Path overlay](https://github.com/sibunlabs/sibunlabs/blob/master/bin/example-cells/cell_real_1_found_path_overlay.png)

#### Examples
*Overlay found contour with original image: [examples/pathfinder_1.py](https://github.com/sibunlabs/sibunlabs/blob/master/examples/pathfinder_1.py)
*Show r as a function of phi by using getRadialPath(): [examples/pathfinder_2.py](https://github.com/sibunlabs/sibunlabs/blob/master/examples/pathfinder_2.py)
