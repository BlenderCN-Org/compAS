"""This module defines basic geometry functions.
All functions assume the provided input is three-dimensional. A corresponding
two-dimensional function can be accessed by appending ``_2d`` to the function
name.

>>> from brg.geometry import cross
>>> from brg.geometry import cross_2d
>>> u = [1.0, 0.0, 0.0]
>>> v = [0.0, 1.0, 0.0]
>>> cross(u, v)
[0.0, 0.0, 1.0]
>>> cross_2d(u, v)
[0.0, 0.0, 1.0]


For notes and algorithms dealing with polygons and meshes see [paulbourke]_

.. rubric:: References

.. [paulbourke] `<http://paulbourke.net/geometry/polygonmesh/>`_
"""

from math import acos
from math import pi
from math import sqrt


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 3, 2014'


SQRT_05 = sqrt(0.5)


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
    """
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def dot_2d(u, v):
    return u[0] * v[0] + u[1] * v[1]


def cross(u, v):
    """Compute the cross product of two vectors.

    Parameters:
        u (tuple, list, Vector): XYZ components of the first vector.
        v (tuple, list, Vector): XYZ components of the second vector.

    Returns:
        list: The cross product of the two vectors.

    The xyz components of the cross product of two vectors :math:`\mathbf{u}`
    and :math:`\mathbf{v}` can be computed as the *minors* of the following matrix:

    .. math::
       :nowrap:

        \\begin{bmatrix}
        x & y & z \\\\
        u_{x} & u_{y} & u_{z} \\\\
        v_{x} & v_{y} & v_{z}
        \end{bmatrix}

    Therefore, the cross product can be written as:

    .. math::
       :nowrap:

        \mathbf{u} \\times \mathbf{v}
        =
        \\begin{bmatrix}
        u_{y} * v_{z} - u_{z} * v_{y} \\\\
        u_{z} * v_{x} - u_{x} * v_{z} \\\\
        u_{x} * v_{y} - u_{y} * v_{x}
        \end{bmatrix}


    >>> cross([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    [0.0, 0.0, 1.0]

    """
    return [u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]]


def cross_2d(u, v):
    return [0.0, 0.0, u[0] * v[1] - u[1] * v[0]]


def length(v):
    """Compute the length of a vector.

    Parameters:
        v (sequence of float): XYZ components of the vector.

    Returns:
        float: The length.

    Examples:
        >>> length([2.0, 0.0, 0.0])
        2.0
    """
    return sqrt(dot(v, v))


def length_2d(v):
    return sqrt(dot_2d(v, v))


def length_sqrd(v):
    """Computes the squared length of a vector.

    Parameters:
        vector (sequence): XYZ components of the vector.

    Returns:
        float: The squared length.

    Examples:
        >>> length_sqrd([2.0, 0.0, 0.0])
        4.0
    """
    return dot(v, v)


def length_sqrd_2d(v):
    return dot_2d(v, v)


def distance(a, b):
    """Compute the distance bewteen a and b.

    Parameters:
        a (sequence of float) : XYZ coordinates of point a.
        b (sequence of float) : XYZ coordinates of point b.

    Returns:
        float: distance bewteen a and b.

    Examples:
        >>> distance([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
        2.0
    """
    v = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    return length(v)


def distance_2d(a, b):
    v = b[0] - a[0], b[1] - a[1]
    return length_2d(v)


def distance_sqrd(a, b):
    """Compute the squared distance bewteen a and b.

    Parameters:
        a (sequence of float) : XYZ coordinates of point a.
        b (sequence of float) : XYZ coordinates of point b.

    Returns:
        float: distance bewteen a and b.

    Examples:
        >>> distance([0.0, 0.0, 0.0], [2.0, 0.0, 0.0])
        4.0
    """
    v = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    return length_sqrd(v)


def distance_sqrd_2d(a, b):
    v = b[0] - a[0], b[1] - a[1]
    return length_sqrd_2d(v)


def angle_smallest(u, v):
    """Compute the smallest angle between two vectors.

    Parameters:
        u (sequence of float) : XYZ components of the first vector.
        v (sequence of float) : XYZ components of the second vector.

    Returns:
        float
            The smallest angle between the input vectors.
            The result is always positive...

    Examples:
        >>> angle_smallest([0.0, 1.0, 0.0], [1.0, 0.0, 0.0])
        90
    """
    a = dot(u, v) / (length(u) * length(v))
    a = max(min(a, 1), -1)
    return 180. * acos(a) / pi


def angle_smallest_2d(u, v):
    a = dot_2d(u, v) / (length_2d(u) * length_2d(v))
    a = max(min(a, 1), -1)
    return 180. * acos(a) / pi


def angles(u, v):
    """Compute the the 2 angles formed by a pair of vectors.

    Parameters:
        u (sequence of float) : XYZ components of the first vector.
        v (sequence of float) : XYZ components of the second vector.

    Returns:
        tuple of floats :
            The two angles.
            The smallest angle is returned first.

    Examples:
        >>> angles()
    """
    a = angle_smallest(u, v)
    return a, 360 - a


def angles_2d(u, v):
    a = angle_smallest_2d(u, v)
    return a, 360 - a


def vector_component(u, v):
    """Compute the component of u in the direction of v.

    Parameters:
        u (sequence of float) : XYZ components of the vector.
        v (sequence of float) : XYZ components of the direction.

    Returns:
        tuple: XYZ components of the component.

    Examples:
        >>> vector_component()
    """
    x = dot(u, v) / length_sqrd(v)
    return x * v[0], x * v[1], x * v[2]


def vector_component_2d(u, v):
    x = dot_2d(u, v) / length_sqrd_2d(v)
    return x * v[0], x * v[1]


def centroid(points):
    """Compute the centroid of the sequence of points.

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


def centroid_2d(points):
    p = len(points)
    return [axis / p for axis in map(sum, zip(*points))]


def midpoint(a, b):
    """Compute the midpoint of two points.

    Parameters:
        a (sequence of float): XYZ coordinates of the first point.
        b (sequence of float): XYZ coordinates of the second point.

    Returns:
        tuple: XYZ coordinates of the midpoint.

    Examples:
        >>> midpoint()
    """
    return 0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.5 * (a[2] + b[2])


def midpoint_2d(a, b):
    return 0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])


def normal(points):
    """Compute the normal of a set of points by computing the average of the
    normals of each pair of vectors formed by sets of three consecutive points.

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
    a2 = 0
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
        a2 += length(n)
        nx += n[0]
        ny += n[1]
        nz += n[2]
    return nx / a2, ny / a2, nz / a2


def normal2(points, unitize=False):
    p = len(points)
    assert p > 2, "At least three points required"
    o  = centroid(points)
    a2 = 0
    nx = 0
    ny = 0
    nz = 0
    for i in range(-1, p - 1):
        p1  = points[i]
        p2  = points[i + 1]
        v1  = p1[0] - o[0], p1[1] - o[1], p1[2] - o[2]
        v2  = p2[0] - o[0], p2[1] - o[1], p2[2] - o[2]
        n   = cross(v1, v2)
        a2 += length(n)
        nx += n[0]
        ny += n[1]
        nz += n[2]
    if not unitize:
        return 0.5 * nx, 0.5 * ny, 0.5 * nz
    return nx / a2, ny / a2, nz / a2


def center_of_mass(polygon):
    """Compute the center of mass of a polygon.

    The center of mass of a polygon is the centroid of the midpoints of the edges,
    each weighted by the length of the corresponding edge.

    Parameters:
        polygon (sequence) : A sequence of XYZ coordinates representing the
            locations of the corners of a polygon.

    Returns:
        tuple of floats: The XYZ coordinates of the center of mass.

    Examples:
        pts = [(0,0,0),(1,0,0),(0,10,0)]
        
        print ("Center of mass: {0}".format(center_of_mass(pts)))
        print ("Centroid: {0}".format(centroid(pts)))
    
    """
    L  = 0
    cx = 0
    cy = 0
    cz = 0
    p  = len(polygon)
    for i in range(-1, p - 1):
        p1  = polygon[i]
        p2  = polygon[i + 1]
        l   = distance(p1, p2)
        cx += 0.5 * l * (p1[0] + p2[0])
        cy += 0.5 * l * (p1[1] + p2[1])
        cz += 0.5 * l * (p1[2] + p2[2])
        L  += l
    cx = cx / L
    cy = cy / L
    cz = cz / L
    return cx, cy, cz


def center_of_mass_2d(polygon):
    L  = 0
    cx = 0
    cy = 0
    p  = len(polygon)
    for i in range(-1, p - 1):
        p1  = polygon[i]
        p2  = polygon[i + 1]
        l   = distance(p1, p2)
        cx += 0.5 * l * (p1[0] + p2[0])
        cy += 0.5 * l * (p1[1] + p2[1])
        L  += l
    cx = cx / L
    cy = cy / L
    return cx, cy


def area(polygon):
    """Compute the area of a polygon.

    Parameters:
        polygon (sequence): A sequence of XYZ coordinates representing the locations
            of the corners of the polygon.

    Returns:
        float: The area of the polygon.

    Examples:
        >>> area()
    """
    o = centroid(polygon)
    u = [polygon[-1][j] - o[j] for j in range(3)]
    v = [polygon[0][j] - o[j] for j in range(3)]
    a = 0.5 * length(cross(u, v))
    for i in range(0, len(polygon) - 1):
        u = v
        v = [polygon[i + 1][j] - o[j] for j in range(3)]
        a += 0.5 * length(cross(u, v))
    return a


def area_2d(polygon):
    o = centroid_2d(polygon)
    u = [polygon[-1][j] - o[j] for j in range(2)]
    v = [polygon[0][j] - o[j] for j in range(2)]
    a = 0.5 * length_2d(cross_2d(u, v))
    for i in range(0, len(polygon) - 1):
        u = v
        v = [polygon[i + 1][j] - o[j] for j in range(2)]
        a += 0.5 * length_2d(cross_2d(u, v))
    return a


def volume(polyhedron):
    """Compute the volume of a polyhedron represented by a closed mesh.

    This is an implementation of the technique described in [centroid]_.
    It is based on the divergence theorem, the fact that the *area vector* is
    constant for each face, and the fact that the area of each face can be computed
    as half the length of the cross product of two adjacent edge vectors

    .. math::
        :nowrap:

        V = \int_{P} 1
          = \\frac{1}{3} \int_{\partial P} \mathbf{x} \cdot \mathbf{n}
          = \\frac{1}{3} \sum_{i=0}^{N-1} \int{A_{i}} a_{i} \cdot n_{i}
          = \\frac{1}{6} \sum_{i=0}^{N-1} a_{i} \cdot \hat n_{i}

    .. rubric:: References

    .. [centroid] `<www.ma.ic.ac.uk/~rn/centroid.pdf>`_
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

    from brg.datastructures.mesh.mesh import Mesh

    vertices = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0],
    ]
    faces = [
        [0, 1, 2, 3],
        [4, 7, 6, 5],
        [1, 5, 6, 2],
        [2, 6, 7, 3],
        [0, 4, 5, 1],
        [3, 7, 4, 0]
    ]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    print volume(mesh)
