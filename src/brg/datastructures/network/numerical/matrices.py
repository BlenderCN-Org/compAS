""""""

from numpy import array
from scipy.sparse import coo_matrix


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


def adjacency_matrix(network, rtype='array'):
    k2i = dict((key, index) for index, key in network.vertices_enum())
    temp = [(1, k2i[key], k2i[nbr]) for key in network.vertices_iter() for nbr in network.neighbours(key)]
    data, rows, cols = zip(*temp)
    A = coo_matrix((data, (rows, cols)))
    if rtype == 'array':
        return A.toarray()
    elif rtype == 'csc':
        return A.tocsc()
    elif rtype == 'csr':
        return A.tocsr()
    elif rtype == 'coo':
        return A
    else:
        return A


def degree_matrix(network, rtype='array'):
    d = [(network.degree(key), index, index) for index, key in network.vertices_enum()]
    d = zip(*d)
    D = coo_matrix((d[0], (d[1], d[2])))
    if rtype == 'array':
        return D.toarray()
    elif rtype == 'csc':
        return D.tocsc()
    elif rtype == 'csr':
        return D.tocsr()
    elif rtype == 'coo':
        return D
    else:
        return D


def connectivity_matrix(network, rtype='array'):
    """"""
    k2i   = dict((key, index) for index, key in network.vertices_enum())
    edges = [(k2i[u], k2i[v]) for u, v in network.edges_iter()]
    m     = len(edges)
    data  = array([-1] * m + [1] * m)
    rows  = array(range(m) + range(m))
    cols  = array(edges).reshape((-1, 1), order='F').squeeze()
    C     = coo_matrix((data, (rows, cols)))
    if rtype == 'array':
        return C.toarray()
    elif rtype == 'csc':
        return C.tocsc()
    elif rtype == 'csr':
        return C.tocsr()
    elif rtype == 'coo':
        return C
    else:
        return C


def laplacian_matrix(network, rtype='array'):
    """Construct the Laplacian matrix of a network.

    Parameters:
        network (brg.datastructures.network.network.Network) :
            The network datastructure.
        rtype (str) :
            Optional.
            The format in which the Laplacian should be returned.
            Default is `'array'`.

    Returns:
        array-like :
            The Laplacian matrix in the format specified by `rtype`.
            Possible values are `'list'`, `'array'`, `'csr'`, '`csc`', `'coo'`

    >>> network = Network.from_obj('lines.obj')
    >>> L = laplacian_matrix(network)
    >>> x = array(network.xyz)
    >>> d = L.dot(x)
    >>> c = x - d

    """
    C = connectivity_matrix(network, rtype='csr')
    L = C.transpose().dot(C)
    if rtype == 'list':
        return L.toarray().tolist()
    if rtype == 'array':
        return L.toarray()
    if rtype == 'csr':
        return L.tocsr()
    if rtype == 'csc':
        return L.tocsc()
    if rtype == 'coo':
        return L.tocoo()
    return L


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import time
    import brg

    from brg.datastructures.network.network import Network
    from brg.geometry import centroid

    from numpy import allclose

    t0 = time.time()

    network = Network.from_obj(brg.get_data('lines.obj'))

    A = adjacency_matrix(network)
    C = connectivity_matrix(network)
    L = laplacian_matrix(network)
    D = degree_matrix(network)

    xyz = [network.vertex_coordinates(key, 'xy') for key in network.vertices_iter()]
    xyz = array(xyz, dtype=float).reshape((-1, 2))

    centroids1 = [centroid([network.vertex_coordinates(nbr, 'xy')
                  for nbr in network.neighbours(key)])
                  for key in network.vertices_iter()]

    centroids1 = array(centroids1, dtype=float)

    # d = L.dot(xyz) is currently a vector that points from the centroid to the vertex
    # therefore c = xyz - d
    # by changing the signs in the laplacian
    # the dsiplacement vectors could be used in a more natural way
    # c = xyz + d
    centroids2 = xyz - L.dot(xyz)
    centroids3 = A.dot(xyz) / D.diagonal().reshape((-1, 1))

    print allclose(centroids1, centroids2)
    print allclose(centroids1, centroids3)

    t1 = time.time()

    print t1 - t0
