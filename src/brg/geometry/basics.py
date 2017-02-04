from __future__ import print_function

from math import acos
from math import pi
from math import sqrt
from math import fabs


SQRT_05 = sqrt(0.5)


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


__all__ = [
    'add_vectors',
    'add_vectorlist',
    'subtract_vectors',
    'vector_component',
    'vector_component_2d',
    'normalize_vector',
    'normalize_vectors',

    'dot',
    'dot_2d',
    'cross',
    'cross_2d',

    'length_vector',
    'length_vector_2d',
    'length_vector_sqrd',
    'length_vector_sqrd_2d',

    'distance_point_point',
    'distance_point_point_2d',
    'distance_point_point_sqrd',
    'distance_point_point_sqrd_2d',

    'distance_point_line',
    'distance_point_line_sqrd',
    'distance_point_line_2d',
    'distance_point_line_sqrd_2d',

    'distance_point_plane',
    'distance_line_line',

    'angles_points',
    'angles_points_2d',
    'angles_vectors',
    'angles_vectors_2d',
    'angle_smallest_points',
    'angle_smallest_points_2d',
    'angle_smallest_vectors',
    'angle_smallest_vectors_2d',

    'midpoint_line',
    'midpoint_line_2d',
    'centroid_points',
    'centroid_points_2d',
    'center_of_mass_polygon',
    'center_of_mass_polygon_2d',
    'center_of_mass_polyhedron',

    'area_polygon',
    'area_polygon_2d',
    'area_triangle',
    'area_triangle_2d',

    'volume_polyhedron',

    'normal_triangle',
    'normal_polygon',

    'bounding_box',
    'bounding_box_2d',

    'sort_points',

    'closest_point',
    'closest_point_on_line',
    'closest_point_on_segment',
    'closest_point_on_plane',
    'closest_point_on_polyline',

    'is_colinear',
    'is_coplanar',
    'is_convex',
    'is_point_on_plane',
    'is_point_on_line',
    'is_point_on_segment',
    'is_point_on_polyline',
    'is_point_in_triangle',
]


# ------------------------------------------------------------------------------
# utilities
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# misc
# ------------------------------------------------------------------------------


def add_vectorlist(vectors):
    """Adds multiple 3d vectors

    Parameters:
       vectors (list): set of vectors.

    Returns:
       Tuple: Resulting vector
    """
    x, y, z = zip(*vectors)
    return sum(x), sum(y), sum(z)


def add_vectors(u, v):
    """Adds two vectors.

    Parameters:
        u (tuple, list, Vector): The first vector.
        v (tuple, list, Vector): The second vector.

    Returns:
        Tuple: Resulting vector
    """
    return u[0] + v[0], u[1] + v[1], u[2] + v[2]


def subtract_vectors(u, v):
    """Subtracts the second vector from the first.

    Parameters:
        u (tuple, list, Vector): The first vector.
        v (tuple, list, Vector): The second vector.

    Returns:
        Tuple: Resulting vector
    """
    return u[0] - v[0], u[1] - v[1], u[2] - v[2]


def vector_from_to(a, b):
    return [b[i] - a[i] for i in range(3)]


def vector_component(u, v):
    """Compute the component of u in the direction of v.

    Note:
        This is similar to computing direction cosines, or to the projection of
        a vector onto another vector. See the respective Wikipedia pages for more
        info:

            - `Direction cosine <https://en.wikipedia.org/wiki/Direction_cosine>`_
            - `Vector projection <https://en.wikipedia.org/wiki/Vector_projection>`_

    Parameters:
        u (sequence of float) : XYZ components of the vector.
        v (sequence of float) : XYZ components of the direction.

    Returns:
        tuple: XYZ components of the component.

    Examples:
        >>> vector_component([1, 2, 3], [1, 0, 0])
        [1, 0, 0]
    """
    x = dot(u, v) / length_vector_sqrd(v)
    return x * v[0], x * v[1], x * v[2]


def vector_component_2d(u, v):
    x = dot_2d(u, v) / length_vector_sqrd_2d(v)
    return x * v[0], x * v[1]


def normalize_vector(vector):
    """normalizes a vector

    Parameters:
        v1 (tuple, list, Vector): The vector.

    Returns:
        Tuple: normalized vector
    """
    l = float(length_vector(vector))
    if l <= 0:
        l = 1e-9
    return vector[0] / l, vector[1] / l, vector[2] / l


def normalize_vectors(vectors):
    return [normalize_vector(vector) for vector in vectors]


# ------------------------------------------------------------------------------
# constructors
# ------------------------------------------------------------------------------


