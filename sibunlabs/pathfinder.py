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

import numpy as np
import cv2

def absSobel(im, x = 0, y = 0):
    """ Applies the sobel filter in x,y direction and returns the absolute
        value
    """
    return abs(cv2.Sobel(im, cv2.CV_32F, x, y))

def absSobelX(im):
    """ Applies the sobel filter in x-direction and returns the absolute value
    """
    return absSobel(im, x=1)

def absSobelY(im):
    """ Applies the sobel filter in y-direction and returns the absolute value
    """
    return absSobel(im, y=1)

def isAdjacent(point_A, point_B):
    """ Tests if point_A is adjacent to point_B """
    if abs(point_A[0] - point_B[0]) <= 1 and abs(point_A[1] - point_B[1]) <= 1:
        return True
    else:
        return False

def calculateDistance(p1, p2):
    """ Calculates the distance between point p1 and p2 """
    return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

class Pathfinder:
    # Never modifiy these members
    _image = None
    _shape = (None, None)
    _path = None
    _centroid = None

    _start_x = None
    _start_y = None

    _lim_x = 2
    _lim_y = 2

    _weight = None
    _weightcount = 1

    DIRECTION_UP = 0
    DIRECTION_UPRIGHT = 1
    DIRECTION_RIGHT = 2
    DIRECTION_DOWNRIGHT = 3
    DIRECTION_DOWN = 4
    DIRECTION_DOWNLEFT = 5
    DIRECTION_LEFT = 6
    DIRECTION_UPLEFT = 7

    # The following members are okay to modify
    max_iterations = 1000
    inflexibility = 5

    @property
    def width(self): return self._shape[1]

    @property
    def height(self): return self._shape[0]

    @property
    def start_x(self): return self._start_x

    @start_x.setter
    def start_x(self, value):
        if isinstance(value, int) == False:
            raise ValueError("value must be an valid integer")
        if value >= self.width:
            raise ValueError("value must be within the image boundaries")

        self._start_x = value

    @property
    def start_y(self): return self._start_y

    @start_y.setter
    def start_y(self, value):
        if isinstance(value, int) == False:
            raise ValueError("value must be an valid integer")
        if value >= self.width:
            raise ValueError("value must be within the image boundaries")

        self._start_y = value

    def __init__(self, image, sobel = True):
        """ Converts the image given by the argument image and converts it to a
            numpy array with dtype = float64. """
        self._image = np.array(image, dtype = np.float32)

        shape = self._image.shape
        if len(shape) != 2:
            raise ValueError("image has to be a 2-dimensional image")
        self._shape = shape

        if sobel:
            self.applySobel()

        self._setDefaultWeight()

    def _setDefaultWeight(self):
        """ Sets the default weight to a useful size """
        self.setWeight(np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]))

    def setWeight(self, weight):
        """ Sets a weight used for calculate the whitness of a given point (eg,
            use a 3x3 array to take into account all adjacent points.
        """
        if len(weight.shape) != 2:
            raise ArgumentError("weight must be 2-dimensional")
        if weight.shape[0] != weight.shape[1]:
            raise ArgumentError("weight must be a squared array")
        if weight.shape[0]%2 == 0:
            raise ArgumentError("weight must have uneven dimensions")

        self._weight = weight
        self._weightcount = self.calcWeightcount(weight)

    def calcWeightcount(self, weight_matrix):
        """ Calculates how many actual weights are contained in the array. 0s
            are not counted """
        c = 0
        for y in weight_matrix:
            for x in y:
                if x > 0:
                    c+=1
        return c

    def applySobel(self):
        """ Applies the sobel filter in x and in y direction to the image and
            then normalizes the image
        """
        self._image =  absSobelX(self._image) + absSobelY(self._image)
        self._normalize()

    def getPath(self, centered = False):
        """ Returns a list of (x,y) integer points describing the path found by
            the search algorithm. If centered is True, the path points get
            adjusted by the calculated centroid.
        """
        if self._path is None:
            self._findPath()

        newpath = np.zeros(self._path.shape)

        if centered == True:
            centroid = self._calculateCentroid()
        else:
            centroid = np.array([0,0])

        # Make a y,x array to a the more intuitive x,y array
        newpath[:,0] = self._path[:,1] - centroid[1]
        newpath[:,1] = self._path[:,0] - centroid[0]

        return newpath

    def _calculateCentroid(self):
        """ Calculates the geometric center (centroid) of the found path and
            returns an (y, x) array with its coordinates as floats.
        """
        if self._centroid is None:
            a = (0,0)
            N = self._path.shape[0]
            L = 0
            for i in range(0, N):
                pm = self._path[i-1]
                p0 = self._path[i]
                try:
                    pp = self._path[i+1]
                except IndexError:
                    pp = self._path[0]
                dm = calculateDistance(pm, p0)
                di = calculateDistance(p0, pp)
                x = a[0] + p0[0]*(dm)
                y = a[1] + p0[1]*(di)
                a = (y, x)
                L = L + di

            a = np.array(a)
            c = a*1/(L)
            self._centroid = c

        return self._centroid

    def getCentroid(self):
        """ Returns a (x, y) tuple of the centroids coordinates """
        centroid = self._calculateCentroid()
        return (centroid[1], centroid[0])

    def getRadialPath(self):
        """ Returns a list of (r, phi) float tuples describing the path found by
            the search algorithm. The points are centered around the calculated
            centroid
        """
        if self._path is None:
            self._findPath()

        # Center the path around the centroid
        centroid = self._calculateCentroid()
        cp = self._path - centroid

        # Convert the path
        radial_path = np.zeros(cp.shape)
        radial_path[:,0] = np.sqrt(cp[:,0]**2 + cp[:,1]**2)
        radial_path[:,1] = np.arctan2(cp[:,1], cp[:,0]) * (-180/np.pi) + 180

        return radial_path

    def _normalize(self):
        """ Normalizes the image array to have a value between 0.0 and 1.0 """
        self._image -= self._image.min()
        self._image /= self._image.max()

        ret, self._image = cv2.threshold(self._image, 0.02, 1.0, 3)

    def _findPath(self):
        """ Tries to find the path """
        # Get the "cross hair" to find the starting point. If not changed, the
        # image center is used.
        if self.start_x == None:
            start_x = self.width//2
        else:
            start_x = self.start_x

        if self.start_y == None:
            start_y = self.height//2
        else:
            start_y = self.start_y

        # Search possibles start points
        startpoints = self._searchStartpoint(start_x, start_y)

        # path storages
        path_fragments = []
        path_reports = []
        for sp in startpoints:
            path_fragments.append([sp])
            path_reports.append(None)
        n_frags = len(path_fragments)

        # look for the path
        j = 3
        i = 0
        while True:
            try:
                next_point = self._searchNextpoint(j, path_fragments[j])
            except OutOfBoundaryError:
                path_reports[j] = "oob"
                break
            path_fragments[j].append(next_point)
            # Max Iteration abort condition
            if i > self.max_iterations:
                path_reports[j] = "max_it"
                break
            # Real abortion only after 10 points
            if i > 10:
                if next_point in path_fragments[j][:-1]:
                    path_reports[j] = "self_bite"
                    break
                if isAdjacent(next_point, path_fragments[j][0]):
                    path_reports[j] = "OK"
                    break
            i+=1

        if path_reports[j] == "self_bite" and len(path_fragments[j]) > self.inflexibility:
            reverse_path = [path_fragments[j][k-1] for k in range(self.inflexibility, 0, -1)]
            i = 0
            while True:
                try:
                    next_point = self._searchNextpoint(j, reverse_path)
                except OutOfBoundaryError:
                    path_reports[j] = "oob"
                    break
                reverse_path.append(next_point)
                # Max Iteration abort condition
                if i > self.max_iterations:
                    path_reports[j] = "max_it"
                    break
                # Real abortion only after 10 points
                if i > 10:
                    if next_point in reverse_path[j]:
                        path_reports[j] = "self_bite"
                        break
                    if next_point in path_fragments[j]:
                        path_reports[j] = "OK"
                        new_path = []
                        for p in path_fragments[j]:
                            if p == next_point:
                                break
                            new_path.append(p)
                        for k in range(len(reverse_path), 0, -1):
                            p = reverse_path[k-1]
                            if p == path_fragments[0]:
                                break
                            new_path.append(p)
                        path_fragments[j] = new_path
                i+=1

        self._path = np.array(path_fragments[j])

        if path_reports[j] == "self_bite":
            raise NoClosedPathFound
        elif path_fragments[j] == "max_it":
            raise MaxIterationReached
        elif path_fragments[j] == "oob":
            raise OutOfBoundaryError

    def _searchNextpoint(self, d, path):
        # Get newest point
        yi, xi = path[-1]

        # Get the default direction
        if d == 0:
            default_direction = self.DIRECTION_RIGHT
        elif d == 1:
            default_direction = self.DIRECTION_DOWN
        elif d == 2:
            default_direction = self.DIRECTION_LEFT
        else:
            default_direction = self.DIRECTION_UP

        # Get points which have to be searched in order to determine the direction
        directionMask, direction = self._getDirectionMask(path, default_direction = default_direction)

        # Calculate the whiteness of those points
        whitesearch_intensities = []
        for point in directionMask:
            whitesearch_intensities.append(self._getWhiteness(y=point[0], x=point[1]))

        # Get the most white point
        maxwhite = max(whitesearch_intensities)

        # Get the actual point by the biggest intensity (the whitest point)
        nextPoint = (0, 0)
        for i in range(0, len(directionMask)):
            if whitesearch_intensities[i] == maxwhite:
                nextPoint = directionMask[i]

        #print(path[-1], self._getWhiteness(y=path[-1][0], x=path[-1][1]), directionMask, direction)

        # Return next point
        return nextPoint

    def _getDirectionMask(self, path, default_direction = None):
        if default_direction is None:
            default_direction = self.DIRECTION_UP

        # Calculate direction or use default direction
        if len(path) >= self.inflexibility:
            # Get the last 10 points
            slopseq = path[-self.inflexibility:]
            # Get difference in y and x direction
            y_diff = slopseq[-1][0] - slopseq[0][0]
            x_diff = slopseq[-1][1] - slopseq[0][1]
            # Get direction
            if x_diff == 0:
                if y_diff < 0:
                    direction = self.DIRECTION_UP
                else:
                    direction = self.DIRECTION_DOWN
            elif y_diff == 0:
                if x_diff > 0:
                    direction = self.DIRECTION_RIGHT
                else:
                    direction = self.DIRECTION_LEFT
            else:
                s = y_diff/x_diff
                if x_diff > 0 and y_diff < 0:
                    # s is negative
                    if s < -2:
                        direction = self.DIRECTION_UP
                    elif s >= -2 and s <= -0.5:
                        direction = self.DIRECTION_UPRIGHT
                    else:
                        direction = self.DIRECTION_RIGHT
                elif x_diff > 0 and y_diff > 0:
                    # s is positive
                    if s < 0.5:
                        direction = self.DIRECTION_RIGHT
                    elif s >= 0.5 and s <= 2:
                        direction = self.DIRECTION_DOWNRIGHT
                    else:
                        direction = self.DIRECTION_DOWN
                elif x_diff < 0 and y_diff > 0:
                    # s is negative
                    if s < -2:
                        direction = self.DIRECTION_DOWN
                    elif s >= -2 and s <= -0.5:
                        direction = self.DIRECTION_DOWNLEFT
                    else:
                        direction = self.DIRECTION_LEFT
                else:
                    # s is positive again
                    if s < 0.5:
                        direction = self.DIRECTION_LEFT
                    elif s >= 0.5 and s <= 2:
                        direction = self.DIRECTION_UPLEFT
                    else:
                        direction = self.DIRECTION_UP
        else:
            direction = default_direction


        yi, xi = path[-1]

        # Get direction mask
        if direction == self.DIRECTION_UP:
            blacksearch_points = [
                (yi-1, xi-1), # top-left
                (yi-1, xi), # top
                (yi-1, xi+1), # top-right
            ]
        elif direction == self.DIRECTION_UPRIGHT:
            blacksearch_points = [
                (yi-1, xi), # top
                (yi-1, xi+1), # top-right
                (yi, xi+1), # right
            ]
        elif direction == self.DIRECTION_RIGHT:
            blacksearch_points = [
                (yi-1, xi+1), # top-right
                (yi, xi+1), # right
                (yi+1, xi+1), # bottom-right
            ]
        elif direction == self.DIRECTION_DOWNRIGHT:
            blacksearch_points = [
                (yi, xi+1), # right
                (yi+1, xi+1), # bottom-right
                (yi+1, xi), # bottom
            ]
        elif direction == self.DIRECTION_DOWN:
            blacksearch_points = [
                (yi+1, xi+1), # bottom-right
                (yi+1, xi), # bottom
                (yi+1, xi-1), # bottom-left
            ]
        elif direction == self.DIRECTION_DOWNLEFT:
            blacksearch_points = [
                (yi+1, xi), # bottom
                (yi+1, xi-1), # bottom-left
                (yi, xi-1), # left
            ]
        elif direction == self.DIRECTION_LEFT:
            blacksearch_points = [
                (yi+1, xi-1), # bottom-left
                (yi, xi-1), # left
                (yi-1, xi-1), # top-left
            ]
        elif direction == self.DIRECTION_UPLEFT:
            blacksearch_points = [
                (yi, xi-1), # left
                (yi-1, xi-1), # top-left
                (yi-1, xi), # top
            ]

        return blacksearch_points, direction

    def _searchStartpoint(self, start_x, start_y):
        points = {
            "north" : ((-1, -1), 0.0),
            "east" : ((-1, -1), 0.0),
            "south" : ((-1, -1), 0.0),
            "west" : ((-1, -1), 0.0),
        }

        for d in points:
            for point in self._searchMaxPoint((start_y, start_x), direction = d):
                whiteness = self._image[point]
                if whiteness > points[d][1]:
                    points[d] = (point, whiteness)

        return points["north"][0], points["east"][0], points["south"][0], points["west"][0]

    def _searchMaxPoint(self, start, direction):
        if direction == "north":
            for y in range(start[0], self._lim_y-1, -1):
                yield (y, start[1])
        elif direction == "south":
            for y in range(start[0], self.height-self._lim_y, 1):
                yield (y, start[1])
        elif direction == "west":
            for x in range(start[1], self._lim_x-1, -1):
                yield (start[0], x)
        elif direction == "east":
            for x in range(start[0], self.width-self._lim_x, 1):
                yield (start[0], x)

    def _getWhiteness(self, x, y):
        # Get weight matrix dimensions
        weight_x_dim, weight_y_dim = self._weight.shape
        # Calculate how many times we need to look "left/right" and "top/bottom"
        weight_x_dim//=2
        weight_y_dim//=2
        # Check if we have enough place to calculate the blackness (OutOfBoundaryError)
        if y < weight_y_dim or y >= (self.height - weight_y_dim - 1)  or x  < weight_x_dim or x >= (self.width - weight_x_dim - 1):
            raise OutOfBoundaryError("Out of boundary: (%i,%i)" %(x,y))

        try:
            subMatrix = (self._image[y-weight_y_dim:y+weight_y_dim+1,x-weight_x_dim:x+weight_x_dim+1])
        except IndexError:
            return 0
        if 0 in subMatrix:
            #print("Zero!")
            r = 0
        else:
            r = ((subMatrix*self._weight)/self._weightcount).sum()
        return r

class PathfinderException(Exception):
    pass

class NoClosedPathFound(PathfinderException):
    pass

class MaxIterationReached(PathfinderException):
    pass

class OutOfBoundaryError(PathfinderException):
    pass