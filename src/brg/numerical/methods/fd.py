from numpy import array

from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

from brg.numerical.matrices import connectivity_matrix
from brg.numerical.linalg import normrow

from result import Result


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Jul 8, 2015'


def fd(vertices, edges, fixed, q, loads):
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
