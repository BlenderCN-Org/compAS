from __future__ import print_function

from numpy import asarray
from numpy import array
from numpy import meshgrid
from numpy import linspace
from numpy import amax
from numpy import amin

from scipy.interpolate import griddata

import matplotlib.pyplot as plt
from compas.numerical.linalg import normrow


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'lengths',
    # 'rotate',
    'scalarfield_contours',
    'plot_scalarfield_contours',
]


def lengths(C, X):
    r"""Calculates the lengths and co-ordinate differences.

    Parameters:
        C (sparse): Connectivity matrix (m x n)
        X (array): Co-ordinates of vertices/points (n x 3).

    Returns:
        array: Vectors of co-ordinate differences in x, y and z (m x 3).
        array: Lengths of members (m x 1)

    Examples:
        >>> C = connectivity_matrix([[0, 1], [1, 2]], 'csr')
        >>> X = array([[0, 0, 0], [1, 1, 0], [0, 0, 1]])
        >>> uvw
        array([[ 1,  1,  0],
               [-1, -1,  1]])
        >>> l
        array([[ 1.41421356],
               [ 1.73205081]])
    """
    uvw = C.dot(X)
    return uvw, normrow(uvw)


# def rotate(points):
#     raise NotImplementedError


def scalarfield_contours(xy, s, N=50):
    r"""Compute the contour lines of a scalarfield.

    The computation of the contour lines is based on the ``contours`` function
    available through matplotlib
    (`<http://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.contour.html#matplotlib.axes.Axes.contour>`_).

    Parameters:
        xy (array-like): The xy-coordinates at which the scalar field is defined.
        s (array-like): The values of the scalar field.
        N (int): Optional. The number of contour lines to compute. Default is ``50``.

    Returns:
        tuple: A tuple of a list of levels and a list of contour geometry.

        The list of levels contains the values of the scalarfield at each of
        the contours. The second item in the tuple is a list of contour lines.
        Each contour line is a list of paths, and each path is a list polygons.

    Examples:

        .. code-block:: python

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            points = [mesh.vertex_coordinates(key) for key in mesh]
            centroid = centroid_points(points)

            distances = [distance_point_point(point, centroid) for point in points]

            xy = [[points[i][0], points[i][1]] for i in range(len(points))]

            levels, contours = contours_scalarfield(xy, distances)

            for i in range(len(contours)):
                level = levels[i]
                contour = contours[i]
                print(level)
                for path in contour:
                    for polygon in path:
                        print(polygon)


    See Also:

        :func:`compas.datastructures.numerical.geometry.mesh_contours`

    """
    xy = asarray(xy)
    s = asarray(s)
    x = xy[:, 0]
    y = xy[:, 1]
    X, Y = meshgrid(
        linspace(amin(x), amax(x), 2 * N),
        linspace(amin(y), amax(y), 2 * N)
    )
    S = griddata((x, y), s, (X, Y), method='cubic')
    ax = plt.figure().add_subplot(111, aspect='equal')
    c = ax.contour(X, Y, S, N)
    plt.draw()
    contours = [0] * len(c.collections)
    levels = c.levels
    for i, coll in enumerate(iter(c.collections)):
        paths = coll.get_paths()
        contours[i] = [0] * len(paths)
        for j, path in enumerate(iter(paths)):
            polygons = path.to_polygons()
            contours[i][j] = [0] * len(polygons)
            for k, polygon in enumerate(iter(polygons)):
                contours[i][j][k] = polygon.tolist()
    return levels, contours


def plot_scalarfield_contours(xy, s, N=50):
    r"""Plot the contours of a scalarfield.

    Parameters:
        xy (array-like): The xy-coordinates at which the scalar field is defined.
        s (array-like): The values of the scalar field.
        N (int): Optional. The number of contour lines to compute. Default is ``30``.

    Examples:

        .. code-block:: python

            import compas

            from compas.datastructures.mesh import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            points = [mesh.vertex_coordinates(key) for key in mesh]
            centroid = centroid_points(points)

            xy = [[points[i][0], points[i][1]] for i in range(len(points))]
            d = [distance_point_point(point, centroid) for point in points]

            plot_scalarfield_contours(xy, d)


        .. plot::

            import compas
            from compas.datastructures.mesh import Mesh
            from compas.geometry import centroid_points
            from compas.geometry import distance_point_point
            from compas.numerical.geometry import plot_scalarfield_contours

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            points = [mesh.vertex_coordinates(key) for key in mesh]
            centroid = centroid_points(points)
            d = [distance_point_point(point, centroid) for point in points]
            xy = [[points[i][0], points[i][1]] for i in range(len(points))]

            plot_scalarfield_contours(xy, d)

    See Also:

        :func:`compas.datastructures.mesh.numerical.geometry.plot_mesh_contours`

    """
    xy = asarray(xy)
    s = asarray(s)
    x = xy[:, 0]
    y = xy[:, 1]
    X, Y = meshgrid(
        linspace(amin(x), amax(x), 2 * N),
        linspace(amin(y), amax(y), 2 * N)
    )
    S = griddata((x, y), s, (X, Y), method='cubic')
    ax = plt.figure().add_subplot(111, aspect='equal')
    ax.contour(X, Y, S, N)
    plt.show()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures.mesh import Mesh
    from compas.geometry import centroid_points
    from compas.geometry import distance_point_point

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    points = [mesh.vertex_coordinates(key) for key in mesh]
    centroid = centroid_points(points)

    distances = [distance_point_point(point, centroid) for point in points]

    xy = [[points[i][0], points[i][1]] for i in range(len(points))]

    plot_scalarfield_contours(xy, distances, 20)
