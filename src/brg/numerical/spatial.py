from numpy import asarray
from numpy import argmin

from scipy.spatial import distance_matrix
from scipy.interpolate import griddata


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 20, 2016'


def closest_points_points(points, cloud, threshold=10**7, distances=True):
    """Find the closest points in a point cloud to a set of sample points.

    Note:
        Items in cloud further from items in points than threshold return zero
        distance and will affect the indices returned if not set suitably high.

    Parameters:
        points (array, list): The sample points (n,).
        cloud (array, list): The cloud points to compare to (n,).
        threshold (float): Points are checked within this distance.
        distances (boolean): Return distance matrix.

    Returns:
        list: Indices of the closest points in the cloud per point in points.
        array: Distances between points and closest points in cloud (n x n).

    Examples:
        >>> a = np.random.rand(4, 3)
        >>> b = np.random.rand(4, 3)
        >>> indices, distances = closest_points(a, b, distances=True)
        [1, 2, 0, 3]
        array([[ 1.03821946,  0.66226402,  0.67964346,  0.98877891],
               [ 0.4650432 ,  0.54484186,  0.36158995,  0.60385484],
               [ 0.19562088,  0.73240154,  0.50235761,  0.51439644],
               [ 0.84680233,  0.85390316,  0.72154983,  0.50432293]])
    """
    points = asarray(points).reshape((-1, 3))
    cloud = asarray(cloud).reshape((-1, 3))
    d_matrix = distance_matrix(points, cloud, threshold=threshold)
    indices = argmin(d_matrix, axis=1).tolist()
    if distances:
        return indices, d_matrix
    return indices


def project_points_heightfield(points, target, interp='linear', rtype='list'):
    """Project the points vertically onto the target represented by xyz points.

    Note:
        Although points can include z coordinates, they are not used.

    Parameters:
        points (array, list): Points to project (m x 3).
        target (array, list): Projection target as a height-field (n x 3).
        interp (str): Interpolation method 'linear', 'nearest', 'cubic'.
        rtype (str): Return results as 'list' else will be returned as array.

    Returns:
        (list, array): Projected points xyz co-ordinates (m x 3).

    This function uses the xyz data from target points to calculate z values
    via interpolation at the xy co-ordinates in points.
    """
    points = asarray(points).reshape((-1, 3))
    target = asarray(target).reshape((-1, 3))
    t_xy = target[:, 0:2]
    t_z  = target[:, 2]
    p_xy = points[:, 0:2]
    p_z  = griddata(t_xy, t_z, p_xy, method=interp, fill_value=0.0)
    points[:, 2] = p_z
    if rtype == 'list':
        return points.tolist()
    return points


def iterative_closest_point(a, b):
    raise NotImplementedError


ICP = iterative_closest_point


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
