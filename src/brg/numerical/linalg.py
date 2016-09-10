import sys

from subprocess import Popen

from numpy import array
from numpy import seterr
from numpy import sum
from numpy import nan_to_num
from numpy import where
from numpy import nonzero
from numpy import argmax
from numpy import asarray
from numpy import zeros
from numpy import atleast_2d
from numpy import float32

from scipy import cross

from numpy.linalg import cond

from scipy.linalg import solve
from scipy.linalg import cho_solve
from scipy.linalg import cho_factor
from scipy.linalg import lstsq
from scipy.linalg import svd
from scipy.linalg import lu
from scipy.linalg import qr

from scipy.sparse.linalg import factorized
from scipy.sparse.linalg import spsolve

from scipy.io import savemat
from scipy.io import loadmat


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 14, 2014'


old_settings = seterr(all='ignore')


# ------------------------------------------------------------------------------
# Fundamentals
# ------------------------------------------------------------------------------


def nullspace(A, tol=0.001):
    A = atleast_2d(asarray(A, dtype=float32))
    u, s, vh = svd(A, compute_uv=True)
    tol = s[0] * tol
    r = (s >= tol).sum()
    null = vh[r:].conj().T
    return null


def rank(A, tol=0.001):
    A = atleast_2d(asarray(A, dtype=float32))
    s = svd(A, compute_uv=False)
    tol = s[0] * tol
    r = (s >= tol).sum()
    return r


def dof(A, tol=0.001, condition=False):
    A = atleast_2d(asarray(A, dtype=float32))
    r = rank(A, tol=tol)
    k = A.shape[1] - r
    m = A.shape[0] - r
    if condition:
        c = cond(A)
        return k, m, c
    return k, m


def pivots(U):
    U = atleast_2d(asarray(U, dtype=float32))
    pivots = []
    for row in U:
        cols = nonzero(row)[0]
        if len(cols):
            pivots.append(cols[0])
    return pivots


def nonpivots(U):
    U = atleast_2d(asarray(U, dtype=float32))
    cols = pivots(U)
    return list(set(range(U.shape[1])) - set(cols))


def rref(A, algo='qr', tol=None, **kwargs):
    A = atleast_2d(asarray(A, dtype=float32))
    if algo == 'qr':
        _, U = qr(A)
        lead_pos = 0
        num_rows, num_cols = U.shape
        for r in range(num_rows):
            if lead_pos >= num_cols:
                return
            i = r
            # find a nonzero lead in column lead_pos
            while U[i][lead_pos] == 0:
                i += 1
                if i == num_rows:
                    i = r
                    lead_pos += 1
                    if lead_pos == num_cols:
                        return
            # swap the row with the nonzero lead with the current row
            U[[i, r]] = U[[r, i]]
            # "normalize" the values of the row
            lead_val = U[r][lead_pos]
            U[r] = U[r] / lead_val
            # make sure all other column values are zero
            for i in range(num_rows):
                if i != r:
                    lead_val = U[i][lead_pos]
                    U[i] = U[i] - lead_val * U[r]
            # go to the next column
            lead_pos += 1
        return U
    if algo == 'sympy':
        # return asarray?
        import sympy
        return sympy.Matrix(A).rref()[0].tolist()
    if algo == 'matlab':
        import platform
        ifile = kwargs['ifile']
        ofile = kwargs['ofile']
        idict = {'A': A}
        savemat(ifile, idict)
        matlab  = ['matlab']
        if platform.system() == 'Windows':
            options = ['-nosplash', '-wait', '-r']
        else:
            options = ['-nosplash', '-r']
        command = ["load('{0}');[R, jb]=rref(A);save('{1}');exit;".format(ifile, ofile)]
        p = Popen(matlab + options + command)
        stdout, stderr = p.communicate()
        odict  = loadmat(ofile)
        return odict['R']


# if algo == 'lu':
#     _, _, u = lu(A)
#     if tol is None:
#         eps = sys.float_info.epsilon
#         tol = max(u.shape) * eps * max(sum(abs(u), axis=1))
#     pivots = {}
#     # iterate over the rows to find the non-pivoting elements
#     # a pivoting element in an upper triangular matrix is the first nonzero
#     # element in a row, if all elements below are also zero
#     m, n = u.shape
#     for i in range(m):
#         row = u[i]
#         # find the first element in the row of which the abs value is above
#         # the threshold
#         cols = nonzero(abs(row) > tol)[0]
#         if len(cols) == 0:
#             # in this row, all elements are zero
#             col = None
#         else:
#             # in this row, the first nonzero element is at cols[0]
#             # this is not necessarily a pivot,
#             # since this column might have been identified in a previous
#             # row as the pivot
#             piv = i
#             col = cols[0]
#             # check if the rows below for the highest value at this column
#             # swap rows to put the higher row on top
#             j = argmax(abs(u[i : m, col]))
#             if j > 0:
#                 print col
#                 print u[i, col]
#                 print u[i + j, col]
#                 print
#             if j > 0:
#                 u[i], u[i + j] = u[i + j], u[i]
#                 row = u[i]
#         # subtract multiples from previously found pivoting rows
#         # until the actual pivot is found
#         # or until the entire row is zero
#         count = 10000
#         while True:
#             if count == 0:
#                 # make sure the loop is not infinite
#                 break
#             count -= 1
#             if col not in pivots:
#                 # if this pivot was not yet found
#                 # update the row in the upper triangular matrix
#                 # this is not a row 'switch'
#                 u[i] = row
#                 break
#             # if there is a row that already had a pivot at this column
#             # update the row by subtracting a multiple of the previously
#             # found row such that the pivot becomes zero
#             piv  = pivots[col]
#             row  = row - (row[col] / u[piv, col]) * u[piv]
#             cols = nonzero(abs(row) > tol)[0]
#             if len(cols) == 0:
#                 # the entire row has become zero
#                 col = None
#             else:
#                 col = cols[0]
#         if col is not None:
#             pivots[col] = piv
#     nonpivots = list(set(range(n)) - set(pivots))


