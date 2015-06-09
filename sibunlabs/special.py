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

from __future__ import division, print_function

import numpy as np

def rfa(r, phi, phi_in_radians = False):
    N = len(r)
    k_max = N//2

    aj = np.zeros(k_max, dtype=np.float64)
    bj = np.zeros(k_max, dtype=np.float64)

    if phi_in_radians == False:
        phi = phi/180*np.pi

    for j in range(0, k_max):
        aj[j] += 2/N*(r*np.cos(j*phi)).sum()
        bj[j] += 2/N*(r*np.sin(j*phi)).sum()

    cj = np.sqrt(aj**2+bj**2)
    phij = np.arctan2(bj, aj)

    return cj, phij