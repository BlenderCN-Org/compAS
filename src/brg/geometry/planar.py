from __future__ import print_function

from math import sqrt
from math import acos
from math import pi
from math import sin
from math import cos

from brg.geometry.utilities import multiply_matrix_vector


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'vector_from_points_2d',
    'circle_from_points_2d',

    'vector_component_2d',

    'add_vectors_2d',
    'subtract_vectors_2d',
    'scale_vector_2d',
    'normalize_vector_2d',
    'normalize_vectors_2d',
    'dot_vectors_2d',
    'cross_vectors_2d',

    'length_vector_2d',
    'length_vector_sqrd_2d',

    'distance_point_point_2d',
    'distance_point_point_sqrd_2d',
    'distance_point_line_2d',
    'distance_point_line_sqrd_2d',
    'distance_line_line_2d',
    'distance_line_line_sqrd_2d',

    'angles_points_2d',
    'angles_vectors_2d',
    'angle_smallest_points_2d',
    'angle_smallest_vectors_2d',

    'midpoint_line_2d',
    'centroid_points_2d',
    'center_of_mass_polygon_2d',

    'area_polygon_2d',
    'area_triangle_2d',

    'bounding_box_2d',

    'closest_point_on_line_2d',
    'closest_point_on_segment_2d',
    'closest_point_on_polyline_2d',
    'closest_part_of_triangle',

    'is_ccw_2d',
    'is_colinear_2d',
    'is_polygon_convex_2d',
    'is_point_on_line_2d',
    'is_point_on_segment_2d',
    'is_point_on_polyline_2d',
    'is_point_in_triangle_2d',
    'is_point_in_polygon_2d',
    'is_intersection_line_line_2d',
    'is_intersection_segment_segment_2d',

    'intersection_line_line_2d',
    'intersection_lines_2d',
    'intersection_circle_circle_2d',

    'translate_points_2d',
    'translate_lines_2d',

    'rotate_points_2d',

    'mirror_point_point_2d',
    'mirror_points_point_2d',
    'mirror_point_line_2d',
    'mirror_points_line_2d',

    'project_point_line_2d',
    'project_points_line_2d',
]


# ------------------------------------------------------------------------------
# constructors
# ------------------------------------------------------------------------------

def vector_from_points_2d(a, b):
    """"""
    return b[0] - a[0], b[1] - a[1]


def plane_from_points_2d(a, b, c):
    """Create a plane from three points.

    Parameters:
        a (sequence of float): XY coordinates.
        b (sequence of float): XY coordinates.
        c (sequence of float): XY coordinates.

    Returns:
        tuple: XY coordinates of base point and normal vector.
    """
    ab = subtract_vectors_2d(b, a)
    ac = subtract_vectors_2d(c, a)
    n = normalize_vector_2d(cross_vectors_2d(ab, ac))
    return a, n


def circle_from_points_2d(p1, p2, p3):
    """Create a circle from three points.

    Parameters:
        p1 (sequence of float): XY coordinates.
        p2 (sequence of float): XY coordinates.
        p3 (sequence of float): XY coordinates.

    Returns:
        tuple: XY coordinates of center and normal, and radius of the circle.

    References:
        https://en.wikipedia.org/wiki/Circumscribed_circle

    """
    ax, ay = p1[0],p1[1]
    bx, by = p2[0],p2[1]
    cx, cy = p3[0],p3[1]
    a = bx - ax
    b = by - ay
    c = cx - ax
    d = cy - ay
    e = a * (ax + bx) + b * (ay + by)
    f = c * (ax + cx) + d * (ay + cy)
    g = 2 * (a * (cy - by) - b * (cx - bx))
    if g == 0: return None
    centerx = (d * e - b * f)/g
    centery = (a * f - c * e)/g 
    r = sqrt((ax - centerx)**2 + (ay - centery)**2)
    return (centerx, centery), r

# ------------------------------------------------------------------------------
# misc
# ------------------------------------------------------------------------------


