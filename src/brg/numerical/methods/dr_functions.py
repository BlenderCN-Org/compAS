"""brg.numerical.methods.dr_functions : Functions for the dynamic relaxation method."""

from brg.numerical.geometry import lengths
from brg.numerical.matrices import connectivity_matrix
from brg.numerical.matrices import mass_matrix
from brg.numerical.linalg import normrow

from numpy import abs
from numpy import array
from numpy import max
from numpy import mean
from numpy import newaxis
from numpy import ones
from numpy import sum
from numpy import tile
from numpy import zeros

from time import time


__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__author__     = ['Andrew Liew <liew@arch.ethz.ch>']


def beam_indices(beams):
    inds = []
    indi = []
    indf = []
    for beam in beams:
        inds.extend([int(x) for x in beam[0:-2]])
        indi.extend([int(x) for x in beam[1:-1]])
        indf.extend([int(x) for x in beam[2:]])
    return inds, indi, indf


def residual(f, l, P, S, uvw, Ct, BC, Pn, f0, rtype='force'):
    R = (P - S - Ct.dot(uvw * tile(f / l, (1, 3)))) * BC
    Rn = normrow(R)
    if rtype == 'force':
        res = mean(Rn / Pn)
    elif rtype == 'prestress':
        res = mean(Rn / mean(abs(f0)))
    elif 'magnitude' in rtype:
        res = max(Rn / float(rtype.split('_')[1]))
    return R, 100 * res


def run(X, edges, BC_, P_, E_, A_, tol, steps, s0_=None, ct='ct',
        rtype='force', beams=None):
    m = len(edges)
    n = len(X)

    # Beams
    if beams:
        inds, indi, indf = beam_indices(beams)

    # Indexed arrays
    s0 = zeros((m, 1))
    if s0_:
        for i in s0_:
            s0[i[0]] = i[1]
    E = zeros((m, 1))
    for i in E_:
        E[i[0]] = i[1]
    A = zeros((m, 1))
    for i in A_:
        A[i[0]] = i[1]
    P = zeros((n, 3))
    for i in P_:
        P[i[0], :] = i[1]
    BC = ones((n, 3))
    for i in BC_:
        BC[i[0], :] = i[1]

    # Arrays
    C = connectivity_matrix(edges, 'csr')
    Ct = C.transpose()
    X = array(X)
    V = zeros(X.shape)
    uvw0, l0 = lengths(C, X)
    Pn = normrow(P)
    S = zeros(P.shape)
    f0 = s0 * A
    M = mass_matrix(Ct, E, A, l0, f0, c=1)
    ks = E * A / l0
    ts, Uo = 0, 0
    res = 1000 * tol
    tic = time()

    # Main loop
    while (ts <= steps) and (res > tol):
        uvw, l = lengths(C, X)
        f = f0 + ks * (l - l0)
        if ct == 't':
            f *= f > 0
        elif ct == 'c':
            f *= f < 0
        R, res = residual(f, l, P, S, uvw, Ct, BC, Pn, f0, rtype=rtype)
        V += R / M
        Un = sum(0.5 * M * V * V)
        if Un < Uo:
            V *= 0
        Uo = Un
        X += V
        ts += 1

    # Summary
    print('-' * 50)
    print('Iterations: ' + str(ts - 1))
    print('Residual: ' + '{0:.3g}'.format(res))
    print('Time: ' + '{0:.3g}'.format(time() - tic) + 's')
    print('-' * 50)

    # print(indf)
    return X