# ------------------------------------------------------------------------------
# Factorisation
# ------------------------------------------------------------------------------


class Memoized:
    """"""
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        key = args[-1]
        if key in self.memo:
            return self.memo[key]
        self.memo[key] = res = self.f(args[0])
        return res


def _chofactor(A):
    return cho_factor(A)


def _lufactorized(A):
    return factorized(A)


chofactor = Memoized(_chofactor)
lufactorized = Memoized(_lufactorized)


# ------------------------------------------------------------------------------
# Geometry
# ------------------------------------------------------------------------------


def normrow(A):
    """Calculate the norm (i.e. the length) of each row vector of A."""
    return (sum(A ** 2, axis=1) ** 0.5).reshape((-1, 1))


def normalizerow(A, do_nan_to_num=True):
    """Normalize the rows of A.

    Divide each element of a row by the norm of the row vector.

    Note:
        Tiling is not necessary, because of NumPy's broadcasting behaviour.

    Parameters:
        A (array): A NumPy array.
        nan_to_num (bool): Convert NaNs to numbers if this flag is set to
            ``True``. Defaults to ``True``.

    Returns:
        A NumPy array of the same size as the input array, but with normalized rows.
    """
    if do_nan_to_num:
        return nan_to_num(A / normrow(A))
    else:
        return A / normrow(A)


def rot90(vectors, axes):
    """Rotate an array of vectors over 90 degrees around an array of axes.

    Compute the cross product of each vector and its corresponding axis.
    Rescale the normal vectors to match the length of the original vectors.

    Parameters:
        vectors (array): An array of vectors.
        axes (array): An array of axes.

    Returns:
        ...
    """
    return normalizerow(cross(axes, vectors)) * normrow(vectors)


# ------------------------------------------------------------------------------
# Solving
# ------------------------------------------------------------------------------


def solve_with_known(A, b, x, known):
    """Solve a system of linear equations with part of the solution known.

    Parameters:
        A (array): The coefficient matrix.
        b (array): RHS
        x (array): The unknowns.
        known (list): The indices of the known elements of ``x``.

    Returns:
        A NumPy array containing the solution.
    """
    eps = 1 / sys.float_info.epsilon
    unknown = list(set(range(x.shape[0])) - set(known))
    A11 = A[unknown, :][:, unknown]
    A12 = A[unknown, :][:, known]
    b = b[unknown] - A12.dot(x[known])
    if cond(A11) < eps:
        Y = cho_solve(cho_factor(A11), b)
        x[unknown] = Y
        return x
    Y = lstsq(A11, b)
    x[unknown] = Y[0]
    return x


def spsolve_with_known(A, B, X, known):
    """"""
    unknown = list(set(range(X.shape[0])) - set(known))
    A11 = A[unknown, :][:, unknown]
    A12 = A[unknown, :][:, known]
    b = B[unknown] - A12.dot(X[known])
    X[unknown] = spsolve(A11, b)
    return X


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import numpy as np

    np.set_printoptions(precision=3, threshold=10000, linewidth=1000)

    E = array([[2, 3, 5], [-4, 2, 3]], dtype=float32)

    null = nullspace(E)

    assert np.allclose(zeros((E.shape[0], 1)), E.dot(null), atol=1e-6), 'E.dot(null) not aproximately zero'

    m, n = E.shape
    s, t = null.shape

    print m, n
    print s, t

    assert n == s, 'num_cols of E should be equal to num_rows of null(E)'

    print rank(E)
    print dof(E)

    print len(pivots(rref(E)))
    print len(nonpivots(rref(E)))

    # ifile = './data/ifile.mat'
    # ofile = './data/ofile.mat'

    # with open(ifile, 'wb+') as fp: pass
    # with open(ofile, 'wb+') as fp: pass

    # print nonpivots(rref(E, algo='qr'))
    # print nonpivots(rref(E, algo='sympy'))
    # print nonpivots(rref(E, algo='matlab', ifile=ifile, ofile=ofile))
