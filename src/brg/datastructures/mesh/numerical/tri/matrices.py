"""This module defines mesh matrices that are specific for triangle meshes."""

from brg.geometry import dot
from brg.geometry import length
from brg.geometry import cross

from numpy import ones

from scipy.sparse import coo_matrix
from scipy.sparse import spdiags


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


def cotangent(u, v, w, key_xyz):
    u = key_xyz[u]
    v = key_xyz[v]
    w = key_xyz[w]
    wu = [u[i] - w[i] for i in range(3)]
    wv = [v[i] - w[i] for i in range(3)]
    return dot(wu, wv) / length(cross(wu, wv))


def cotangent_laplacian_matrix(mesh):
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
        The other entries are ...

    >>> ...

    """
    # minus sum of the adjacent weights on the diagonal
    # cotangent weights on the neighbours
    key_index = dict((key, index) for index, key in mesh.vertices_enum())
    key_xyz = dict((key, mesh.vertex_coordinates(key)) for key in mesh)
    n = len(mesh)
    data = []
    rows = []
    cols = []
    for u, v in mesh.edges_iter():
        uv = mesh.face[mesh.halfedge[u][v]][v]
        vu = mesh.face[mesh.halfedge[v][u]][u]
        a = cotangent(u, v, uv, key_xyz)
        b = cotangent(v, u, vu, key_xyz)
        i = key_index[u]
        j = key_index[v]
        data.append(0.5 * a)
        rows.append(i)
        cols.append(j)
        data.append(0.5 * b)
        rows.append(j)
        cols.append(i)
    L = coo_matrix((data, (rows, cols)), shape=(n, n))
    L = L.tocsr()
    L = L - spdiags(L * ones(n), 0, n, n)
    L = L.tocsr()
    return L


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
