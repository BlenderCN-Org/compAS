from brg.geometry.basics import length_vector


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'translate_points',
    'translate_lines',
    'rotate_points',
    'normalize_vectors',
    'scale_points',
    'mirror_points_point',
    'mirror_points_line',
    'mirror_points_plane',
    'project_points_line',
    'project_points_plane'
]


# ------------------------------------------------------------------------------
# translate
# ------------------------------------------------------------------------------


def translate_points(points, vector):
    return [[point[axis] + vector[axis] for axis in (0, 1, 2)] for point in points]


def translate_lines(lines, vector):
    sps, eps = zip(*lines)
    sps = translate_points(sps, vector)
    eps = translate_points(eps, vector)
    return zip(sps, eps)


# ------------------------------------------------------------------------------
# rotate
# ------------------------------------------------------------------------------


def rotate_points(points, axis, angle):
    raise NotImplementedError


# ------------------------------------------------------------------------------
# normalize
# ------------------------------------------------------------------------------


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
# project (not the same as pull) => projection direction is required
# ------------------------------------------------------------------------------


def scale_points(vector, f):
    """Scales vector by factor

    Parameters:
        vector (tuple, list, Vector): The vector
        f (float): scale factor

    Returns:
        Tuple: Scaled vector
    """
    return vector[0] * f, vector[1] * f, vector[2] * f


# ------------------------------------------------------------------------------
# mirror
# ------------------------------------------------------------------------------


def mirror_points_point():
    pass


def mirror_points_line():
    pass


def mirror_points_plane():
    pass


# ------------------------------------------------------------------------------
# project (not the same as pull) => projection direction is required
# ------------------------------------------------------------------------------


def project_points_plane():
    pass


def project_points_line():
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