def circle_from_points(a, b, c):
    """Create a circle from three points.

    Parameters:
        a (sequence of float): XYZ coordinates.
        a (sequence of float): XYZ coordinates.
        a (sequence of float): XYZ coordinates.

    Returns:
        tuple: center, normal, radius of the circle.

    References:
        https://en.wikipedia.org/wiki/Circumscribed_circle

    """
    ab = [b[i] - a[i] for i in range(3)]
    cb = [b[i] - c[i] for i in range(3)]
    ba = [a[i] - b[i] for i in range(3)]
    ca = [a[i] - c[i] for i in range(3)]
    ac = [c[i] - a[i] for i in range(3)]
    bc = [c[i] - b[i] for i in range(3)]
    normal = normalize_vector(cross(ab, ac))
    d = 2 * length_vector_sqrd(cross(ba, cb))
    A = length_vector_sqrd(cb) * dot(ba, ca) / d
    B = length_vector_sqrd(ca) * dot(ab, cb) / d
    C = length_vector_sqrd(ba) * dot(ac, bc) / d
    Aa = [A * a[i] for i in range(3)]
    Bb = [B * b[i] for i in range(3)]
    Cc = [C * c[i] for i in range(3)]
    center = add_vectorlist([Aa, Bb, Cc])
    radius = distance_point_point(center, a)
    return center, normal, radius


# ------------------------------------------------------------------------------
# operations
# ------------------------------------------------------------------------------


def dot(u, v):
    """Compute the dot product of two vectors.

    Parameters:
        u (tuple, list, Vector): XYZ components of the first vector.
        v (tuple, list, Vector): XYZ components of the second vector.

    Returns:
        float: The dot product of the two vectors.

    Examples:
        >>> dot([1.0, 0, 0], [2.0, 0, 0])
        2

    See Also:
        :func:`dot_2d`

    """
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def dot_2d(u, v):
    """Compute the dot product of the XY componets of two vectors."""
    return u[0] * v[0] + u[1] * v[1]


def cross(u, v):
    r"""Compute the cross product of two vectors.

    Parameters:
        u (tuple, list, Vector): XYZ components of the first vector.
        v (tuple, list, Vector): XYZ components of the second vector.

    Returns:
        list: The cross product of the two vectors.

    The xyz components of the cross product of two vectors :math:`\mathbf{u}`
    and :math:`\mathbf{v}` can be computed as the *minors* of the following matrix:

    .. math::
       :nowrap:

        \begin{bmatrix}
        x & y & z \\
        u_{x} & u_{y} & u_{z} \\
        v_{x} & v_{y} & v_{z}
        \end{bmatrix}

    Therefore, the cross product can be written as:

    .. math::
       :nowrap:

        \mathbf{u} \times \mathbf{v}
        =
        \begin{bmatrix}
        u_{y} * v_{z} - u_{z} * v_{y} \\
        u_{z} * v_{x} - u_{x} * v_{z} \\
        u_{x} * v_{y} - u_{y} * v_{x}
        \end{bmatrix}

    Exmaples:
        >>> cross([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        [0.0, 0.0, 1.0]

    See Also:
        :func:`cross_2d`

    """
    return [u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]]


def cross_2d(u, v):
    """Compute the cross product of the XY components of two vectors.

    Note:
        The resulting vector is always parallel to the Z-axis, i.e. its X and Y
        components are zero.
    """
    return [0.0, 0.0, u[0] * v[1] - u[1] * v[0]]


# ------------------------------------------------------------------------------
# length
# ------------------------------------------------------------------------------


def length_vector(v):
    """Compute the length of a vector.

    Parameters:
        v (sequence of float): XYZ components of the vector.

    Returns:
        float: The length.

    Examples:
        >>> length([2.0, 0.0, 0.0])
        2.0

    See Also:
        :func:`length_2d`

    """
    return sqrt(dot(v, v))


def length_vector_2d(v):
    """Compute the length of the XY components of a vector."""
    return sqrt(dot_2d(v, v))


def length_vector_sqrd(v):
    """Computes the squared length of a vector.

    Parameters:
        vector (sequence): XYZ components of the vector.

    Returns:
        float: The squared length.

    Examples:
        >>> length_sqrd([2.0, 0.0, 0.0])
        4.0

    See Also:
        :func:`length_sqrd_2d`

    """
    return dot(v, v)


def length_vector_sqrd_2d(v):
    """Compute the squared length of the XY components of a vector."""
    return dot_2d(v, v)


# ------------------------------------------------------------------------------
# distance
# ------------------------------------------------------------------------------


