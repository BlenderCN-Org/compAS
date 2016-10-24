from functions import cross
from functions import dot
from functions import center_of_mass
from functions import distance
from functions import distance_sqrd
from functions import angles
from functions import length_sqrd

from arithmetic import add_vectors
from arithmetic import subtract_vectors

from spatial import closest_point_on_line
from spatial import closest_point_on_segment


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 3, 2014'


docs = [
    'is_colinear',
    'is_coplanar',
    'is_coplanar4',
    'is_convex',
    'is_closed',
    'is_point_on_plane',
    'is_point_on_line',
    'is_point_on_segment',
    'is_point_on_polyline',
    'is_point_in_triangle',
    'is_ray_intersecting_triangle',
]


def is_colinear(a, b, c):
    """Verify if three points are colinear.

    Parameters:
        a (tuple, list, Point): Point 1.
        b (tuple, list, Point): Point 2.
        c (tuple, list, Point): Point 3.

    Returns:
        bool: True if the points are collinear, False otherwise.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1])  * (c[0] - a[0]) == 0


def is_coplanar(points):
    """Verify if the points are coplanar.

    Compute the normal vector (cross product) of the vectors formed by the first
    three points. Include one more vector at a time to compute a new normal and
    compare with the original normal. If their cross product is not zero, they
    are not parallel, which means the point are not in the same plane.

    Parameters:
        points (sequence): A sequence of locations in three-dimensional space.

    Returns:
        bool: True if the points are coplanar, False otherwise.
    """
    u = [points[1][i] - points[0][i] for i in range(3)]
    v = [points[2][i] - points[1][i] for i in range(3)]
    w = cross(u, v)
    for i in range(1, len(points) - 2):
        u = v
        v = [points[i + 2][j] - points[i + 1][j] for j in range(3)]
        wuv = cross(w, cross(u, v))
        if wuv[0] != 0 or wuv[1] != 0 or wuv[2] != 0:
            return False
    return True


def is_coplanar4(points, tol=0.01):
    """Check if 4 points are coplanar.

    Four points are coplanar if the volume of the tetrahedron defined by them is
    0. Coplanarity is equivalent to the statement that the pair of lines
    determined by the four points are not skew, and can be equivalently stated
    in vector form as (x2 - x0).[(x1 - x0) x (x3 - x2)] = 0.

    Parameters:
        points
        tol

    Returns:
        bool: True if the points are coplanar.
    """
    v01 = (points[1][0] - points[0][0], points[1][1] - points[0][1], points[1][2] - points[0][2],)
    v02 = (points[2][0] - points[0][0], points[2][1] - points[0][1], points[2][2] - points[0][2],)
    v23 = (points[3][0] - points[2][0], points[3][1] - points[2][1], points[3][2] - points[2][2],)
    res = dot(v02, cross(v01, v23))
    return res**2 < tol**2


def is_convex(points):
    c = center_of_mass(points)
    for i in range(-1, len(points) - 1):
        p0 = points[i]
        p1 = points[i - 1]
        p2 = points[i + 1]
        v0 = (c[0] - p0[0], c[1] - p0[1], c[2] - p0[2])
        v1 = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        v2 = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
        a1 = angles(v1, v0)
        a2 = angles(v0, v2)
        if a1[0] + a2[0] > 180:
            return False
    return True


def is_closed(points):
    """Verify if the points form a closed figure.

    Parameters:
        points (sequence): A sequence locations in three-dimensional space.

    Returns:
        bool: True if the figure is closed, False otherwise.
    """
    p_ = points[0]
    _p = points[-1]
    return p_[0] == _p[0] and p_[1] == _p[-1] and p_[2] and _p[2]


def is_point_on_plane(point, plane):
    """Verify if a point lies in a plane.

    Parameters:
        point (Point): A ``Point`` object.
        plane (Plane): A ``Plane`` object.
    """
    pass


def is_point_on_line(p1, v1, tp, tol=0):
    """Verify if a point (tp) is on line (p1, v1) within a tolerance (tol).

    Parameters:
        p1, v1 (tuples): 3d point and 3d vector of line
        tp (3-tuple): 3d make_blocks point
        tol (float): tolerance distance

    Returns:
        (bool): True if the point is in on the line, False otherwise.

    Todo:
        - can be done much simpler by using the algorithm used in is_point_on_line_segment

    """
    pt2 = closest_point_on_line(p1, v1, tp)
    if pt2 is None:
        return
    if distance(tp, pt2) <= tol:
        return True
    return False


def is_closest_point_on_segment(p1, p2, tp, result=True):
    """
    Verify if the closest point on a line is on line segment (p1, p2) for a testpoint tp.

    Parameters:
        p1, p2 (tuples): two 3d points defining the line segment
        tp (3-tuple): 3d testpoint
        result (bool):  if True the closest point is returned if there is a closest point
                        if False, True is returned if there is a closest point

    Returns:
        (bool/tuple): the point if the point is in on the line, False otherwise.
        (bool): True if the point is in on the line, False otherwise.

    """
    v1 = subtract_vectors(p1, p2)
    d = length_sqrd(v1)
    if d == 0:
        return
    dis = distance_sqrd(p1, p2)
    u = ((tp[0] - p1[0]) * v1[0] + (tp[1] - p1[1]) * v1[1] + (tp[2] - p1[2]) * v1[2]) / float(d)
    onlinept = (p1[0] + u * v1[0], p1[1] + u * v1[1], p1[2] + u * v1[2])
    disp1 = distance_sqrd(p1, onlinept)
    disp2 = distance_sqrd(p2, onlinept)
    if disp1 > dis or disp2 > dis:
        return False
    if result:
        return onlinept
    return True


def is_point_on_segment(p1, p2, tp, tol=0.0001):
    a = distance(p1, p2)
    b = distance(p1, tp)
    c = distance(p2, tp)
    s = 0.5 * (a + b + c)
    if a == 0:
        return False
    ha = abs((2 / a) * (s * (s - a) * (s - b) * (s - c))) ** 0.5
    if ha < tol and (b < a + tol and c < a + tol):
        return True
    return False


def is_point_on_polyline(points, tp, tol=0):
    for i in xrange(len(points) - 1):
        clospt = closest_point_on_segment(points[i], points[i + 1], tp)
        if distance(clospt, tp) <= tol:
            return True
    return False


def is_point_in_triangle(p, abc):
    """Verify if a point (p) is inside line of the triangle abc.

    Parameters:
        p (tuple): 3d point
        abc (tuples): 3d triangle points

    Returns:
        (bool): True if the point is in inside the triangle, False otherwise.
    """
    def is_on_same_side(p1, p2, a, b):
        v = subtract_vectors(b, a)
        cp1 = cross(v, subtract_vectors(p1, a))
        cp2 = cross(v, subtract_vectors(p2, a))
        if dot(cp1, cp2) >= 0:
            return True
        else:
            return False
    a, b, c = abc
    if is_on_same_side(p, a, b, c) and is_on_same_side(p, b, a, c) and is_on_same_side(p, c, a, b):
        return True
    return False


def is_ray_intersecting_triangle(p1, v1, a, b, c):
    """
    Computes the intersection of a ray (p1,v1) and a triangle (a,b,c)
    based on Moeller Trumbore intersection algorithm

    Parameters:
        p1, v1 (tuples): 3d point and 3d vector of line
        a,b,c (list of 3-tuples): 3d points of triangle

    Returns:
        (bool): True if the ray intersects with the triangle, False otherwise.
    """
    EPSILON = 0.000000001
    # Find vectors for two edges sharing V1
    e1 = subtract_vectors(b, a)
    e2 = subtract_vectors(c, a)
    # Begin calculating determinant - also used to calculate u parameter
    p = cross(v1, e2)
    # if determinant is near zero, ray lies in plane of triangle
    det = dot(e1, p)
    # NOT CULLING
    if(det > - EPSILON and det < EPSILON):
        return False
    inv_det = 1.0 / det
    # calculate distance from V1 to ray origin
    t = subtract_vectors(p1, a)
    # Calculate u parameter and make_blocks bound
    u = dot(t, p) * inv_det
    # The intersection lies outside of the triangle
    if(u < 0.0 or u > 1.0):
        return False
    # Prepare to make_blocks v parameter
    q = cross(t, e1)
    # Calculate V parameter and make_blocks bound
    v = dot(v1, q) * inv_det
    # The intersection lies outside of the triangle
    if(v < 0.0 or u + v  > 1.0):
        return False
    t = dot(e2, q) * inv_det
    if(t > EPSILON):
        return True
    # No hit, no win
    return False


def is_line_line_intersection_2d(p1, v1, p2, v2, points=False):
    """Verify if two lines intersect in 2d on the xy plane.

    Parameters:
        p1, v1 (tuples): 3d point and 3d vector of line A
        p2, v2 (tuples): 3d point and 3d vector of line B
        points (bool): if True v1,v2 will be interpreted as end points of the lines
    Returns:
        (bool): True if there is a intersection, False otherwise.

    """
    if points:
        p1b = v1
        p2b = v2
    else:
        p1b = add_vectors(p1, v1)
        p2b = add_vectors(p2, v2)
    d = (p2b[1] - p2[1]) * (p1b[0] - p1[0]) - (p2b[0] - p2[0]) * (p1b[1] - p1[1])
    if d == 0:
        return False
    return True


# def lines_intersect_in_2d():
#     return False


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
