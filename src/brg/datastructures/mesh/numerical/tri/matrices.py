"""This module defines mesh matrices that are specific for triangle meshes."""

from numpy import ones

from scipy.sparse import coo_matrix
from scipy.sparse import spdiags


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


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


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg
    from brg.datastructures.mesh.mesh import Mesh
    from brg.datastructures.mesh.algorithms.triangulation import delaunay_from_mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    delaunay = delaunay_from_mesh(mesh)

    L = cotangent_laplacian_matrix(delaunay)

    print L

    delaunay.draw(show_vertices=True)
