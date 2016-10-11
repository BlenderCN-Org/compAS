from numpy import asarray
from numpy import argmin

from scipy.spatial import distance_matrix
from scipy.interpolate import griddata


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 14, 2014'


def closest_points(points, cloud):
    """Find the closest points in a cloud to a set of sample points.

    Parameters:
        points (array-like) : The sample points.
        cloud (array-like) : The cloud in which to find the closest points to the
            sample points.

    Returns:
        list: The indices of the closest points in the cloud. The length of the list
            is equla to the number of sample points.
    """
    points = asarray(points).reshape((-1, 3))
    cloud  = asarray(cloud).reshape((-1, 3))
    return argmin(distance_matrix(points, cloud), axis=1).tolist()


def project_points(points, target, rtype='list'):
    """Project the points vertically onto the target.

    Parameters:
        points (array-like) : The points to project.
        target (array-like) : The projection target as a heightfield.

    Returns:
        list : The projected points.
    """
    points = asarray(points).reshape((-1, 3))
    target = asarray(target).reshape((-1, 3))
    t_xy = target[:, 0:2]
    t_z  = target[:, 2]
    p_xy = points[:, 0:2]
    p_z  = griddata(t_xy, t_z, p_xy, method='linear', fill_value=0.0)
    points[:, 2] = p_z
    if rtype == 'list':
        return points.tolist()
    return points
