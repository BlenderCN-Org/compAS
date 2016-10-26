from math import cos
from math import sin

from numpy import array


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 20, 2016'


def translation_matrix(direction, rtype='list'):
    """Creates a translation matrix to translate vectors.

    Parameters:
        direction (list): The x, y and z components of the translation.
        rtype (str): Return the result as 'list' or 'array'.

    Returns:
        (list, array): The (4 x 4) translation matrix.

    Homogeneous vectors are used, i.e. vector [x, y, z]T is represented as
    [x, y, z, 1]T. Matrix multiplication of the translation matrix with the
    homogeneous vector will return the new translated vector.

    Examples:
        >>> T = translation_matrix([1, 2, 3], rtype='array')
        [[1 0 0 1]
         [0 1 0 2]
         [0 0 1 3]
         [0 0 0 1]]
        >>> dot(T, array([[2], [2], [2], [1]]))
        [[3]
         [4]
         [5]
         [1]]
    """
    T = [[1, 0, 0, direction[0]],
         [0, 1, 0, direction[1]],
         [0, 0, 1, direction[2]],
         [0, 0, 0, 1]]
    if  rtype == 'list':
        return T
    elif rtype == 'array':
        return array(T)


def rotation_matrix(angle, direction, point=None, rtype='list'):
    """Creates a rotation matrix for rotating vectors around an axis.

    Parameters:
        angle (float): Angle in radians to rotate by.
        direction (list): The x, y and z components of the rotation axis.
        rtype (str): Return the result as 'list' or 'array'.

    Returns:
        (list, array): The (3 x 3) rotation matrix.

    Rotates a vector around a given axis (the axis will be unitised), the
    rotation is based on the right hand rule, i.e. anti-clockwise when the axis
    of rotation points towards the observer.

    Examples:
        >>> R = rotation_matrix(angle=pi/2, direction=[0, 0, 1], rtype='array')
        [[  6.12-17  -1.00+00   0.00+00]
         [  1.00+00   6.12-17   0.00+00]
         [  0.00+00   0.00+00   1.00+00]]
        >>> dot(R, array([[1], [1], [1]]))
        [[-1.]
         [ 1.]
         [ 1.]]
    """
# To perform a rotation around an arbitrary line (i.e. an axis not through
# the origin) an origin other than (0, 0, 0) may be provided for the
# direction vector. Note that the returned 'rotation matrix' is then
# composed of three translations and a rotation: Tp-1 Txy-1 Tz-1 R Tz Txy Tp
    l = sum(direction[i] ** 2 for i in range(3)) ** 0.5
    u = [direction[i] / l for i in range(3)]
    cosa = cos(angle)
    sina = sin(angle)
    mca = 1 - cosa
    R = [[cosa + u[0] ** 2  * mca, u[0] * u[1] * mca - u[2] * sina,  u[0] * u[2] * mca + u[1] * sina],
         [u[1] * u[0] * mca + u[2] * sina, cosa + u[1] ** 2 * mca, u[1] * u[2] * mca - u[0] * sina],
         [u[2] * u[0] * mca - u[1] * sina, u[2] * u[1] * mca + u[0] * sina, cosa + u[2] ** 2 * mca]]
    if  rtype == 'list':
        return R
    elif rtype == 'array':
        return array(R)


def scale_matrix(factor, rtype='list'):
    """Creates a scale matrix to scale vectors.

    Parameters:
        factor (float): Uniform scale factor for the  x, y and z components.
        rtype (str): Return the result as 'list' or 'array'.

    Returns:
        (list, array): The (3 x 3) scale matrix.

    The scale matrix is a (3 x 3) matrix with the scale factor along all of the
    three diagonal elements, used to scale a vector.

    Examples:
        >>> S = scale_matrix(2, rtype='array')
        [[2 0 0]
         [0 2 0]
         [0 0 2]]
        >>> dot(S, array([[1], [2], [3]]))
        [[2]
         [4]
         [6]]
    """
    S = [[factor, 0, 0],
         [0, factor, 0],
         [0, 0, factor]]
    if  rtype == 'list':
        return S
    elif rtype == 'array':
        return array(S)


def projection_matrix():
    raise NotImplementedError


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