def distance_point_point(a, b):
    """Compute the distance bewteen a and b.

    Parameters:
        a (sequence of float) : XYZ coordinates of point a.
        b (sequence of float) : XYZ coordinates of point b.

    Returns:
        float: distance bewteen a and b.

    Examples:
        >>> distance([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
        2.0

    See Also:
        :func:`distance_point_point_2d`

    """
    v = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    return length_vector(v)


def distance_point_point_2d(a, b):
    v = b[0] - a[0], b[1] - a[1]
    return length_vector_2d(v)


def distance_point_point_sqrd(a, b):
    """Compute the squared distance bewteen points a and b.

    Parameters:
        a (sequence of float) : XYZ coordinates of point a.
        b (sequence of float) : XYZ coordinates of point b.

    Returns:
        float: distance bewteen a and b.

    Examples:
        >>> distance([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
        4.0

    See Also:
        :func:`distance_point_point_sqrd_2d`

    """
    v = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    return length_vector_sqrd(v)


def distance_point_point_sqrd_2d(a, b):
    v = b[0] - a[0], b[1] - a[1]
    return length_vector_sqrd_2d(v)


def distance_points_point(points, target):
    return [distance_point_point(point, target) for point in points]


def distance_point_line(point, line):
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
    ab   = [b[i] - a[i] for i in range(3)]
    pa   = [a[i] - point[i] for i in range(3)]
    pb   = [b[i] - point[i] for i in range(3)]
    l    = length_vector(cross(pa, pb))
    l_ab = length_vector(ab)
    return l / l_ab


def distance_point_line_2d(point, line):
    """Compute the distance in the XY plane between a point and a line."""
    a, b = line
    ab   = [b[i] - a[i] for i in range(2)]
    pa   = [a[i] - point[i] for i in range(2)]
    pb   = [b[i] - point[i] for i in range(2)]
    l    = length_vector_2d(cross_2d(pa, pb))
    l_ab = length_vector_2d(ab)
    return l / l_ab


def distance_point_line_sqrd(point, line):
    """Compute the squared distance between a point and a line."""
    a, b = line
    ab   = [b[i] - a[i] for i in range(3)]
    pa   = [a[i] - point[i] for i in range(3)]
    pb   = [b[i] - point[i] for i in range(3)]
    l    = length_vector_sqrd(cross(pa, pb))
    l_ab = length_vector_sqrd(ab)
    return l / l_ab


def distance_point_line_sqrd_2d(point, line):
    """Compute the squared distance in the XY plane between a point and a line."""
    a, b = line
    ab   = [b[i] - a[i] for i in range(2)]
    pa   = [a[i] - point[i] for i in range(2)]
    pb   = [b[i] - point[i] for i in range(2)]
    l    = length_vector_sqrd(cross(pa, pb))
    l_ab = length_vector_sqrd(ab)
    return l / l_ab


def distance_point_plane(point, plane):
    r"""Compute the distance from a point to a plane defined by three points.

    The distance from a pioint to a planbe can be computed from the coefficients
    of the equation of the plane and the coordinates of the point.

    Parameters:
        point (list) : Point coordinates.
        plane (tuple) : A point and a vector defining a plane.

    Returns:
        float : Distance between point and plane.

    Note:
        The equation of a plane is

        .. math::

            Ax + By + Cz + D = 0

        where

        .. math::
            :nowrap:

            \begin{align}
                D &= - Ax_0 - Bx_0 - Cz_0 \\
                Q &= (x_0, y_0, z_0) \\
                N &= (A, B, C)
            \end{align}

        with :math:`Q` a point on the plane, and :math:`N` the normal vector at
        that point. The distance of any point :math:`P` to a plane is the
        absolute value of the dot product of the vector from :math:`Q` to :math:`P`
        and the normal at :math:`Q`.

    References:
        http://mathinsight.org/distance_point_plane

    """
    base, normal = plane
    vector = [point[i] - base[i] for i in range(3)]
    return fabs(dot(vector, normal))


def distance_line_line(l1, l2):
    """Compute the distance between two skew lines.

    The distance is the absolute value of the dot product of a unit vector that
    is perpendicular to the two lines, and the vector between two points on the lines.

    If each of the lines is defined by two points (:math:`l_1 = (\mathbf{x_1}, \mathbf{x_2})`,
    :math:`l_2 = (\mathbf{x_3}, \mathbf{x_4})`), then the unit vector that is
    perpendicular to both lines is...


    Parameters:
        l1 (tuple) : Two points defining a line.
        l2 (tuple) : Two points defining a line.

    Returns:
        float : The distance between the two lines.


    References:
        http://mathworld.wolfram.com/Line-LineDistance.html
        https://en.wikipedia.org/wiki/Skew_lines#Distance

    """
    x1, x2 = l1
    x3, x4 = l2
    a = [x2[i] - x1[i] for i in range(3)]
    b = [x4[i] - x3[i] for i in range(3)]
    c = [x3[i] - x1[i] for i in range(3)]
    n = cross(a, b)
    l = length_vector(n)
    n = [n[i] / l for i in range(3)]
    return fabs(dot(n, c))


