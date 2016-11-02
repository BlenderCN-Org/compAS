from numpy import abs
from numpy import array
from numpy import asarray
from numpy import float32
from numpy import tile

from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import diags
from scipy.sparse import vstack as svstack


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 20, 2016'


def adjacency_matrix():
    raise NotImplementedError


def degree_matrix():
    raise NotImplementedError


def connectivity_matrix(edges, rtype='array'):
    """Creates a connectivity matrix from a list of edge topologies.

    Note:
        A connectivity matrix is generally sparse and will perform superior
        in numerical calculations as a sparse matrix than a dense (array)
        matrix.

    Parameters:
        edges (list): List of lists [[node_i, node_j], [node_k, node_l]].
        rtype (str): Format of the result, 'array', 'csc', 'csr', 'coo'.

    Returns:
        sparse: If ''rtype'' is ``None, 'csc', 'csr', 'coo'``.
        array: If ''rtype'' is ``'array'``.

    The connectivity matrix displays how edges in a network are connected
    together. Each row represents an edge and has 1 and -1 inserted into the
    columns for the start and end nodes (which is the start does not matter).

    Examples:
        >>> connectivity_matrix([[0, 1], [0, 2], [0, 3]], rtype='array')
        [[-1  1  0  0]
         [-1  0  1  0]
         [-1  0  0  1]]
    """
    m    = len(edges)
    data = array([-1] * m + [1] * m)
    rows = array(range(m) + range(m))
    cols = array([edge[0] for edge in edges] + [edge[1] for edge in edges])
    C    = coo_matrix((data, (rows, cols)))
    if rtype == 'array':
        return C.toarray()
    elif rtype == 'csc':
        return C.tocsc()
    elif rtype == 'csr':
        return C.tocsr()
    elif rtype == 'coo':
        return C
    elif rtype == 'lol':
        return C.tolist()
    else:
        return C


def laplacian_matrix(edges, rtype='array'):
    """Creates a laplacian matrix from a list of edge topologies.

    Parameters:
        edges (list): List of lists [[node_i, node_j], [node_k, node_l]].
        rtype (str): Format of the result, 'array', 'csc', 'csr', 'coo'.

    Returns:
        sparse: If ''rtype'' is ``None, 'csc', 'csr', 'coo'``.
        array: If ''rtype'' is ``'array'``.

    The laplacian matrix is defined as

    .. math::
       :nowrap:

        \mathbf{L}=\mathbf{C}^\mathrm{T}\mathbf{C}

    Examples:
        >>> laplacian_matrix([[0, 1], [0, 2], [0, 3]], rtype='array')
        [[ 3 -1 -1 -1]
         [-1  1  0  0]
         [-1  0  1  0]
         [-1  0  0  1]]
    """
    C = connectivity_matrix(edges, rtype='csr')
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


def mass_matrix(Ct, E, A, l, f=0, c=1, tiled=True):
    """Creates a network's nodal mass matrix.

    Parameters:
        Ct (sparse): Sparse transpose of the connectivity matrix (n x m).
        E (array): Vector of member Young's moduli (m x 1).
        A (array): Vector of member section areas (m x 1).
        l (array): Vector of member lengths (m x 1).
        f (array): Vector of member forces (m x 1).
        c (float): Convergence factor.
        tiled (boolean): Whether to tile horizontally by 3 for x, y, z.

    Returns:
        (array): mass matrix, either (m x 1) or (m x 3).

    The mass matrix is defined as the sum of the member axial stiffnesses
    (inline) of the elements connected to each node, plus the force density.
    The force density ensures a non-zero value in form-finding/pre-stress
    modelling where E=0.

    .. math::
       :nowrap:

        \mathbf{m}=|\mathbf{C}^\mathrm{T}|(\mathbf{E}\circ\mathbf{A}\oslash\mathbf{l}+\mathbf{f}\oslash\mathbf{l})
    """
    ks = E*A/l
    m = c*(abs(Ct).dot(ks + f/l))
    if  tiled:
        return tile(m, (1, 3))
    else:
        return m


def equilibrium_matrix(C, xyz, free, rtype='array'):
    """Construct the equilibrium matrix of a structural system.

    Note:
        The matrix of vertex coordinates is vectorised to speed up the
        calculations.

    Parameters:
        C (array, sparse): Connectivity matrix (m x n).
        xyz (array, list): Array of vertex coordinates (n x 3).
        free (list): The index values of the free vertices.
        rtype (str): Format of the result, 'array', 'csc', 'csr', 'coo'.

    Returns:
        sparse: If ''rtype'' is ``None, 'csc', 'csr', 'coo'``.
        array: If ''rtype'' is ``'array'``.

    Analysis of the equilibrium matrix reveals some of the properties of the
    structural system, its size is (2ni x m) where ni is the number of free or
    internal nodes. It is calculated by

    .. math::
       :nowrap:

        \mathbf{E}
        =
        \left[
            \begin{array}{c}
                \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{U} \\[0.3em]
                \hline\\[-0.7em]
                \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{V}
            \end{array}
        \right].

    Examples:
        >>> C = connectivity_matrix([[0, 1], [0, 2], [0, 3]])
        >>> xyz = [[0, 0, 1], [0, 1, 0], [-1, -1, 0], [1, -1, 0]]
        >>> equilibrium_matrix(C, xyz, [0], rtype='array')
            [[ 0.  1. -1.]
             [-1.  1.  1.]]
    """
    xyz = asarray(xyz, dtype=float32)
    C   = csr_matrix(C)
    xy  = xyz[:, :2]
    uv  = C.dot(xy)
    U   = diags([uv[:, 0].flatten()], [0])
    V   = diags([uv[:, 1].flatten()], [0])
    Ct  = C.transpose()
    Cti = Ct[free, :]
    E   = svstack((Cti.dot(U), Cti.dot(V)))
    if rtype == 'array':
        return E.toarray()
    elif rtype == 'csr':
        return E.tocsr()
    elif rtype == 'csc':
        return E.tocsc()
    elif rtype == 'coo':
        return E.tocoo()
    else:
        return E


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg
    from brg.datastructures.network.network import Network

    network = Network.from_obj(brg.get_data('lines.obj'))

    k_i = dict((key, index) for index, key in network.vertices_enum())
    xyz = [network.vertex_coordinates(key) for key in network]
    edges = [(k_i[u], k_i[v]) for u, v in network.edges_iter()]
    C = connectivity_matrix(edges, 'csr')
    Q = diags([[2.0 for i in range(len(edges))]], [0])

    print C.shape
    print Q.shape

    res = Q.dot(C)

    print res

