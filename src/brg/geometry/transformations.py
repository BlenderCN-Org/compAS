from brg.geometry.basics import length_vector
from brg.geometry.basics import add_vectors
from brg.geometry.basics import subtract_vectors
from math import cos, sin, sqrt


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


    """Rotates points around an arbitrary axis in 3D.

    Parameters:
        p1 (tuple): start point of axis
        p2 (tuple): end point of axis
        points (list of tuples): the points to rotate 
        angle (float): the angle of rotation in radians
        
    Returns:
        points (list of tuples): the rotated points 
    """
def rotate_points(p1, p2, points, angle):
    axis = subtract_vectors(p2,p1)
    x,y,z = normalize_vector(axis)
    # rotation matrix factors     
    c = cos(angle)
    t = (1 - cos(angle))
    s = sin(angle)
    # rotation matrix 
    rot_mat = [[t*x**2 + c,t*x*y - s*z,t*x*z + s*y],
        [t*x*y + s*z, t*y**2 + c,t*y*z - s*x],
        [t*x*z - s*y,t*y*z + s*x,t*z**2 + c]]
    rotated_pts = []
    for p0 in points:
        # translation vector to axis origin
        vec_trans = subtract_vectors(p0,p1)#p
        # rotation matrix * translation vector
        vec = [sum([x * y for x, y in zip(rot_mat[i],vec_trans)]) for i in xrange(3)]    
        rotated_pts.append(add_vectors(p1,vec))      
    return rotated_pts

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


def scale_vector(vector, f):
    """Scales vector by factor

    Parameters:
        vector (tuple, list, Vector): The vector
        f (float): scale factor

    Returns:
        Tuple: Scaled vector
    """
    return vector[0] * f, vector[1] * f, vector[2] * f  


def scale_points(vector, f):
    pass


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
    from math import radians,pi
    
    p1 = (0.0,0.0,0.0)
    p2 = (0.0,0.0,1.0)
    
    pts = [(1.0,1.0,1.0)]
    
    angle = pi*0.5
    
    print rotate_points(p1, p2, pts, angle)
    