# ------------------------------------------------------------------------------
# angles
# ------------------------------------------------------------------------------


def angles_vectors(u, v):
    """Compute the the 2 angles formed by a pair of vectors.

    Parameters:
        u (sequence of float) : XYZ components of the first vector.
        v (sequence of float) : XYZ components of the second vector.

    Returns:
        tuple: The two angles.

        The smallest angle is returned first.

    """
    a = angle_smallest_vectors(u, v)
    return a, 360 - a


def angles_vectors_2d(u, v):
    """Compute the angles between the XY components of two vectors.

    Parameters:
        u (sequence of float) : XY(Z) components of the first vector.
        v (sequence of float) : XY(Z) components of the second vector.

    Returns:
        tuple: The two angles.

        The smallest angle is returned first.

    """
    a = angle_smallest_vectors_2d(u, v)
    return a, 360 - a


def angles_points(a, b, c):
    """Compute the two angles define by three points.

    Parameters:
        a (sequence of float): XYZ coordinates.
        b (sequence of float): XYZ coordinates.
        c (sequence of float): XYZ coordinates.

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
    u = [b[i] - a[i] for i in range(3)]
    v = [c[i] - a[i] for i in range(3)]
    return angles_vectors(u, v)


def angles_points_2d(a, b, c):
    """Compute the angles defined by the XY components of three points.

    Parameters:
        a (sequence of float): XY(Z) coordinates.
        b (sequence of float): XY(Z) coordinates.
        c (sequence of float): XY(Z) coordinates.

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


def angle_smallest_vectors(u, v):
    """Compute the smallest angle between two vectors.

    Parameters:
        u (sequence of float) : XYZ components of the first vector.
        v (sequence of float) : XYZ components of the second vector.

    Returns:
        float: The smallest angle.

        The angle is always positive.

    Examples:
        >>> angle_smallest([0.0, 1.0, 0.0], [1.0, 0.0, 0.0])
        90

    """
    a = dot(u, v) / (length_vector(u) * length_vector(v))
    a = max(min(a, 1), -1)
    return 180. * acos(a) / pi


