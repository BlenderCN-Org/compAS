from brg.numerical.linalg import normrow


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 20, 2016'


def lengths(C, X):
    """Calculates the lengths and co-ordinate differences.

    Parameters:
        C (sparse): Connectivity matrix (m x n)
        X (array): Co-ordinates of vertices/points (n x 3).

    Returns:
        array: Vectors of co-ordinate differences in x, y and z (m x 3).
        array: Lengths of members (m x 1)

    Examples:
        >>> C = connectivity_matrix([[0, 1], [1, 2]], 'csr')
        >>> X = array([[0, 0, 0], [1, 1, 0], [0, 0, 1]])
        >>> uvw
        array([[ 1,  1,  0],
               [-1, -1,  1]])
        >>> l
        array([[ 1.41421356],
               [ 1.73205081]])
    """
    uvw = C.dot(X)
    l = normrow(uvw)
    return uvw, l
