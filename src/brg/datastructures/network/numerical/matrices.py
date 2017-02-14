from numpy import array
from scipy.sparse import coo_matrix

from brg.numerical.matrices import adjacency_matrix
from brg.numerical.matrices import degree_matrix
from brg.numerical.matrices import connectivity_matrix
from brg.numerical.matrices import laplacian_matrix
from brg.numerical.matrices import face_matrix


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


__all__ = [
    'network_adjacency_matrix',
    'network_degree_matrix',
    'network_connectivity_matrix',
    'network_laplacian_matrix',
    'network_face_matrix',
]


def _return_matrix(M, rtype):
    if rtype == 'list':
        return M.toarray().tolist()
    if rtype == 'array':
        return M.toarray()
    if rtype == 'csr':
        return M.tocsr()
    if rtype == 'csc':
        return M.tocsc()
    if rtype == 'coo':
        return M.tocoo()
    return M


def network_adjacency_matrix(network, rtype='array'):
    k_i = dict((key, index) for index, key in network.vertices_enum())
    adjacency = [[k_i[nbr] for nbr in network.neighbours(key)] for key in network.vertices_iter()]
    return adjacency_matrix(adjacency, rtype=rtype)


def network_degree_matrix(network, rtype='array'):
    k_i = dict((key, index) for index, key in network.vertices_enum())
    adjacency = [[k_i[nbr] for nbr in network.neighbours(key)] for key in network.vertices_iter()]
    return degree_matrix(adjacency, rtype=rtype)


def network_connectivity_matrix(network, rtype='array'):
    k_i   = dict((key, index) for index, key in network.vertices_enum())
    edges = [(k_i[u], k_i[v]) for u, v in network.edges_iter()]
    return connectivity_matrix(edges, rtype=rtype)


def network_laplacian_matrix(network, rtype='array'):
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
    k_i   = dict((key, index) for index, key in network.vertices_enum())
    edges = [(k_i[u], k_i[v]) for u, v in network.edges_iter()]
    return laplacian_matrix(edges, rtype=rtype)


def network_face_matrix(network, rtype='csr'):
    """Construct the face matrix of a network.

    Parameters:
        network (brg.datastructures.network.network.Network) :
            A ``brg`` network datastructure object.
        rtype (str) : Optional.
            The type of matrix to be returned. The default is ``'csr'``.

    Returns:
        ...

    The face matrix represents the relationship between faces and vertices.
    Each row of the matrix represents a face. Each column represents a vertex.
    The matrix is filled with zeros except where a relationship between a vertex
    and a face exist.

    .. math::

        F_{ij} =
        \cases{
            1 & if vertex j is part of face i \cr
            0 & otherwise
        }

    The face matrix can for example be used to compute the centroids of all
    faces of a network:

    >>> import brg
    >>> from brg.datastructures.network.network import Network
    >>> network = Network.from_obj(brg.find_resource('lines.obj'))
    >>> F = face_matrix(network, 'csr')
    >>> xyz = array([network.vertex_coordinates(key) for key in network])
    >>> c = F.dot(xyz)

    """
    k_i = dict((key, index) for index, key in network.vertices_enum())
    face_vertices = [[k_i[key] for key in network.face_vertices(fkey)] for fkey in network.faces()]
    return face_matrix(face_vertices, rtype=rtype)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import time
    import brg

    from brg.datastructures.network import Network
    from brg.geometry.planar import centroid_points_2d

    from numpy import allclose

    t0 = time.time()

    network = Network.from_obj(brg.find_resource('grid_irregular.obj'))

    key_index = dict((key, index) for index, key in network.vertices_enum())

    A = network_adjacency_matrix(network)
    C = network_connectivity_matrix(network)
    L = network_laplacian_matrix(network)
    D = network_degree_matrix(network)

    xyz = [network.vertex_coordinates(key, 'xy') for key in network.vertices_iter()]
    xyz = array(xyz, dtype=float).reshape((-1, 2))

    centroids1 = [centroid_points_2d([network.vertex_coordinates(nbr, 'xy') for nbr in network.neighbours(key)])
                  for key in network.vertices_iter()]

    centroids1 = array(centroids1, dtype=float)

    # d = L.dot(xyz) is currently a vector that points from the centroid to the vertex
    # therefore c = xyz - d
    # by changing the signs in the laplacian
    # the dsiplacement vectors could be used in a more natural way
    # c = xyz + d

    L = L / D.diagonal().reshape((-1, 1))

    d = L.dot(xyz)

    centroids2 = xyz - d
    centroids3 = A.dot(xyz) / D.diagonal().reshape((-1, 1))

    print allclose(centroids1, centroids2)
    print allclose(centroids2, centroids3)
    print allclose(centroids1, centroids3)

    for row in L.tolist():
        print row

    t1 = time.time()

    print t1 - t0

    network.plotter.vlabel = {key: index for index, key in network.vertices_enum()}
    network.plotter.lines = [{'start': xyz[key_index[key]], 'end': xyz[key_index[key]] - d[key_index[key]]} for key in network]
    network.plot()