def vector_component_2d(u, v):
    x = dot_vectors_2d(u, v) / length_vector_sqrd_2d(v)
    return x * v[0], x * v[1]


# ------------------------------------------------------------------------------
# operations
# ------------------------------------------------------------------------------


def add_vectors_2d(u, v):
    """Adds two vectors.

    Parameters:
        u (sequence of float): The first vector.
        v (sequence of float): The second vector.

    Returns:
        Tuple: Resulting vector
    """
    return u[0] + v[0], u[1] + v[1]


def subtract_vectors_2d(u, v):
    """Subtracts the second vector from the first.

    Parameters:
        u (sequence of float): The first vector.
        v (sequence of float): The second vector.

    Returns:
        Tuple: Resulting vector
    """
    return u[0] - v[0], u[1] - v[1]


def scale_vector_2d(vector, scale):
    return vector[0] * scale, vector[1] * scale


def normalize_vector_2d(vector):
    """normalizes a vector

    Parameters:
        vector (sequence of float): The vector.

    Returns:
        tuple: The normalized vector.
    """
    l = float(length_vector_2d(vector))
    if l == 0.0:
        return vector
    return vector[0] / l, vector[1] / l


def normalize_vectors_2d(vectors):
    return [normalize_vector_2d(vector) for vector in vectors]


def dot_vectors_2d(u, v):
    """Compute the dot product of two vectors.

    Parameters:
        u (sequence of float): XY components of the first vector.
        v (sequence of float): XY components of the second vector.

    Returns:
        float: The dot product of the two vectors.

    Examples:
        >>> dot([1.0, 0, 0], [2.0, 0, 0])
        2

    """
    return u[0] * v[0] + u[1] * v[1]


def cross_vectors_2d(u, v):
    r"""Compute the cross product of two vectors.

    Parameters:
        u (sequence of float): XY components of the first vector.
        v (sequence of float): XY components of the second vector.

    Returns:
        list: The cross product of the two vectors.

    Exmaples:
        >>> cross([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        [0.0, 0.0, 1.0]

    """
    return [0.0, 0.0, u[0] * v[1] - u[1] * v[0]]


# ------------------------------------------------------------------------------
# length
# ------------------------------------------------------------------------------


def length_vector_2d(v):
    """Compute the length of a vector.

    Parameters:
        v (sequence of float): XY components of the vector.

    Returns:
        float: The length.

    Examples:
        >>> length([2.0, 0.0, 0.0])
        2.0

    """
    return sqrt(dot_vectors_2d(v, v))


def length_vector_sqrd_2d(v):
    """Computes the squared length of a vector.

    Parameters:
        vector (sequence): XY components of the vector.

    Returns:
        float: The squared length.

    Examples:
        >>> length_sqrd([2.0, 0.0, 0.0])
        4.0

    """
    return dot_vectors_2d(v, v)


# ------------------------------------------------------------------------------
# distance
# ------------------------------------------------------------------------------


def distance_point_point_2d(a, b):
    """Compute the distance bewteen a and b.

    Parameters:
        a (sequence of float) : XY coordinates of point a.
        b (sequence of float) : XY coordinates of point b.

    Returns:
        float: distance bewteen a and b.

    Examples:
        >>> distance([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
        2.0

    """
    ab = subtract_vectors_2d(b, a)
    return length_vector_2d(ab)


def distance_point_point_sqrd_2d(a, b):
    """Compute the squared distance bewteen points a and b.

    Parameters:
        a (sequence of float) : XY coordinates of point a.
        b (sequence of float) : XY coordinates of point b.

    Returns:
        float: distance bewteen a and b.

    Examples:
        >>> distance([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
        4.0

    See Also:
        :func:`distance_point_point_sqrd_2d`

    """
    ab = subtract_vectors_2d(b, a)
    return length_vector_sqrd_2d(ab)


