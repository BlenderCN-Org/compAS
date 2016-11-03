from functions import distance_sqrd
from functions import length
from functions import vector_component

from transformations import normalize
from transformations import scale

from arithmetic import subtract_vectors
from arithmetic import add_vectors


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 3, 2014'


def sort_points(point, cloud):
    """Sorts points of a pointcloud to a make_blocks point.

    Notes:
        Check kdTree class for an optimized implementation (MR).

    Parameters:
        point (tuple): x,y,z make_blocks point value
        cloud (sequence): A sequence locations in three-dimensional space.

    Returns:
        list (floats): min distances
        list (tuples): sorted points
        list (ints): closest point indices

    Examples:
        >>> sort_points()
    """
    minsq = [distance_sqrd(p, point) for p in cloud]
    return zip(*sorted(zip(minsq, cloud, range(len(cloud)))))


def closest_point(point, cloud):
    """Calculates the closest point to a pointcloud.

    Notes:
        Check kdTree class for an optimized implementation (MR).

    Parameters:
        point (tuple): x,y,z make_blocks point value
        cloud (sequence): A sequence locations in three-dimensional space.

    Returns:
        float: min distance
        tuple: closest point
        int: closest point index
    """
    list1, list2, list3 = sort_points(point, cloud)
    return list1[0], list2[0], list3[0]


def closest_point_on_line(p1, p2, tp):
    """
    Computes closest point on line (p1, p2) to testpoint.

    Parameters:
        p1, v1 (tuples): two 3d points defining the line
        tp (3-tuple): 3d testpoint

    Returns:
        (3-tuple): closest point on line
    """
    t = subtract_vectors(tp, p1)
    v = subtract_vectors(p2, p1)
    s = vector_component(t, v)
    return (p1[0] + s * v[0],
            p1[1] + s * v[1],
            p1[2] + s * v[2])


def closest_point_on_segment(p1, p2, tp):
    """
    Computes closest point on line segment (p1, p2) to testpoint.

    Parameters:
        p1, p2 (tuples): two 3d points defining the line segment
        tp (3-tuple): 3d testpoint

    Returns:
        (3-tuple): closest point on line segment
    """
    p  = closest_point_on_line(p1, p2, tp)
    d  = distance_sqrd(p1, p2)
    d1 = distance_sqrd(p1, p)
    d2 = distance_sqrd(p2, p)
    if d1 > d or d2 > d:
        if d1 < d2:
            return p1
        return p2
    return p


def closest_point_on_polyline(points, tp):
    # should be straight forward using the closest_point_on_line_segment function
    raise NotImplementedError


def closest_point_on_plane(p0, n, p):
    """
    Computes closest point on plane (p1, v1) to testpoint.

    Warning:
        Not tested!

    Parameters:
        p0 (sequence) : XYZ coordinates of point on plane.
        n (sequence) : XYZ coordinates of normal vecor at point ``p0``.
        p (sequence) : XYZ coordinates of point in space.

    Returns:
        (3-tuple): Closest point on plane to given point in space.

    Examples:
        >>> closest_point_to_plane()

    References:
        `Wikipedia: Distance from a point to a plane <http://en.wikipedia.org/wiki/Distance_from_a_point_to_a_plane>`_

    Todo:
        - check if this is correct (compare to previous implementation).
    """
    n  = normalize(n)
    d0 = n[0] * p[0] + n[1] * p[1] + n[2] * p[2] - (n[0] * p0[0] + n[1] * p0[1] + n[2] * p0[2])
    d  = d0 / length(n)
    n  = scale(n, - d)
    return add_vectors(p, n)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
