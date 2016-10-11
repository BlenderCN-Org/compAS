# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

from numpy import tile
from numpy import divide
from numpy import hstack
from numpy import arange

from scipy import cross

from scipy.sparse import coo_matrix

from linalg import normrow
from linalg import normalizerow
from linalg import rot90


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 14, 2014'


__all__ = [
    'div',
    'grad',
    'curl',
]


def grad(V, F, rtype='array'):
    """Construct the gradient operator of a triangle mesh.

    The gradient operator is fully determined by the connectivity of the mesh
    and the coordinate difference vectors associated with the edges

    Parameters:
        V (array): The vertex coordinates of the mesh.
        F (array): The face vertex indices.
        rtype (str): Return format. Defaults to `array`.

    Returns:
        Sparse SciPy matrix, if ``rtype`` is one of ``None, 'csc', 'csr', 'coo'``
        NumPy array, if ``rtype`` is ``'array'``.
    """
    v = V.shape[0]
    f = F.shape[0]
    # index of first vertex of each face
    f0 = F[:, 0]
    # index of second vertex of each face
    f1 = F[:, 1]
    # index of last vertex of each face
    f2 = F[:, 2]
    # vector from vertex 0 to vertex 1, for each face
    v01 = V[f1, :] - V[f0, :]
    # vector from vertex 1 to vertex 2, for each face
    v12 = V[f2, :] - V[f1, :]
    # vector from vertex 2 to vertex 0, for each face
    v20 = V[f0, :] - V[f2, :]
    # the normal vector to each face
    n = cross(v12, v20)
    # the length of the normal vector is equal to twice the area of the face
    A2 = normrow(n)
    A2 = tile(A2, (1, 3))
    # unit normals for each face
    u = normalizerow(n)
    # vector perpendicular to v01, normalized by A2
    v01_ = divide(rot90(v01, u), A2)
    # vector perpendicular to v20, normalized by A2
    v20_ = divide(rot90(v20, u), A2)
    # nonzero rows
    i = hstack((
        0 * f + tile(arange(f), (1, 4)),
        1 * f + tile(arange(f), (1, 4)),
        2 * f + tile(arange(f), (1, 4))
    )).flatten()
    # nonzero columns
    j = tile(hstack((f1, f0, f2, f0)), (1, 3)).flatten()
    data = hstack((
        hstack((v20_[:, 0], - v20_[:, 0], v01_[:, 0], - v01_[:, 0])),
        hstack((v20_[:, 1], - v20_[:, 1], v01_[:, 1], - v01_[:, 1])),
        hstack((v20_[:, 2], - v20_[:, 2], v01_[:, 2], - v01_[:, 2])),
    )).flatten()
    G = coo_matrix((data, (i, j)), shape=(3 * f, v))
    if rtype == 'array':
        return G.toarray()
    elif rtype == 'csr':
        return G.tocsr()
    elif rtype == 'csc':
        return G.tocsc()
    elif rtype == 'coo':
        return G
    else:
        return G


def div():
    pass


def curl():
    pass