def distance_point_line_2d(point, line):
    """Compute the distance between a point and a line.

    This implementation computes the *right angle distance* from a point P to a
    line defined by points A and B as twice the area of the triangle ABP divided
    by the length of AB.

    Parameters:
        point (list, tuple) : Point location.
        line (list, tuple) : Line defined by two points.

    Returns:
        float : The distance between the point and the line.

    References:
        https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line

    """
    a, b = line
    ab   = subtract_vectors_2d(b, a)
    pa   = subtract_vectors_2d(a, point)
    pb   = subtract_vectors_2d(b, point)
    l    = length_vector_2d(cross_vectors_2d(pa, pb))
    l_ab = length_vector_2d(ab)
    return l / l_ab


def distance_point_line_sqrd_2d(point, line):
    """Compute the squared distance between a point and a line."""
    a, b = line
    ab   = subtract_vectors_2d(b, a)
    pa   = subtract_vectors_2d(a, point)
    pb   = subtract_vectors_2d(b, point)
    l    = length_vector_sqrd_2d(cross_vectors_2d(pa, pb))
    l_ab = length_vector_sqrd_2d(ab)
    return l / l_ab


def distance_line_line_2d():
    raise NotImplementedError


def distance_line_line_sqrd_2d():
    raise NotImplementedError


# ------------------------------------------------------------------------------
# angles
# ------------------------------------------------------------------------------


def angles_vectors_2d(u, v):
    """Compute the angles between the XY components of two vectors.

    Parameters:
        u (sequence of float) : XY components of the first vector.
        v (sequence of float) : XY components of the second vector.

    Returns:
        tuple: The two angles.

        The smallest angle is returned first.

    """
    a = angle_smallest_vectors_2d(u, v)
    return a, 360 - a


def angles_points_2d(a, b, c):
    """Compute the angles defined by the XY components of three points.

    Parameters:
        a (sequence of float): XY coordinates.
        b (sequence of float): XY coordinates.
        c (sequence of float): XY coordinates.

    Returns:
        tuple: The two angles.

        The smallest angle is returned first.

    Notes:
        The vectors are defined in the following way

        .. math::

            \mathbf{u} = \mathbf{b} - \mathbf{a} \\
            \mathbf{v} = \mathbf{c} - \mathbf{a}

        Z components may be provided, but are simply ignored.

    """
    raise NotImplementedError


def angle_smallest_vectors_2d(u, v):
    """Compute the smallest angle between the XY components of two vectors.

    Parameters:
        u (sequence of float): XY components of the first vector.
        v (sequence of float): XY components of the second vector.

    Returns:
        float: The smallest angle.

        The angle is always positive.

    Notes:
        The vectors are defined in the following way

        .. math::

            \mathbf{u} = \mathbf{b} - \mathbf{a} \\
            \mathbf{v} = \mathbf{c} - \mathbf{a}

        Z components may be provided, but are simply ignored.

    """
    a = dot_vectors_2d(u, v) / (length_vector_2d(u) * length_vector_2d(v))
    a = max(min(a, 1), -1)
    return 180. * acos(a) / pi


def angle_smallest_points_2d(a, b, c):
    """Compute the smallest angle between vectors formed by the XY components of three points.

    Parameters:
        a (sequence of float): XY coordinates.
        b (sequence of float): XY coordinates.
        c (sequence of float): XY coordinates.

    Returns:
        float: The smallest angle.

        The angle is always positive.

    Note:
        The vectors are defined in the following way

        .. math::

            \mathbf{u} = \mathbf{b} - \mathbf{a} \\
            \mathbf{v} = \mathbf{c} - \mathbf{a}

    """
    raise NotImplementedError


# ------------------------------------------------------------------------------
# average
# ------------------------------------------------------------------------------


def centroid_points_2d(points):
    """Compute the centroid of a set of points.

    Warning:
        Duplicate points are **NOT** removed. If there are duplicates in the
        sequence, they should be there intentionally.

    Parameters:
        points (sequence): A sequence of XY coordinates.

    Returns:
        list: XY coordinates of the centroid.

    Examples:
        >>> centroid()
    """
    p = float(len(points))
    x, y = zip(*points)
    return sum(x) / p, sum(y) / p


