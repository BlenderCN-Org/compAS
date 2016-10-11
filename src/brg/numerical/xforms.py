# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

from math import cos
from math import sin

from numpy import array


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 7, 2014'


docs = [
    'translation_matrix',
    'rotation_matrix',
    'scale_matrix',
    'projection_matrix',
]


def translation_matrix(direction):
    """"""
    return [
        [1, 0, 0, direction[0]],
        [0, 1, 0, direction[1]],
        [0, 0, 1, direction[2]],
        [0, 0, 0, 1]
    ]


def rotation_matrix(angle, direction, point=None, format='list'):
    """
    Construct a rotation matrix for a rotation over a given angle around a given
    axis represented by a (unit) direction vector. By default, the axis is
    assumed to pass through the origin.

    To perform a rotation around an arbitrary line (i.e. an axis not through
    the origin) an origin other than (0, 0, 0) may be provided for the
    direction vector. Note that the returned 'rotation matrix' is then composed
    of three translations and a rotation: Tp-1 Txy-1 Tz-1 R Tz Txy Tp
    """
    l = sum(direction[i] ** 2 for i in range(3)) ** 0.5
    u = [direction[i] / l for i in range(3)]
    cosa = cos(angle)
    sina = sin(angle)
    return [
        [cosa + u[0] ** 2  * (1 - cosa), u[0] * u[1] * (1 - cosa) - u[2] * sina,  u[0] * u[2] * (1 - cosa) + u[1] * sina],
        [u[1] * u[0] * (1 - cosa) + u[2] * sina, cosa + u[1] ** 2 * (1 - cosa), u[1] * u[2] * (1 - cosa) - u[0] * sina],
        [u[2] * u[0] * (1 - cosa) - u[1] * sina, u[2] * u[1] * (1 - cosa) + u[0] * sina, cosa + u[2] ** 2 * (1 - cosa)]
    ]


def scale_matrix(factor):
    """"""
    return [
        [factor, 0, 0],
        [0, factor, 0],
        [0, 0, factor]
    ]


def projection_matrix():
    """"""
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import math
    import time

    from numpy.random import randint
    from numpy import vstack

    import matplotlib.pyplot as plt

    n = 200

    points = randint(0, high=100, size=(n, 3)).astype(float)
    points = vstack((points, array([[0, 0, 0], [100, 0, 0]], dtype=float).reshape((2, 3))))

    t0 = time.time()

    a = math.pi / randint(1, high=8)
    R = array(rotation_matrix(a, (0, 0, 1)), dtype=float).reshape((3, 3))

    rpoints = R.dot(points.T).T

    t1 = time.time()

    print t1 - t0

    plt.plot(points[:, 0], points[:, 1], 'bo')
    plt.plot(rpoints[:, 0], rpoints[:, 1], 'ro')

    plt.plot(points[-2:, 0], points[-2:, 1], 'b-', label='before')
    plt.plot(rpoints[-2:, 0], rpoints[-2:, 1], 'r-', label='after')

    plt.legend(title='Rotation {0}'.format(180 * a / math.pi), fancybox=True)

    ax = plt.gca()
    ax.set_aspect('equal')
    ax.set_ylim((-10, 150))

    plt.show()
