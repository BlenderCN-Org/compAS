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
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'adjacency_matrix',
    'degree_matrix',
    'connectivity_matrix',
    'laplacian_matrix',
    'face_matrix',
    'mass_matrix',
    'stiffness_matrix',
    'equilibrium_matrix'
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


def adjacency_matrix(adjacency, rtype='array'):
    a = [(1, i, j) for i in range(len(adjacency)) for j in adjacency[i]]
    data, rows, cols = zip(*a)
    A = coo_matrix((data, (rows, cols)))
    return _return_matrix(A, rtype)


def degree_matrix(adjacency, rtype='array'):
    d = [(len(adjacency[i]), i, i) for i in range(len(adjacency))]
    data, rows, cols = zip(*d)
    D = coo_matrix((data, (rows, cols)))
    return _return_matrix(D, rtype)


def connectivity_matrix(edges, rtype='array'):
    """Creates a connectivity matrix from a list of vertex index pairs.

    The connectivity matrix encodes how edges in a network are connected
    together. Each row represents an edge and has 1 and -1 inserted into the
    columns for the start and end nodes.

    .. math::

        \mathbf{C}_{ij} =
        \cases{
            -1 & if edge i starts at vertex j \cr
            +1 & if edge i ends at vertex j \cr
            0  & otherwise
        }

    Note:
        A connectivity matrix is generally sparse and will perform superior
        in numerical calculations as a sparse matrix.

    Parameters:
        edges (list of list): List of lists [[node_i, node_j], [node_k, node_l]].
        rtype (str): Format of the result, 'array', 'csc', 'csr', 'coo'.

    Returns:
        sparse: If ``rtype`` is ``None``, ``'csc'``, ``'csr'``, ``'coo'``.

        array: If ``rtype`` is ``'array'``.

    Examples:
        >>> connectivity_matrix([[0, 1], [0, 2], [0, 3]], rtype='array')
        [[-1  1  0  0]
         [-1  0  1  0]
         [-1  0  0  1]]

    """
    m    = len(edges)
    data = array([-1] * m + [1] * m)
    rows = array(list(range(m)) + list(range(m)))
    cols = array([edge[0] for edge in edges] + [edge[1] for edge in edges])
    C    = coo_matrix((data, (rows, cols)))
    return _return_matrix(C, rtype)


def laplacian_matrix(edges, rtype='array'):
    """Creates a laplacian matrix from a list of edge topologies.

    The laplacian matrix is defined as

    .. math::

        \mathbf{L} = \mathbf{C} ^ \mathrm{T} \mathbf{C}

    Note:
        The current implementation only supports umbrella weights, 
        as other weighting schemes are not generally applicable.

    See also:
        :func:`brg.datastructures.network.numerical.matrices.network_laplacian_matrix`
        :func:`brg.datastructures.mesh.numerical.matrices.mesh_laplacian_matrix`
        :func:`brg.datastructures.mesh.numerical.matrices.trimesh_cotangent_laplacian_matrix`
        :func:`brg.datastructures.mesh.numerical.matrices.trimesh_positive_cotangent_laplacian_matrix`

    Parameters:
        edges (list of list): List of lists [[node_i, node_j], [node_k, node_l]].
        rtype (str): Format of the result, 'array', 'csc', 'csr', 'coo'.

    Returns:
        sparse: If ''rtype'' is ``None, 'csc', 'csr', 'coo'``.
        array: If ''rtype'' is ``'array'``.

    Examples:
        >>> laplacian_matrix([[0, 1], [0, 2], [0, 3]], rtype='array')
        [[ 3 -1 -1 -1]
         [-1  1  0  0]
         [-1  0  1  0]
         [-1  0  0  1]]

    """
    C = connectivity_matrix(edges, rtype='csr')
    L = C.transpose().dot(C)
    return _return_matrix(L, rtype)


def face_matrix(face_vertices, rtype='array'):
    """Creates a face-vertex adjacency matrix.
    
    Parameters:
        face_vertices (list of list) : List of vertices per face.
        rtype (str) : The return type.

    """
    f = array([(i, j, 1) for i, vertices in enumerate(face_vertices) for j in vertices])
    F = coo_matrix((f[:, 2], (f[:, 0], f[:, 1])))
    return _return_matrix(F, rtype)