def midpoint_line_2d(a, b):
    """Compute the midpoint of a line defined by two points.

    Parameters:
        a (sequence of float): XY coordinates of the first point.
        b (sequence of float): XY coordinates of the second point.

    Returns:
        tuple: XY coordinates of the midpoint.

    Examples:
        >>> midpoint()
    """
    return 0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])


def center_of_mass_polygon_2d(polygon):
    """Compute the center of mass of a polygon defined as a sequence of points.

    The center of mass of a polygon is the centroid of the midpoints of the edges,
    each weighted by the length of the corresponding edge.

    Parameters:
        polygon (sequence) : A sequence of XY coordinates representing the
            locations of the corners of a polygon.

    Returns:
        tuple of floats: The XY coordinates of the center of mass.

    Examples:
        >>> pts = [(0.,0.,0.),(1.,0.,0.),(0.,10.,0.)]
        >>> print "Center of mass: {0}".format(center_of_mass(pts))
        >>> print "Centroid: {0}".format(centroid(pts))

    """
    L  = 0
    cx = 0
    cy = 0
    p  = len(polygon)
    for i in range(-1, p - 1):
        p1  = polygon[i]
        p2  = polygon[i + 1]
        d   = distance_point_point_2d(p1, p2)
        cx += 0.5 * d * (p1[0] + p2[0])
        cy += 0.5 * d * (p1[1] + p2[1])
        L  += d
    cx = cx / L
    cy = cy / L
    return cx, cy


# ------------------------------------------------------------------------------
# size
# ------------------------------------------------------------------------------


def area_polygon_2d(polygon):
    """Compute the area of a polygon.

    Parameters:
        polygon (sequence): The XY coordinates of the vertices/corners of the
            polygon. The vertices are assumed to be in order. The polygon is
            assumed to be closed: the first and last vertex in the sequence should
            not be the same.

    Returns:
        float: The area of the polygon.

    """
    o = centroid_points_2d(polygon)
    u = subtract_vectors_2d(polygon[-1], o)
    v = subtract_vectors_2d(polygon[0], o)
    a = 0.5 * length_vector_2d(cross_vectors_2d(u, v))
    for i in range(0, len(polygon) - 1):
        u = v
        v = subtract_vectors_2d(polygon[i + 1], o)
        a += 0.5 * length_vector_2d(cross_vectors_2d(u, v))
    return a


def area_triangle_2d(triangle):
    """Compute the area of a triangle defined by three points.
    """
    raise NotImplementedError


# ------------------------------------------------------------------------------
# orientation
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# bounding boxes
# ------------------------------------------------------------------------------


def bounding_box_2d(points):
    """Computes the bounding box of a list of points.
    """
    x, y = zip(*points)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    return [(min_x, min_y),
            (max_x, min_y),
            (max_x, max_y),
            (min_x, max_y)]


# ------------------------------------------------------------------------------
# proximity
# ------------------------------------------------------------------------------


def closest_point_on_line_2d(point, line):
    """
    Computes closest point on line to a given point.

    Parameters:
        point (sequence of float): XY coordinates.
        line (tuple): Two points defining the line.

    Returns:
        list: XY coordinates of closest point.

    See Also:
        :func:`brg.geometry.transformations.project_point_line`

    """
    a, b = line
    ab = subtract_vectors_2d(b, a)
    ap = subtract_vectors_2d(point, a)
    c = vector_component_2d(ap, ab)
    return add_vectors_2d(a, c)


def closest_point_on_segment_2d(point, segment):
    """
    Computes closest point on line segment (p1, p2) to testpoint.

    Parameters:
        point (sequence of float): XY coordinates.
        saegment (tuple): Two points defining the segment.

    Returns:
        list: XY coordinates of closest point.

    """
    a, b = segment
    p  = closest_point_on_line_2d(point, segment)
    d  = distance_point_point_sqrd_2d(a, b)
    d1 = distance_point_point_sqrd_2d(a, p)
    d2 = distance_point_point_sqrd_2d(b, p)
    if d1 > d or d2 > d:
        if d1 < d2:
            return a
        return b
    return p


