from brg.geometry.basics import dot
from brg.geometry.basics import vector_component
from brg.geometry.basics import normalize_vector
from brg.geometry.basics import subtract_vectors
from brg.geometry.basics import add_vectors

from brg.geometry.basics import dot_matrix_vector

from math import cos
from math import sin


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'translate_points',
    'translate_lines',
    'rotate_points',
    'scale_vector',
    'scale_vectors',
    'mirror_points_point',
    'mirror_points_line',
    'mirror_points_plane',
    'project_point_line',
    'project_points_line',
    'project_point_plane',
    'project_points_plane'
]


# ------------------------------------------------------------------------------
# translate
# ------------------------------------------------------------------------------


def translate_points(points, vector):
    return [add_vectors(point, vector) for point in points]


def translate_lines(lines, vector):
    sps, eps = zip(*lines)
    sps = translate_points(sps, vector)
    eps = translate_points(eps, vector)
    return zip(sps, eps)


# ------------------------------------------------------------------------------
# rotate
# ------------------------------------------------------------------------------


def rotate_points(points, axis, angle, origin=None):
    """Rotates points around an arbitrary axis in 3D.

    Parameters:
        points (sequence of sequence of float): XYZ coordinates of the points.
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
        origin = [0.0, 0.0, 0.0]
    # rotation matrix
    x, y, z = normalize_vector(axis)
    c = cos(angle)
    t = (1 - cos(angle))
    s = sin(angle)
    R = [
        [t * x * x + c    , t * x * y - s * z, t * x * z + s * y],
        [t * x * y + s * z, t * y * y + c    , t * y * z - s * x],
        [t * x * z - s * y, t * y * z + s * x, t * z * z + c]
    ]
    # translate points
    points = translate_points(points, scale_vector(origin, -1.0))
    # rotate points
    points = [dot_matrix_vector(R, point) for point in points]
    # translate points back
    points = translate_points(points, origin)
    return points


# ------------------------------------------------------------------------------
# project (not the same as pull) => projection direction is required
# ------------------------------------------------------------------------------


def scale_vector(vector, f):
    """Scales vector by factor

    Parameters:
        vector (sequence of float): The vector.
        f (float): The scale factor.

    Returns:
        list: the scaled vector.

    """
    f = float(f)
    return [vector[0] * f, vector[1] * f, vector[2] * f]


def scale_vectors(vectors, f):
    """Scale a list of vectors by a factor.

    Parameters:
        vectors (sequence of sequence of float): XYZ coordinates of the vectors.
        f (float): the scaling factor.

    Returns:
        list: the scaled vectors.

    """
    return [scale_vector(vector, f) for vector in vectors]


# ------------------------------------------------------------------------------
# mirror
# ------------------------------------------------------------------------------


def mirror_point_point(point, mirror):
    """Mirror a point about a point.

    Parameters:
        point (sequence of float): XYZ coordinates of the point to mirror.
        mirror (sequence of float): XYZ coordinates of the mirror point.

    """
    return add_vectors(mirror, subtract_vectors(mirror, point))


def mirror_points_point(points, mirror):
    """Mirror multiple points about a point."""
    return [mirror_point_point(point, mirror) for point in points]


def mirror_point_line(point, line):
    pass


def mirror_points_line(points, line):
    pass


def mirror_point_plane(point, plane):
    pass


def mirror_points_plane(points, plane):
    pass


# ------------------------------------------------------------------------------
# project (not the same as pull) => projection direction is required
# ?
# ------------------------------------------------------------------------------


def project_point_plane(point, plane):
    """Project a point onto a plane.

    The projection is in the direction perpendicular to the plane.
    The projercted point is thus the closest point on the plane to the original
    point.

    Parameters:
        point (sequence of float): XYZ coordinates of the original point.
        plane (tuple): Base point and normal vector defining the plane.

    Returns:
        list: XYZ coordinates of the projected point.

    Examples:

        >>> from brg.geometry.transformations import project_point_plane
        >>> point = [3.0, 3.0, 3.0]
        >>> plane = ([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])  # the XY plane
        >>> project_point_plane(point, plane)
        [3.0, 3.0, 3.0]


    References:
        http://stackoverflow.com/questions/8942950/how-do-i-find-the-orthogonal-projection-of-a-point-onto-a-plane
        http://math.stackexchange.com/questions/444968/project-a-point-in-3d-on-a-given-plane

    """
    base, normal = plane
    normal = normalize_vector(normal)
    vector = subtract_vectors(point, base)
    snormal = scale_vector(normal, dot(vector, normal))
    return subtract_vectors(point, snormal)


def project_points_plane(points, plane):
    """Project multiple points onto a plane.

    Parameters:
        points (sequence of sequence of float): Cloud of XYZ coordinates.
        plane (tuple): Base point and normal vector defining the projection plane.

    Returns:
        list of list: The XYZ coordinates of the projected points.

    See Also:
        :func:`project_point_plane`

    """
    return [project_point_plane(point, plane) for point in points]


def project_point_line(point, line):
    """Project a point onto a line.

    Parameters:
        point (sequence of float): XYZ coordinates.
        line (tuple): Two points defining a line.

    Returns:
        list: XYZ coordinates of the projected point.

    References:
        https://en.wikibooks.org/wiki/Linear_Algebra/Orthogonal_Projection_Onto_a_Line

    """
    a, b = line
    ab = subtract_vectors(b, a)
    ap = subtract_vectors(point, a)
    c = vector_component(ap, ab)
    return add_vectors(a, c)


def project_points_line(points, line):
    """Project multiple points onto a line."""
    return [project_point_line(point, line) for point in points]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from math import pi

    points = [(1.0, 1.0, 0.0), ]

    axis = (0.0, 0.0, 1.0)
    angle = pi * 0.5

    print rotate_points(points, axis, angle)

    # point = [2., 2., 10.]
    # plane = ([0., 0., 0.], [1.0, 0., 0.0])

    # print project_point_plane(point, plane)
