from xalglib import sparsecreate
from xalglib import sparseset
from xalglib import sparseconvertotcrs


def connectivity_matrix(edges, n, rtype=None):
    """Construct a sparse connectivity matrix.

    Parameters:
        edges (list) : Pairs of vertex indices.
        n (int) : The number of vertices.
        rtype (str) : Optional. The return type. Default is `None`.

    >>> import brg
    >>> network = Network.from_lines(brg.get_data('lines.obj'))
    >>> key_index = dict((key, index) for index, key in network.vertices_enum())
    >>> edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]
    >>> n = len(network)
    >>> C = connectivity_matrix(edges, n)

    """
    m = len(edges)
    C = sparsecreate(m, n)
    for row, (i, j) in enumerate(edges):
        sparseset(C, row, i, -1)
        sparseset(C, row, j, +1)
    if rtype == 'crs':
        sparseconvertotcrs(C)
    return C


def laplacian_matrix(n, neighbours, rtype=None):
    """Construct a sparse Laplacian matrix.

    Parameters:
        n (int) : The number of vertices.
        neighbours (dict) : An adjacency dictionary. For each vertex there should
            be a list of neighbouring vertex indices.
        rtype (str) : Optional. The return type. Default is `None`.

    >>> import brg
    >>> network = Network.from_lines(brg.get_data('lines.obj'))
    >>> key_index = dict((key, index) for index, key in network.vertices_enum())
    >>> neighbours = dict((key, network.neighbours(key)) for key in network)
    >>> neighbours = dict((key_index[key], [key_index[nbr] for nbr in nbrs]))
    >>> n = len(network)
    >>> L = laplacian_matrix(n, neighbours)
    """
    L = sparsecreate(n, n)
    for i in range(n):
        nbrs = neighbours[i]
        d = len(nbrs)
        for j in nbrs:
            sparseset(L, i, j, -1.0 / d)
        sparseset(L, i, i, 1.0)
    if rtype == 'crs':
        sparseconvertotcrs(L)
    return L


def CtQC():
    pass


def CitQCi():
    pass


def CitQCf():
    pass