def closest_point_on_polyline_2d(point, polyline):
    raise NotImplementedError


def closest_part_of_triangle(p, triangle):
    a, b, c = triangle
    ab = subtract_vectors_2d(b, a)
    bc = subtract_vectors_2d(c, b)
    ca = subtract_vectors_2d(a, c)
    # closest to edge ab?
    ab_ = cross_vectors_2d(ab, [0, 0, 1])
    ba_ = add_vectors_2d(ab, ab_)
    if not is_ccw_2d(a, b, p) and \
       not is_ccw_2d(b, ba_, p) and \
       is_ccw_2d(a, ab_, p):
        return a, b
    # closest to edge bc?
    bc_ = cross_vectors_2d(bc, [0, 0, 1])
    cb_ = add_vectors_2d(bc, bc_)
    if not is_ccw_2d(b, c, p) and \
       not is_ccw_2d(c, cb_, p) and \
       is_ccw_2d(b, bc_, p):
        return b, c
    # closest to edge ac?
    ca_ = cross_vectors_2d(ca, [0, 0, 1])
    ac_ = add_vectors_2d(ca, ca_)
    if not is_ccw_2d(c, a, p) and \
       not is_ccw_2d(a, ac_, p) and \
       is_ccw_2d(c, ca_, p):
        return c, a
    # closest to a?
    if not is_ccw_2d(a, ab_, p) and \
       is_ccw_2d(a, ac_, p):
        return a
    # closest to b?
    if not is_ccw_2d(b, bc_, p) and \
       is_ccw_2d(b, ba_, p):
        return b
    # closest to c?
    if not is_ccw_2d(c, ca_, p) and \
       is_ccw_2d(c, cb_, p):
        return c


# ------------------------------------------------------------------------------
# queries
# ------------------------------------------------------------------------------


def is_ccw_2d(a, b, c, colinear=False):
    """Verify if ``c`` is on the left of ``ab`` when looking from ``a`` to ``b``.

    Parameters:
        a (sequence): XY coordinates.
        b (sequence): XY coordinates.
        c (sequence): XY coordinates.
        colinear (bool): Optional. Allow points to be colinear. Default is ``False``.

    Returns:
        bool : ``True`` if ccw, ``False`` otherwise.

    Examples:
        >>> is_ccw([0,0,0], [0,1,0], [-1, 0, 0])
        True
        >>> is_ccw([0,0,0], [0,1,0], [+1, 0, 0])
        False
        >>> is_ccw([0,0,0], [1,0,0], [2,0,0])
        False
        >>> is_ccw([0,0,0], [1,0,0], [2,0,0], True)
        True

    References:
        https://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation

    """
    if colinear:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1])  * (c[0] - a[0]) >= 0
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1])  * (c[0] - a[0]) > 0


def is_colinear_2d():
    raise NotImplementedError


def is_polygon_convex_2d(points, colinear=False):
    """Verify if the points form a convex figure.

    Note:
        The make_blocks is performed using the projection of the points onto the XY
        plane.

    Parameters:
        points (sequence): A sequence of points representing the polygon. The
            first and last point should not be the sane.
        colinear (bool): Are points allowed to be colinear?

    Returns:
        bool: True if the figure is convex, False otherwise.

    """
    a = points[-2]
    b = points[-1]
    c = points[0]
    direction = is_ccw_2d(a, b, c, colinear)
    for i in range(-1, len(points) - 2):
        a = b
        b = c
        c = points[i + 2]
        if direction != is_ccw_2d(a, b, c, colinear):
            return False
    return True


def is_point_on_line_2d():
    raise NotImplementedError


def is_point_on_segment_2d():
    raise NotImplementedError


def is_point_on_polyline_2d():
    raise NotImplementedError