def angle_smallest_vectors_2d(u, v):
    """Compute the smallest angle between the XY components of two vectors.

    Parameters:
        u (sequence of float): XY(Z) components of the first vector.
        v (sequence of float): XY(Z) components of the second vector.

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
    a = dot_2d(u, v) / (length_vector_2d(u) * length_vector_2d(v))
    a = max(min(a, 1), -1)
    return 180. * acos(a) / pi


def angle_smallest_points(a, b, c):
    """Compute the smallest angle between the vectors defined by three points.

    Parameters:
        a (sequence of float): XYZ coordinates.
        b (sequence of float): XYZ coordinates.
        c (sequence of float): XYZ coordinates.

    Returns:
        float: The smallest angle.

        The angle is always positive.

    Note:
        The vectors are defined in the following way

        .. math::

            \mathbf{u} = \mathbf{b} - \mathbf{a} \\
            \mathbf{v} = \mathbf{c} - \mathbf{a}

        Z components may be provided, but are simply ignored.

    """
    u = [b[i] - a[i] for i in range(3)]
    v = [c[i] - a[i] for i in range(3)]
    return angle_smallest_points(u, v)


def angle_smallest_points_2d(a, b, c):
    """Compute the smallest angle between vectors formed by the XY components of three points.

    Parameters:
        a (sequence of float): XY(Z) coordinates.
        b (sequence of float): XY(Z) coordinates.
        c (sequence of float): XY(Z) coordinates.

    Returns:
        float: The smallest angle.

        The angle is always positive.

    Note:
        The vectors are defined in the following way

        .. math::

            \mathbf{u} = \mathbf{b} - \mathbf{a} \\
            \mathbf{v} = \mathbf{c} - \mathbf{a}

        Z components may be provided, but are simply ignored.

    """
    raise NotImplementedError


# ------------------------------------------------------------------------------
# average
# ------------------------------------------------------------------------------


def centroid_points(points):
    """Compute the centroid of a set of points.

    Warning:
        Duplicate points are **NOT** removed. If there are duplicates in the
        sequence, they should be there intentionally.

    Parameters:
        points (sequence): A sequence of XYZ coordinates.

    Returns:
        list: XYZ coordinates of the centroid.

    Examples:
        >>> centroid()
    """
    p = len(points)
    return [axis / p for axis in map(sum, zip(*points))]


def centroid_points_2d(points):
    p = len(points)
    return [axis / p for axis in map(sum, zip(*points))]


def midpoint_line(a, b):
    """Compute the midpoint of a line defined by two points.

    Parameters:
        a (sequence of float): XYZ coordinates of the first point.
        b (sequence of float): XYZ coordinates of the second point.

    Returns:
        tuple: XYZ coordinates of the midpoint.

    Examples:
        >>> midpoint()
    """
    return 0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.5 * (a[2] + b[2])


def midpoint_line_2d(a, b):
    return 0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])


def center_of_mass_polygon(polygon):
    """Compute the center of mass of a polygon defined as a sequence of points.

    The center of mass of a polygon is the centroid of the midpoints of the edges,
    each weighted by the length of the corresponding edge.

    Parameters:
        polygon (sequence) : A sequence of XYZ coordinates representing the
            locations of the corners of a polygon.

    Returns:
        tuple of floats: The XYZ coordinates of the center of mass.

    Examples:
        >>> pts = [(0.,0.,0.),(1.,0.,0.),(0.,10.,0.)]
        >>> print "Center of mass: {0}".format(center_of_mass(pts))
        >>> print "Centroid: {0}".format(centroid(pts))

    """
    L  = 0
    cx = 0
    cy = 0
    cz = 0
    p  = len(polygon)
    for i in range(-1, p - 1):
        p1  = polygon[i]
        p2  = polygon[i + 1]
        d   = distance_point_point(p1, p2)
        cx += 0.5 * d * (p1[0] + p2[0])
        cy += 0.5 * d * (p1[1] + p2[1])
        cz += 0.5 * d * (p1[2] + p2[2])
        L  += d
    cx = cx / L
    cy = cy / L
    cz = cz / L
    return cx, cy, cz


def center_of_mass_polygon_2d(polygon):
    L  = 0
    cx = 0
    cy = 0
    p  = len(polygon)
    for i in range(-1, p - 1):
        p1  = polygon[i]
        p2  = polygon[i + 1]
        d   = distance_point_point(p1, p2)
        cx += 0.5 * d * (p1[0] + p2[0])
        cy += 0.5 * d * (p1[1] + p2[1])
        L  += d
    cx = cx / L
    cy = cy / L
    return cx, cy


def center_of_mass_polyhedron():
    """Compute the center of mass of a polyhedron"""
    raise NotImplementedError


# ------------------------------------------------------------------------------
# size
# ------------------------------------------------------------------------------


def area_polygon(polygon):
    """Compute the area of a polygon.

    Parameters:
        polygon (sequence): The XYZ coordinates of the vertices/corners of the
            polygon. The vertices are assumed to be in order. The polygon is
            assumed to be closed: the first and last vertex in the sequence should
            not be the same.

    Returns:
        float: The area of the polygon.

    """
    o = centroid_points(polygon)
    u = [polygon[-1][j] - o[j] for j in range(3)]
    v = [polygon[0][j] - o[j] for j in range(3)]
    a = 0.5 * length_vector(cross(u, v))
    for i in range(0, len(polygon) - 1):
        u = v
        v = [polygon[i + 1][j] - o[j] for j in range(3)]
        a += 0.5 * length_vector(cross(u, v))
    return a


def area_polygon_2d(polygon):
    o = centroid_points_2d(polygon)
    u = [polygon[-1][j] - o[j] for j in range(2)]
    v = [polygon[0][j] - o[j] for j in range(2)]
    a = 0.5 * length_vector_2d(cross_2d(u, v))
    for i in range(0, len(polygon) - 1):
        u = v
        v = [polygon[i + 1][j] - o[j] for j in range(2)]
        a += 0.5 * length_vector_2d(cross_2d(u, v))
    return a


def area_triangle(triangle):
    """Compute the area of a triangle defined by three points.
    """
    return 0.5 * length_vector(normal_triangle(triangle, False))


def area_triangle_2d(triangle):
    """Compute the area of the XY projection of a triangle defined by three points.
    """
    raise NotImplementedError


def volume_polyhedron(polyhedron):
    r"""Compute the volume of a polyhedron represented by a closed mesh.

    This implementation is based on the divergence theorem, the fact that the
    *area vector* is constant for each face, and the fact that the area of each
    face can be computed as half the length of the cross product of two adjacent
    edge vectors.

    .. math::
        :nowrap:

        \begin{align}
            V  = \int_{P} 1
              &= \frac{1}{3} \int_{\partial P} \mathbf{x} \cdot \mathbf{n} \\
              &= \frac{1}{3} \sum_{i=0}^{N-1} \int{A_{i}} a_{i} \cdot n_{i} \\
              &= \frac{1}{6} \sum_{i=0}^{N-1} a_{i} \cdot \hat n_{i}
        \end{align}


    References:
        http://www.ma.ic.ac.uk/~rn/centroid.pdf

    """
    V = 0
    for fkey in polyhedron.face:
        vertices = polyhedron.face_vertices(fkey, ordered=True)
        if len(vertices) == 3:
            faces = [vertices]
        else:
            faces = []
            for i in range(1, len(vertices) - 1):
                faces.append(vertices[0:1] + vertices[i:i + 2])
        for face in faces:
            a  = polyhedron.vertex_coordinates(face[0])
            b  = polyhedron.vertex_coordinates(face[1])
            c  = polyhedron.vertex_coordinates(face[2])
            ab = [b[i] - a[i] for i in range(3)]
            ac = [c[i] - a[i] for i in range(3)]
            n  = cross(ab, ac)
            V += dot(a, n)
    return V / 6.


# ------------------------------------------------------------------------------
# orientation
# ------------------------------------------------------------------------------


def normal_polygon(points, unitized=True):
    """Compute the normal of a polygon defined by a sequence of points.

    Note:
        The points in the list should be unique. For example, the first and last
        point in the list should not be the same.

    Parameters:
        points (sequence): A sequence of points.

    Returns:
        list: The normal vector.

    Raises:
        ValueError: If less than three points are provided.
    """
    p = len(points)
    assert p > 2, "At least three points required"
    nx = 0
    ny = 0
    nz = 0
    for i in range(-1, p - 1):
        p1  = points[i - 1]
        p2  = points[i]
        p3  = points[i + 1]
        v1  = [p1[axis] - p2[axis] for axis in range(3)]
        v2  = [p3[axis] - p2[axis] for axis in range(3)]
        n   = cross(v1, v2)
        nx += n[0]
        ny += n[1]
        nz += n[2]
    if not unitized:
        # since the length of the cross product vector is twice the area of the
        # triangle formed by vectors involved in the cross product
        return 0.5 * nx, 0.5 * ny, 0.5 * nz
    a2 = length_vector([nx, ny, nz])
    return nx / a2, ny / a2, nz / a2


def normal_triangle(triangle, unitized=True):
    """Compute the normal vector of a triangle.
    """
    assert len(triangle) == 3, "Three points are required."
    a, b, c = triangle
    ab = [b[i] - a[i] for i in range(3)]
    ac = [c[i] - a[i] for i in range(3)]
    n  = cross(ab, ac)
    if not unitized:
        return n
    lvec = length_vector(n)
    return n[0] / lvec, n[1] / lvec, n[2] / lvec


# ------------------------------------------------------------------------------
# bounding boxes
# ------------------------------------------------------------------------------


def bounding_box(points):
    """Computes the bounding box of a list of points.
    """
    x, y, z = zip(*points)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    min_z = min(z)
    max_z = max(z)
    return [(min_x, min_y, min_z),
            (max_x, min_y, min_z),
            (max_x, max_y, min_z),
            (min_x, max_y, min_z),
            (min_x, min_y, max_z),
            (max_x, min_y, max_z),
            (max_x, max_y, max_z),
            (min_x, max_y, max_z)]


def bounding_box_2d(points):
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


def sort_points(point, cloud):
    """Sorts points of a pointcloud to a point.

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
    minsq = [distance_point_point_sqrd(p, point) for p in cloud]
    return sorted(zip(minsq, cloud, range(len(cloud))), key=lambda x: x[0])


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
    data = sort_points(point, cloud)
    return data[0]


