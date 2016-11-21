"""brg.numerical.spatial : Numerical methods based on spatial co-ordinates."""

from numpy import array
from numpy import asarray
from numpy import argmax
from numpy import argmin
from numpy import dot
from numpy import sum
from numpy import ptp

from scipy.linalg import solve

from scipy.spatial import ConvexHull
from scipy.spatial import distance_matrix

from scipy.interpolate import griddata

from brg.geometry import cross
from brg.geometry import normalize


__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']


def closest_points_points(points, cloud, threshold=10**7, distances=True):
    """Find the closest points in a point cloud to a set of sample points.

    Note:
        Items in cloud further from items in points than threshold return zero
        distance and will affect the indices returned if not set suitably high.

    Parameters:
        points (array, list): The sample points (n,).
        cloud (array, list): The cloud points to compare to (n,).
        threshold (float): Points are checked within this distance.
        distances (boolean): Return distance matrix.

    Returns:
        list: Indices of the closest points in the cloud per point in points.
        array: Distances between points and closest points in cloud (n x n).

    Examples:
        >>> a = np.random.rand(4, 3)
        >>> b = np.random.rand(4, 3)
        >>> indices, distances = closest_points(a, b, distances=True)
        [1, 2, 0, 3]
        array([[ 1.03821946,  0.66226402,  0.67964346,  0.98877891],
               [ 0.4650432 ,  0.54484186,  0.36158995,  0.60385484],
               [ 0.19562088,  0.73240154,  0.50235761,  0.51439644],
               [ 0.84680233,  0.85390316,  0.72154983,  0.50432293]])
    """
    points = asarray(points).reshape((-1, 3))
    cloud = asarray(cloud).reshape((-1, 3))
    d_matrix = distance_matrix(points, cloud, threshold=threshold)
    indices = argmin(d_matrix, axis=1).tolist()
    if distances:
        return indices, d_matrix
    return indices


def project_points_heightfield(points, target, interp='linear', rtype='list'):
    """Project the points vertically onto the target represented by xyz points.

    Note:
        Although points can include z coordinates, they are not used.

    Parameters:
        points (array, list): Points to project (m x 3).
        target (array, list): Projection target as a height-field (n x 3).
        interp (str): Interpolation method 'linear', 'nearest', 'cubic'.
        rtype (str): Return results as 'list' else will be returned as array.

    Returns:
        (list, array): Projected points xyz co-ordinates (m x 3).

    This function uses the xyz data from target points to calculate z values
    via interpolation at the xy co-ordinates in points.
    """
    points = asarray(points).reshape((-1, 3))
    target = asarray(target).reshape((-1, 3))
    t_xy = target[:, 0:2]
    t_z  = target[:, 2]
    p_xy = points[:, 0:2]
    p_z  = griddata(t_xy, t_z, p_xy, method=interp, fill_value=0.0)
    points[:, 2] = p_z
    if rtype == 'list':
        return points.tolist()
    return points


def iterative_closest_point(a, b):
    raise NotImplementedError


ICP = iterative_closest_point


def bounding_box_2d(points, plot_hull=False):
    """Compute the aligned bounding box of set of points.

    Parameters:
        points (list) : A list of 2D points.

    Returns:
        list:
            The coordinates of the corners of the bounding box.
            This list can be used to construct a bounding box object to simplify,
            for example, plotting.

    Note:
        The *object-aligned bounding box* (OABB) is computed using the following
        procedure:

            1. Compute the convex hull of the points.
            2. For each of the edges on the hull:
                1. Compute the s-axis as the unit vector in the direction of the edge
                2. Compute the othorgonal t-axis.
                3. Use the start point of the edge as origin.
                4. Compute the spread of the points along the s-axis.
                   (dot product of the point vecor in local coordinates and the s-axis)
                5. Compute the spread along the t-axis.
                6. Determine the side of s on which the points are.
                7. Compute and store the corners of the bbox and its area.
            3. Select the box with the smallest area.

    >>> from numpy import random
    >>> points = random.rand(100, 2)
    >>> points[:, 0] *= 10.0
    >>> points[:, 1] *= 4.0
    >>> corners, area = BBOX2(points)

    """
    points = asarray(points)
    n, dim = points.shape

    assert 1 < dim, "The point coordinates should be at least 2D: %i" % dim

    points = points[:, :2]

    hull = ConvexHull(points)
    xy_hull = points[hull.vertices].reshape((-1, 2))

    if plot_hull:
        plt.plot(xy_hull[:, 0], xy_hull[:, 1], 'b-')
        plt.plot(xy_hull[[-1, 0], 0], xy_hull[[-1, 0], 1], 'b-')

    boxes = []
    m = sum(xy_hull, axis=0) / n

    for simplex in hull.simplices:
        p0 = points[simplex[0]]
        p1 = points[simplex[1]]
        # s direction
        s  = p1 - p0
        sl = sum(s ** 2) ** 0.5
        su = s / sl
        vn = xy_hull - p0
        sc = (sum(vn * s, axis=1) / sl).reshape((-1, 1))
        scmax = argmax(sc)
        scmin = argmin(sc)
        # box corners
        b0 = p0 + sc[scmin] * su
        b1 = p0 + sc[scmax] * su
        # t direction
        t  = array([-s[1], s[0]])
        tl = sum(t ** 2) ** 0.5
        tu = t / tl
        vn = xy_hull - p0
        tc = (sum(vn * t, axis=1) / tl).reshape((-1, 1))
        tcmax = argmax(tc)
        tcmin = argmin(tc)
        # area
        w = sc[scmax] - sc[scmin]
        h = tc[tcmax] - tc[tcmin]
        a = w * h
        # box corners
        if dot(t, m - p0) < 0:
            b3 = b0 - h * tu
            b2 = b1 - h * tu
        else:
            b3 = b0 + h * tu
            b2 = b1 + h * tu
        # box
        boxes.append([[b0, b1, b2, b3], a[0]])

    # return the box with the smallest area
    return min(boxes, key=lambda b: b[1])