def is_point_in_convex_polygon_2d(point, points):
    ccw = None
    for i in range(-1, len(points) - 1):
        a = points[i]
        b = points[i + 1]
        if ccw is None:
            ccw = is_ccw_2d(a, b, point, True)
        else:
            if ccw != is_ccw_2d(a, b, point, True):
                return False
    return True


def is_point_in_polygon_2d(tp, points):
    """Verify if a point is in the interior of a polygon.

    Note:
        This only makes sense in the x/y plane

    Parameters:
        points (Polygon): list of ordered points.
        tp (3-tuple): 3d make_blocks point

        not implemented:
            include_boundary (bool): Should the boundary be included in the make_blocks? Defaults to False.
            A tolerance value would be nice too... float errors are problematic
            points which are located on the boundary are not always uniquely defines as inside/outside

    Returns:
        bool: True if the point is in the polygon, False otherwise.
    """
    x, y = tp[0], tp[1]
    points = [(pt[0], pt[1]) for pt in points]  # make 2D
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def is_point_in_triangle_2d(p, triangle):
    a, b, c = triangle
    ccw = is_ccw_2d(c, a, p, True)
    if ccw != is_ccw_2d(a, b, p, True):
        return False
    if ccw != is_ccw_2d(b, c, p, True):
        return False
    return True


def is_point_in_circle_2d(point, circle):
    """Verify if a point lies a circle in 2d on the xy plane.

    Parameters:
        point (sequence of float): XY coordinates.
        circle (tuple): center, radius of the circle in the xy plane.

    Returns:
        (bool): True if there is a intersection, False otherwise.

    """
    dis = distance_point_point_2d(point, circle[0])
    if dis <= circle[1]: return True
    return False


def is_intersection_line_line_2d(l1, l2):
    """Verify if two lines intersect in 2d on the xy plane.

    Parameters:
        l1 (tuple):
        l2 (tuple):

    Returns:
        (bool): True if there is a intersection, False otherwise.

    """
    raise NotImplementedError


def is_intersection_segment_segment_2d(s1, s2):
    """Do the segments a-b and c-d intersect?

    Two segments a-b and c-d intersect, if both of the following conditions are true:

        * c is on the left of ab, and d is on the right, or vice versa
        * d is on the left of ac, and on the right of bc, or vice versa

    Parameters:
        s1: (tuple): Two points defining a segment.
        s2: (tuple): Two points defining a segment.

    Returns:
        bool: ``True`` if the segments intersect, ``False`` otherwise.

    """
    a, b = s1
    c, d = s2
    return is_ccw_2d(a, c, d) != is_ccw_2d(b, c, d) and is_ccw_2d(a, b, c) != is_ccw_2d(a, b, d)


# ==============================================================================
# intersections
# ==============================================================================


def intersection_line_line_2d(l1, l2):
    """Calculates the intersection of two lines in the XY plane.

    Parameters:
        l1 (tuple): two points.
        l2 (tuple): two points.

    Returns:
        None: if there is no intersection point.
        list: XY coordinates of intersection point.

    Note:
        If the lines are parallel, there is no intersection point.
        Two lines in the XY plane are parallel if the Z component of their
        cross product is zero.

    """
    a, b = l1
    c, d = l2
    ab = [b[i] - a[i] for i in range(2)]
    cd = [d[i] - c[i] for i in range(2)]
    div = ab[0] * cd[1] - ab[1] * cd[0]
    if div == 0.0:
        return None
    x = (a[0] * b[1] - a[1] * b[0]) * cd[0] - (c[0] * d[1] - c[1] * d[0]) * ab[0]
    y = (a[0] * b[1] - a[1] * b[0]) * cd[1] - (c[0] * d[1] - c[1] * d[0]) * ab[1]
    return [x / div, y / div]


def intersection_lines_2d():
    raise NotImplementedError