def closest_point_on_line(point, line):
    """
    Computes closest point on line to a given point.

    Parameters:
        point (sequence of float): XYZ coordinates.
        line (tuple): Two points defining the line.

    Returns:
        list: XYZ coordinates of closest point.

    See Also:
        :func:`brg.geometry.transformations.project_point_line`

    """
    a, b = line
    ab = [b[i] - a[i] for i in range(3)]
    ap = [point[i] - a[i] for i in range(3)]
    c = vector_component(ap, ab)
    return [a[i] + c[i] for i in range(3)]


def closest_point_on_segment(point, segment):
    """
    Computes closest point on line segment (p1, p2) to testpoint.

    Parameters:
        point (sequence of float): XYZ coordinates.
        saegment (tuple): Two points defining the segment.

    Returns:
        list: XYZ coordinates of closest point.

    """
    a, b = segment
    p  = closest_point_on_line(point, segment)
    d  = distance_point_point_sqrd(a, b)
    d1 = distance_point_point_sqrd(a, p)
    d2 = distance_point_point_sqrd(b, p)
    if d1 > d or d2 > d:
        if d1 < d2:
            return a
        return b
    return p


def closest_point_on_polyline(point, polyline):
    # should be straight forward using the closest_point_on_line_segment function
    raise NotImplementedError