def mass_matrix(Ct, E, A, l, f=0, c=1, tiled=True):
    """Creates a network's nodal mass matrix.

    The mass matrix is defined as the sum of the member axial stiffnesses
    (inline) of the elements connected to each node, plus the force density.
    The force density ensures a non-zero value in form-finding/pre-stress
    modelling where E=0.

    .. math::

        \mathbf{m} = |\mathbf{C}^\mathrm{T}| (\mathbf{E} \circ \mathbf{A} \oslash \mathbf{l} + \mathbf{f} \oslash \mathbf{l})

    Parameters:
        Ct (sparse): Sparse transpose of the connectivity matrix (n x m).
        E (array): Vector of member Young's moduli (m x 1).
        A (array): Vector of member section areas (m x 1).
        l (array): Vector of member lengths (m x 1).
        f (array): Vector of member forces (m x 1).
        c (float): Convergence factor.
        tiled (boolean): Whether to tile horizontally by 3 for x, y, z.

    Returns:
        array : mass matrix, either (m x 1) or (m x 3).

    """
    ks = E * A / l
    m = c * (abs(Ct).dot(ks + f / l))
    if tiled:
        return tile(m, (1, 3))
    return m


def stiffness_matrix():
    raise NotImplementedError


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
        sparse : If ``rtype`` is ``'csc', 'csr', 'coo'``.
        array : If ``rtype`` is ``'array'``.

    Analysis of the equilibrium matrix reveals some of the properties of the
    structural system, its size is (2ni x m) where ni is the number of free or
    internal nodes. It is calculated by

    .. math::

        \mathbf{E}
        =
        \left[
            \\begin{array}{c}
                \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{U} \\\[0.3em]
                \hline \\\[-0.7em]
                \mathbf{C}^{\mathrm{T}}_{\mathrm{i}}\mathbf{V}
            \end{array}
        \\right].


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
    return _return_matrix(E, rtype)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from operator import itemgetter

    import brg
    from brg.datastructures.network.network import Network

    from scipy.sparse.linalg import spsolve

    class Network(Network):
        def __init__(self, **kwargs):
            super(Network, self).__init__(**kwargs)
            self.dea.update({'q': 1.0})

    network = Network.from_obj(brg.get_data('lines.obj'))

    k_i = dict((key, index) for index, key in network.vertices_enum())
    i_k = dict(network.vertices_enum())
    xyz = [network.vertex_coordinates(key) for key in network]
    edges = [(k_i[u], k_i[v]) for u, v in network.edges_iter()]
    n = len(xyz)
    m = len(edges)
    fixed = [k_i[key] for key in network.leaves()]
    free = list(set(range(n)) - set(fixed))
    q = [float(1.0) for i in range(m)]

    ij_q = dict(((k_i[u], k_i[v]), attr['q']) for u, v, attr in network.edges_iter(True))
    ij_q.update(((k_i[v], k_i[u]), attr['q']) for u, v, attr in network.edges_iter(True))

    xyz = array(xyz)

    C = connectivity_matrix(edges, 'csr')
    Q = diags([q], [0])
    Ci = C[:, free]
    Cf = C[:, fixed]

    Cit = Ci.transpose()

    CitQCi = Cit.dot(Q).dot(Ci)
    CitQCf = Cit.dot(Q).dot(Cf)

    print(CitQCf.dot(xyz[fixed]))

    CtQC = [[0.0 for j in range(n)] for i in range(n)]

    for i in range(n):
        key = i_k[i]
        Q = 0
        for nbr in network.neighbours(key):
            j = k_i[nbr]
            q = ij_q[(i, j)]
            Q += q
            CtQC[i][j] = - q
        CtQC[i][i] = Q

    CitQCi = [[CtQC[i][j] for j in free] for i in free]
    CitQCf = [[CtQC[i][j] for j in fixed] for i in free]

    CtQC = array(CtQC)

    CitQCi = csr_matrix(array(CitQCi))
    CitQCf = csr_matrix(array(CitQCf))

    xyz[free] = spsolve(CitQCi, - CitQCf.dot(xyz[fixed]))

    for key, attr in network.vertices_iter(True):
        index = k_i[key]
        attr['x'] = xyz[index, 0]
        attr['y'] = xyz[index, 1]

    vlabel = dict((key, str(index)) for index, key in network.vertices_enum())
    elabel = dict(((u, v), str(index)) for index, u, v in network.edges_enum())

    network.plot(vlabel=vlabel, elabel=None)
