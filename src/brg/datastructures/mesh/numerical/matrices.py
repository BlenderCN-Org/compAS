from brg.geometry import dot
from brg.geometry import length_vector
from brg.geometry import cross

from brg.numerical.matrices import adjacency_matrix
from brg.numerical.matrices import connectivity_matrix
from brg.numerical.matrices import laplacian_matrix

from numpy import ones

from scipy.sparse import coo_matrix
from scipy.sparse import spdiags


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_adjacency_matrix',
    'mesh_connectivity_matrix',
    'mesh_laplacian_matrix',
    'trimesh_edge_cotangent',
    'trimesh_edge_cotangents',
    'trimesh_cotangent_laplacian_matrix',
    'trimesh_positive_cotangent_laplacian_matrix',
]


def mesh_adjacency_matrix(mesh, rtype='csr'):
    k_i   = dict((key, index) for index, key in mesh.vertices_enum())
    adjacency = [[k_i[nbr] for nbr in mesh.vertex_neighbours(key)] for key in mesh]
    return adjacency_matrix(adjacency, rtype=rtype)


def mesh_connectivity_matrix(mesh, rtype='csr'):
    k_i   = dict((key, index) for index, key in mesh.vertices_enum())
    edges = [(k_i[u], k_i[v]) for u, v in mesh.edges_iter()]
    return connectivity_matrix(edges, rtype=rtype)


def mesh_laplacian_matrix(mesh, rtype='csr'):
    k_i   = dict((key, index) for index, key in mesh.vertices_enum())
    edges = [(k_i[u], k_i[v]) for u, v in mesh.edges_iter()]
    return laplacian_matrix(edges, rtype=rtype)


def trimesh_edge_cotangent(mesh, u, v):
    fkey = mesh.halfedge[u][v]
    cotangent = 0.0
    if fkey is not None:
        w = mesh.face[fkey][v]  # self.vertex_descendent(v, fkey)
        wu = mesh.edge_vector(w, u)
        wv = mesh.edge_vector(w, v)
        cotangent = dot(wu, wv) / length_vector(cross(wu, wv))
    return cotangent


def trimesh_edge_cotangents(mesh, u, v):
    a = trimesh_edge_cotangent(u, v)
    b = trimesh_edge_cotangent(v, u)
    return a, b


def trimesh_cotangent_laplacian_matrix(mesh):
    """Construct the Laplacian of a triangular mesh with cotangent weights.

    Parameters:
        mesh (brg.datastructures.mesh.tri.TriMesh) :
            The triangular mesh.

    Returns:
        array-like :
            The Laplacian matrix with cotangent weights.
            ...

    Note:
        The matrix is constructed such that the diagonal contains the sum of the
        weights of the adjacent vertices, multiplied by `-1`.
        The entries of the matrix are thus

        .. math::

            \mathbf{L}_{ij} =
                \begin{cases}
                    - \sum_{(i, k) \in \mathbf{E}_{i}} w_{ik} & if i = j \\
                    w_{ij} & if (i, j) \in \mathbf{E} \\
                    0 & otherwise
                \end{cases}

    >>> ...

    """
    # minus sum of the adjacent weights on the diagonal
    # cotangent weights on the neighbours
    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    n = len(mesh)
    data = []
    rows = []
    cols = []
    # compute the weight of each halfedge
    # as the cotangent of the angle at the opposite vertex
    for u, v in mesh.edges_iter():
        a, b = mesh.edge_cotangents(u, v)
        i = key_index[u]
        j = key_index[v]
        data.append(0.5 * a)  # not sure why multiplication with 0.5 is necessary
        rows.append(i)
        cols.append(j)
        data.append(0.5 * b)  # not sure why multiplication with 0.5 is necessary
        rows.append(j)
        cols.append(i)
    L = coo_matrix((data, (rows, cols)), shape=(n, n))
    L = L.tocsr()
    # subtract from the diagonal the sum of the weights of the neighbours of the
    # vertices corresponding to the diagonal entries.
    L = L - spdiags(L * ones(n), 0, n, n)
    L = L.tocsr()
    return L


def trimesh_positive_cotangent_laplacian_matrix(mesh):
    raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg
    from brg.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    # print mesh_adjacency_matrix(mesh, 'list')
    # print mesh_connectivity_matrix(mesh, 'list')
    print mesh_laplacian_matrix(mesh, 'list')