def closest_point_on_plane(point, plane):
    """
    Compute closest point on a plane to a given point.

    Parameters:
        point (sequenceof float): XYZ coordinates of point.
        plane (tuple): The base point and normal defining the plane.

    Returns:
        (list): XYZ coordinates of the closest point.

    Examples:
        >>> plane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
        >>> point = [1.0, 2.0, 3.0]
        >>> closest_point_on_plane(point, plane)

    References:
        http://en.wikipedia.org/wiki/Distance_from_a_point_to_a_plane

    """
    base, normal = plane
    x, y, z = base
    a, b, c  = normalize_vector(normal)
    x1, y1, z1 = point
    d = a * x + b * y + c * z
    k = (a * x1 + b * y1 + c * z1 - d) / (a**2 + b**2 + c**2)
    return [x1 - k * a,
            y1 - k * b,
            z1 - k * c, ]


# ------------------------------------------------------------------------------
# queries
# ------------------------------------------------------------------------------


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


def is_coplanar(points, tol=0.01):
    """Verify if the points are coplanar.

    Compute the normal vector (cross product) of the vectors formed by the first
    three points. Include one more vector at a time to compute a new normal and
    compare with the original normal. If their cross product is not zero, they
    are not parallel, which means the point are not in the same plane.

    Four points are coplanar if the volume of the tetrahedron defined by them is
    0. Coplanarity is equivalent to the statement that the pair of lines
    determined by the four points are not skew, and can be equivalently stated
    in vector form as (x2 - x0).[(x1 - x0) x (x3 - x2)] = 0.

    Parameters:
        points (sequence): A sequence of locations in three-dimensional space.

    Returns:
        bool: True if the points are coplanar, False otherwise.

    """
    tol2 = tol ** 2
    if len(points) == 4:
        v01 = (points[1][0] - points[0][0], points[1][1] - points[0][1], points[1][2] - points[0][2],)
        v02 = (points[2][0] - points[0][0], points[2][1] - points[0][1], points[2][2] - points[0][2],)
        v23 = (points[3][0] - points[2][0], points[3][1] - points[2][1], points[3][2] - points[2][2],)
        res = dot(v02, cross(v01, v23))
        return res**2 < tol2
    # len(points) > 4
    # compare length of cross product vector to tolerance
    u = [points[1][i] - points[0][i] for i in range(3)]
    v = [points[2][i] - points[1][i] for i in range(3)]
    w = cross(u, v)
    for i in range(1, len(points) - 2):
        u = v
        v = [points[i + 2][j] - points[i + 1][j] for j in range(3)]
        wuv = cross(w, cross(u, v))
        if wuv[0]**2 > tol2 or wuv[1]**2 > tol2 or wuv[2]**2 > tol2:
            return False
    return True


def is_polygon_convex(polygon):
    """Verify if a polygon is convex.

    Parameters:
        polygon (sequence of sequence of floats): The XYZ coordinates of the
            corners of the polygon.

    Note:
        Use this function for *spatial* polygons.
        If the polygon is in a horizontal plane, use :func:`brg.geometry.planar.is_polygon_convex`
        instead.

    See Also:
        :func:`brg.geometry.planar.is_polygon_convex`

    """
    c = center_of_mass_polygon(polygon)
    for i in range(-1, len(polygon) - 1):
        p0 = polygon[i]
        p1 = polygon[i - 1]
        p2 = polygon[i + 1]
        v0 = (c[0] - p0[0], c[1] - p0[1], c[2] - p0[2])
        v1 = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        v2 = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
        a1, _ = angles_vectors(v1, v0)
        a2, _ = angles_vectors(v0, v2)
        if a1 + a2 > 180:
            return False
    return True


def is_point_on_plane(point, plane, tol=0.0):
    """Verify if a point lies in a plane.

    Parameters:
        point (sequence of float): XYZ coordinates.
        plane (tuple): Base point and normal defining a plane.
        tol (float): Optional. A tolerance. Default is ``0.0``.

    Returns:
        (bool): True if the point is in on the plane, False otherwise.

    """
    d = distance_point_plane(point, plane)
    return d <= tol


