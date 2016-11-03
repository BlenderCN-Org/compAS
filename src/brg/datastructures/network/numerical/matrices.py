# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$


from numpy import array

from scipy.sparse import coo_matrix


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Dec 15, 2014'


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
    """"""
    C = connectivity_matrix(network, rtype='csr')
    L = C.transpose().dot(C)
    if rtype == 'array':
        return L.toarray()
    elif rtype == 'csr':
        return L.tocsr()
    elif rtype == 'csc':
        return L.tocsc()
    elif rtype == 'coo':
        return L.tocoo()
    else:
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

    centroids1 = [centroid([network.vertex_coordinates(nbr, 'xy') for nbr in network.neighbours(key)]) for key in network.vertices_iter()]
    centroids1 = array(centroids1, dtype=float)

    centroids2 = xyz - L.dot(xyz)
    centroids3 = A.dot(xyz) / D.diagonal().reshape((-1, 1))

    print allclose(centroids1, centroids2)
    print allclose(centroids1, centroids3)

    t1 = time.time()

    print t1 - t0