def intersection_circle_circle_2d(circle1,circle2):
    """Calculates the intersection points of two circles in 2d on the xy plane.

    Parameters:
        circle1 (tuple): center, radius of the first circle in the xy plane.
        circle2 (tuple): center, radius of the second circle in the xy plane.

    Returns:
        points (list of tuples): the intersection points if there are any
        None: if there are no intersection points

    """
    p1,r1 = circle1[0],circle1[1] 
    p2,r2 = circle2[0],circle2[1] 
    d = distance_point_point_2d(p1, p2)
    if d > r1 + r2:
        return None
    if d < abs(r1 - r2):
        return None
    if (d == 0) and (r1 == r2):
        return None
    a   = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h   = (r1 * r1 - a * a) ** 0.5
    cx2 = p1[0] + a * (p2[0] - p1[0]) / d
    cy2 = p1[1] + a * (p2[1] - p1[1]) / d
    i1  = ((cx2 + h * (p2[1] - p1[1]) / d), (cy2 - h * (p2[0] - p1[0]) / d), 0)
    i2  = ((cx2 - h * (p2[1] - p1[1]) / d), (cy2 + h * (p2[0] - p1[0]) / d), 0)
    return i1, i2


# ==============================================================================
# transformations
# ==============================================================================


def translate_points_2d(points, vector):
    return [add_vectors_2d(point, vector) for point in points]


def translate_lines_2d(lines, vector):
    sps, eps = zip(*lines)
    sps = translate_points_2d(sps, vector)
    eps = translate_points_2d(eps, vector)
    return zip(sps, eps)


# ------------------------------------------------------------------------------
# rotate
# ------------------------------------------------------------------------------


def rotate_points_2d(points, axis, angle, origin=None):
    """Rotates points around an arbitrary axis in 2D.

    Parameters:
        points (sequence of sequence of float): XY coordinates of the points.
        axis (sequence of float): The rotation axis.
        angle (float): the angle of rotation in radians.
        origin (sequence of float): Optional. The origin of the rotation axis.
            Default is ``[0.0, 0.0, 0.0]``.

    Returns:
        list: the rotated points

    References:
        https://en.wikipedia.org/wiki/Rotation_matrix

    """
    if not origin:
        origin = [0.0, 0.0]
    # rotation matrix
    x, y = normalize_vector_2d(axis)
    cosa = cos(angle)
    sina = sin(angle)
    R = [[cosa, -sina], [sina, cosa]]
    # translate points
    points = translate_points_2d(points, scale_vector_2d(origin, -1.0))
    # rotate points
    points = [multiply_matrix_vector(R, point) for point in points]
    # translate points back
    points = translate_points_2d(points, origin)
    return points


# ------------------------------------------------------------------------------
# mirror
# ------------------------------------------------------------------------------


def mirror_point_point_2d(point, mirror):
    """Mirror a point about a point.

    Parameters:
        point (sequence of float): XY coordinates of the point to mirror.
        mirror (sequence of float): XY coordinates of the mirror point.

    """
    return add_vectors_2d(mirror, subtract_vectors_2d(mirror, point))


def mirror_points_point_2d(points, mirror):
    """Mirror multiple points about a point."""
    return [mirror_point_point_2d(point, mirror) for point in points]


def mirror_point_line_2d(point, line):
    pass


def mirror_points_line_2d(points, line):
    pass


# ------------------------------------------------------------------------------
# project (not the same as pull) => projection direction is required
# ------------------------------------------------------------------------------


def project_point_line_2d(point, line):
    """Project a point onto a line.

    Parameters:
        point (sequence of float): XY coordinates.
        line (tuple): Two points defining a line.

    Returns:
        list: XY coordinates of the projected point.

    References:
        https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line

    """
    a, b = line
    ab = subtract_vectors_2d(b, a)
    ap = subtract_vectors_2d(point, a)
    c = vector_component_2d(ap, ab)
    return add_vectors_2d(a, c)


def project_points_line_2d(points, line):
    """Project multiple points onto a line."""
    return [project_point_line_2d(point, line) for point in points]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