def is_point_on_line(point, line, tol=0.0):
    """Verify if a point lies on a line.

    Parameters:
        point (sequence of float): XYZ coordinates.
        line (tuple): Two points defining a line.
        tol (float): Optional. A tolerance. Default is ``0.0``.

    Returns:
        (bool): True if the point is in on the line, False otherwise.

    """
    d = distance_point_line(point, line)
    return d <= tol


def is_point_on_segment(point, segment, tol=0.0):
    a, b = segment
    if not is_point_on_line(point, segment, tol=tol):
        return False
    d_ab = distance_point_point(a, b)
    if d_ab == 0:
        return False
    d_pa = distance_point_point(a, point)
    d_pb = distance_point_point(b, point)
    if d_pa + d_pb <= d_ab + tol:
        return True
    return False


def is_closest_point_on_segment(point, segment, tol=0.0, return_point=False):
    """Verify if the closest point on the line of a segment is on the segment.

    Parameters:
        point (sequence of float): XYZ coordinates of the point.
        segment (tuple): Two points defining the line segment.
        tol (float): Optional. A tolerance. Default is ``0.0``.
        return_point (bool): Optional. If ``True`` return the closest point.
            Default is ``False``.

    Returns:
        (bool/tuple): the point if the point is in on the line, False otherwise.
        (bool): True if the point is in on the line, False otherwise.

    """
    a, b = segment
    v = [b[i] - a[i] for i in range(3)]
    d_ab = distance_point_point_sqrd(a, b)
    if d_ab == 0:
        return
    u = sum((point[i] - a[i]) * v[i] for i in range(3)) / d_ab
    c = a[0] + u * v[0], a[1] + u * v[1], a[2] + u * v[2]
    d_ac = distance_point_point_sqrd(a, c)
    d_bc = distance_point_point_sqrd(b, c)
    if d_ac + d_bc <= d_ab + tol:
        if return_point:
            return c
        return True
    return False


def is_point_on_polyline(point, polyline, tol=0.0):
    """Verify if a point is on a polyline.

    Parameters:
        point (sequence of float): XYZ coordinates.
        polyline (sequence of sequence of float): XYZ coordinates of the points
            of the polyline.
        tol (float): Optional. The tolerance. Default is ``0.0``.

    Returns:
        bool: ``True`` if the point is on the polyline. ``False`` otherwise.

    """
    for i in xrange(len(polyline) - 1):
        a = polyline[i]
        b = polyline[i + 1]
        c = closest_point_on_segment(point, (a, b))
        if distance_point_point(point, c) <= tol:
            return True
    return False


def is_point_in_triangle(point, triangle):
    """Verify if a point is in the interior of a triangle.

    Parameters:
        point (sequence of float): XYZ coordinates.
        triangle (sequence of sequence of float): XYZ coordinates of the triangle corners.

    Returns:
        (bool): True if the point is in inside the triangle, False otherwise.

    Note:
        Should the point be in the same plane as the triangle?

    See Also:
        :func:`brg.geometry.planar.is_point_in_triangle`

    """
    def is_on_same_side(p1, p2, segment):
        a, b = segment
        v = vector_from_to(a, b)
        c1 = cross(v, vector_from_to(a, p1))
        c2 = cross(v, vector_from_to(a, p2))
        if dot(c1, c2) >= 0:
            return True
        else:
            return False
    a, b, c = triangle
    if is_on_same_side(point, a, (b, c)) and \
       is_on_same_side(point, b, (a, c)) and \
       is_on_same_side(point, c, (a, b)):
        return True
    return False


def is_point_in_circle(point, circle):
    center, normal, radius = circle
    if is_point_on_plane(point, (center, normal)):
        return distance_point_point(point, center) <= radius
    return False


# def is_line_line_intersection_2d(p1, v1, p2, v2, points=False):
#     """Verify if two lines intersect in 2d on the xy plane.

#     Parameters:
#         p1, v1 (tuples): 3d point and 3d vector of line A
#         p2, v2 (tuples): 3d point and 3d vector of line B
#         points (bool): if True v1,v2 will be interpreted as end points of the lines
#     Returns:
#         (bool): True if there is a intersection, False otherwise.

#     """
#     if points:
#         p1b = v1
#         p2b = v2
#     else:
#         p1b = add_vectors(p1, v1)
#         p2b = add_vectors(p2, v2)
#     d = (p2b[1] - p2[1]) * (p1b[0] - p1[0]) - (p2b[0] - p2[0]) * (p1b[1] - p1[1])
#     if d == 0:
#         return False
#     return True


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    c = vector_component([2., 2., 3.], [0., 1., 0.])
    print(c)
