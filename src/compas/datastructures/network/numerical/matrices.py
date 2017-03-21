from __future__ import print_function

from numpy import array

from compas.numerical.matrices import adjacency_matrix
from compas.numerical.matrices import degree_matrix
from compas.numerical.matrices import connectivity_matrix
from compas.numerical.matrices import laplacian_matrix
from compas.numerical.matrices import face_matrix


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


def network_laplacian_matrix(network, rtype='array', normalize=False):
    r"""Construct the Laplacian matrix of a network.

    Parameters:
        network (compas.datastructures.network.network.Network) :
            The network datastructure.

        rtype (str) :
            Optional.
            The format in which the Laplacian should be returned.
            Default is `'array'`.

        normalize (bool):
            Optional.
            Normalize the entries such that the value on the diagonal is ``1``.
            Default is ``False``.

    Returns:
        array-like: The Laplacian matrix in the format specified by ``rtype``.

        Possible values of ``rtype`` are ``'list'``, ``'array'``, ``'csr'``, ``'csc'``, ``'coo'``.


    Note:
        ``d = L.dot(xyz)`` is currently a vector that points from the centroid to the vertex.
        Therefore ``c = xyz - d``.
        By changing the signs in the laplacian,
        the dsiplacement vectors could be used in a more natural way ``c = xyz + d``.


    Example:

        .. plot::
            :include-source:

            from numpy import array

            import compas
            from compas.datastructures.network import Network
            from compas.datastructures.network.numerical import network_laplacian_matrix

            network = Network.from_obj(compas.get_data('grid_irregular.obj'))

            xy = array([network.vertex_coordinates(key, 'xy') for key in network])
            L  = network_laplacian_matrix(network, rtype='csr', normalize=True)
            d  = L.dot(xy)

            lines = [{'start': xy[i], 'end': xy[i] - d[i]} for i, k in network.vertices_enum()]

            network.plot(lines=lines)

    """
    k_i   = dict((key, index) for index, key in network.vertices_enum())
    edges = [(k_i[u], k_i[v]) for u, v in network.edges_iter()]
    return laplacian_matrix(edges, normalize=normalize, rtype=rtype)


def network_face_matrix(network, rtype='csr'):
    r"""Construct the face matrix of a network.

    Parameters:
        network (compas.datastructures.network.network.Network) :
            A ``compas`` network datastructure object.
        rtype (str) : Optional.
            The type of matrix to be returned. The default is ``'csr'``.

    Returns:
        array-like: The face matrix in the format specified by ``rtype``.

        Possible values of ``rtype`` are ``'list'``, ``'array'``, ``'csr'``, ``'csc'``, ``'coo'``.


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
    faces of a network.

    Example:

        .. code-block:: python

            import compas
            from compas.datastructures.network.network import Network

            network = Network.from_obj(compas.find_resource('lines.obj'))

            F   = face_matrix(network, 'csr')
            xyz = array([network.vertex_coordinates(key) for key in network])
            c   = F.dot(xyz)

    """
    k_i = dict((key, index) for index, key in network.vertices_enum())
    face_vertices = [[k_i[key] for key in network.face_vertices(fkey)] for fkey in network.faces()]
    return face_matrix(face_vertices, rtype=rtype)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures.network import Network

    from numpy import allclose

    network = Network.from_obj(compas.find_resource('grid_irregular.obj'))

    key_index = dict((key, index) for index, key in network.vertices_enum())

    A = network_adjacency_matrix(network)
    C = network_connectivity_matrix(network)
    L = network_laplacian_matrix(network, normalize=True, rtype='csr')
    D = network_degree_matrix(network)

    xy = [network.vertex_coordinates(key, 'xy') for key in network.vertices_iter()]
    xy = array(xy, dtype=float).reshape((-1, 2))

    centroids1 = [network.vertex_neighbourhood_centroid(key) for key in network.vertices_iter()]
    centroids1 = array(centroids1, dtype=float)[:, 0:2]

    d = L.dot(xy)

    centroids2 = xy - d
    centroids3 = A.dot(xy) / D.diagonal().reshape((-1, 1))

    print(allclose(centroids1, centroids2))
    print(allclose(centroids2, centroids3))
    print(allclose(centroids1, centroids3))
