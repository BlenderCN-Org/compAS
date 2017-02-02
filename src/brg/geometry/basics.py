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
    'add_vectors_list',
    'subtract_vectors',
    'vector_component',
    'vector_component_2d',

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
]


def add_vectors_list(vectors):
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
            :nowrap:

            Ax + By + Cz + D = 0, \text{where}
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
    n = n / length_vector(n)
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


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    c = vector_component([2., 2., 3.], [0., 1., 0.])
    print(c)