def _compute_local_axes(a, b, c):
    u = b - a
    v = c - a
    w = cross(u, v)
    v = cross(w, u)
    return normalize(u), normalize(v), normalize(w)


def _compute_local_coords(o, uvw, xyz):
    uvw = asarray(uvw).T
    xyz = xyz.T - o.reshape((-1, 1))
    rst = solve(uvw, xyz)
    return rst.T


def _compute_global_coords(o, uvw, rst):
    uvw = asarray(uvw).T
    rst = asarray(rst).T
    xyz = uvw.dot(rst) + o.reshape((-1, 1))
    return xyz.T


def bounding_box_3d(points):
    """Compute the aligned bounding box of a set of points in 3D space.

    Parameters:
        points (list) : A list of 3D points.

    Returns:
        list:
            The coordinates of the corners of the bounding box.
            The list can be used to construct a bounding box object for easier
            plotting.

    Note:
        The implementation is based on the convex hull of the points.

    >>> ...

    """
    points = asarray(points)
    n, dim = points.shape

    assert 2 < dim, "The point coordinates should be at least 3D: %i" % dim

    points = points[:, :3]

    hull = ConvexHull(points)
    volume = None
    bbox = []

    # this can be vectorised!
    for simplex in hull.simplices:
        abc = points[simplex]
        uvw = _compute_local_axes(abc[0], abc[1], abc[2])
        xyz = points[hull.vertices]
        rst = _compute_local_coords(abc[0], uvw, xyz)
        dr, ds, dt = ptp(rst, axis=0)
        v = dr * ds * dt

        if volume is None or v < volume:
            rmin, smin, tmin = argmin(rst, axis=0)
            rmax, smax, tmax = argmax(rst, axis=0)
            bbox = [
                [rst[rmin, 0], rst[smin, 1], rst[tmin, 2]],
                [rst[rmax, 0], rst[smin, 1], rst[tmin, 2]],
                [rst[rmax, 0], rst[smax, 1], rst[tmin, 2]],
                [rst[rmin, 0], rst[smax, 1], rst[tmin, 2]],
                [rst[rmin, 0], rst[smin, 1], rst[tmax, 2]],
                [rst[rmax, 0], rst[smin, 1], rst[tmax, 2]],
                [rst[rmax, 0], rst[smax, 1], rst[tmax, 2]],
                [rst[rmin, 0], rst[smax, 1], rst[tmax, 2]],
            ]
            bbox = _compute_global_coords(abc[0], uvw, bbox)
            volume = v

    return hull, bbox, volume


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from numpy.random import rand
    from numpy.random import randint

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    from brg.numerical.xforms import rotation_matrix

    class CUBE3(object):
        """"""
        def __init__(self, points):
            self.points = points

        def plot(self, axes):
            xmin, ymin, zmin = argmin(self.points, axis=0)
            xmax, ymax, zmax = argmax(self.points, axis=0)
            xspan = self.points[xmax, 0] - self.points[xmin, 0]
            yspan = self.points[ymax, 1] - self.points[ymin, 1]
            zspan = self.points[zmax, 2] - self.points[zmin, 2]
            span = max(xspan, yspan, zspan)
            axes.plot([self.points[xmin, 0]], [self.points[ymin, 1]], [self.points[zmin, 2]], 'w')
            axes.plot([self.points[xmin, 0] + span], [self.points[ymin, 1] + span], [self.points[zmin, 2] + span], 'w')

    class HULL3(object):
        """"""
        def __init__(self, hull):
            self.vertices = hull.points
            self.faces = hull.simplices

        def plot(self, axes):
            tri = [[self.vertices[index] for index in face] for face in self.faces]
            tri_coll = Poly3DCollection(tri)
            tri_coll.set_facecolors([(0.0, 1.0, 0.0) for face in self.faces])
            axes.add_collection3d(tri_coll)

    class BBOX3(object):
        """"""
        def __init__(self, corners):
            self.corners = corners
            self.faces = [[0, 1, 2, 3], [4, 7, 6, 5], [1, 5, 6, 2], [0, 4, 5, 1], [0, 3, 7, 4], [2, 6, 7, 3]]

        def plot(self, axes):
            rec = [[self.corners[index] for index in face] for face in self.faces]
            rec_coll = Poly3DCollection(rec)
            rec_coll.set_facecolors([(1.0, 0.0, 0.0) for face in self.faces])
            rec_coll.set_alpha(0.2)
            axs.add_collection3d(rec_coll)

    points = rand(1000, 3)
    points[:, 0] *= 10.0
    points[:, 1] *= 3.0
    points[:, 2] *= 6.0

    a = randint(1, high=8) * 10 * 3.14159 / 180
    R = rotation_matrix(a, [0, 0, 1], rtype='array')

    points[:] = points.dot(R)

    hull, corners, volume = bounding_box_3d(points)

    hull3 = HULL3(hull)
    bbox3 = BBOX3(corners)
    cube3 = CUBE3(points)

    fig = plt.figure()
    axs = fig.add_subplot(111, projection='3d', aspect='equal')

    hull3.plot(axs)
    bbox3.plot(axs)
    cube3.plot(axs)

    plt.show()
