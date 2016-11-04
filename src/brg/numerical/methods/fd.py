"""brg.numerical.methods.fd : The force-density method."""

from numpy import array

from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

from brg.numerical.matrices import connectivity_matrix
from brg.numerical.linalg import normrow

from result import Result


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 20, 2016'


def fd(vertices, edges, fixed, q, loads):
    """Force-density numerical method.

    Parameters:
        vertices (list): Vertices' x, y and z co-ordinates.
        edges (list): Connectivity information of edges
        fixed (list): Indices of vertices fixed from spatial translations.
        q (list): Force densities of edges.
        loads (list): Point loads (px, py, pz) applied to vertices.

    Returns:
        obj: Result class of output data.
    """
    num_v     = len(vertices)
    free      = list(set(range(num_v)) - set(fixed))
    xyz       = array(vertices, dtype=float).reshape((-1, 3))
    q         = array(q, dtype=float).reshape((-1, 1))
    p         = array(loads, dtype=float).reshape((-1, 3))
    C         = connectivity_matrix(edges, 'csr')
    Ci        = C[:, free]
    Cf        = C[:, fixed]
    Ct        = C.transpose()
    Cit       = Ci.transpose()
    Q         = diags([q.flatten()], [0])
    A         = Cit.dot(Q).dot(Ci)
    b         = p[free] - Cit.dot(Q).dot(Cf).dot(xyz[fixed])
    xyz[free] = spsolve(A, b)
    l         = normrow(C.dot(xyz))
    f         = q * l
    r         = p - Ct.dot(Q).dot(C).dot(xyz)
    return Result(xyz, q, f, l, r)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
