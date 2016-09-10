# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

from numpy import array
from numpy import asarray
from numpy import float32

from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import diags
from scipy.sparse import vstack as svstack


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 14, 2014'


def adjacency_matrix():
    pass


def degree_matrix():
    pass


def connectivity_matrix(edges, rtype='array'):
    """"""
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
    else:
        return C


def laplacian_matrix(edges, rtype='array'):
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


def equilibrium_matrix(C, xyz, free, rtype='array'):
    """Construct the equilibrium matrix of a structural system.

    Analysis of the equilibrium matrix reveals some of the properties of the
    structural system, as described in ...

    Note:
        The matrix of vertex coordinates is vectorized to speed up the
        calculations.

    Parameters:
        C (sparse matrix): [m x n] SciPy sparse connectivity matrix of the
            structural system.
        xyz (array): [n x 3] NumPy array of vertex coordinates.
        free (list): The list of indices of the free vertices.

    Returns:
        Sparse SciPy matrix, if ``f`` one of ``None, 'csc', 'csr', 'coo'``.
        NumPy array, if ``f`` is ``'array'``.
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

    pass
