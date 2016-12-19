"""brg.numerical.methods.dr_functions : Functions for the dynamic relaxation method."""

from brg.numerical.geometry import lengths
from brg.numerical.matrices import connectivity_matrix
from brg.numerical.matrices import mass_matrix
from brg.numerical.linalg import normrow

from numpy import abs
from numpy import array
from numpy import arccos
from numpy import cross
from numpy import isnan
from numpy import max
from numpy import mean
from numpy import newaxis
from numpy import ones
from numpy import sin
from numpy import sum
from numpy import tile
from numpy import zeros

from time import time


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Oct 17, 2016'


def beam_indices(beams):
    inds = []
    indi = []
    indf = []
    EIx = []
    EIy = []
    for c in range(len(beams['nodes'])):
        beam = beams['nodes'][c]
        inds.extend([int(x) for x in beam[0:-2]])
        indi.extend([int(x) for x in beam[1:-1]])
        indf.extend([int(x) for x in beam[2:]])
        EIx.extend(beams['EIx'][c][1:-1])
        EIy.extend(beams['EIy'][c][1:-1])
    EIx = array(EIx)[:, newaxis]
    EIy = array(EIy)[:, newaxis]
    return inds, indi, indf, EIx, EIy


def beam_shear(S, X, inds, indi, indf, EIx, EIy):
    S *= 0
    Qs = X[inds, :]
    Qi = X[indi, :]
    Qf = X[indf, :]
    Qa = Qi - Qs
    Qb = Qf - Qi
    Qc = Qf - Qs
    Qn = cross(Qa, Qb)
    Qnn = normrow(Qn)
    La = normrow(Qa)
    Lb = normrow(Qb)
    Lc = normrow(Qc)
    Ln = normrow(Qn)
    a = arccos((La**2 + Lb**2 - Lc**2) / (2 * La * Lb))
    k = 2 * sin(a) / Lc
    mu = -0.5 * Qs + 0.5 * Qf
    mun = normrow(mu)
    ex = Qn / tile(Qnn, (1, 3))  # Temp simplification
    ez = mu / tile(mun, (1, 3))
    ey = cross(ez, ex)
    K = tile(k / Ln, (1, 3)) * Qn
    Kx = tile(sum(K * ex, 1)[:, newaxis], (1, 3)) * ex
    Ky = tile(sum(K * ey, 1)[:, newaxis], (1, 3)) * ey
    Mc = EIx * Kx + EIy * Ky
    cma = cross(Mc, Qa)
    cmb = cross(Mc, Qb)
    ua = cma / tile(normrow(cma), (1, 3))
    ub = cmb / tile(normrow(cmb), (1, 3))
    c1 = cross(Qa, ua)
    c2 = cross(Qb, ub)
    Lc1 = normrow(c1)
    Lc2 = normrow(c2)
    M = sum(Mc**2, 1)[:, newaxis]
    Sa = ua * tile(M * Lc1 / (La * sum(Mc * c1, 1)[:, newaxis]), (1, 3))
    Sb = ub * tile(M * Lc2 / (Lb * sum(Mc * c2, 1)[:, newaxis]), (1, 3))
    Sa[isnan(Sa)] = 0
    Sb[isnan(Sb)] = 0
    S[inds, :] += Sa
    S[indi, :] += -Sa - Sb
    S[indf, :] += Sb
    # print(Sa)
    # Add node junction duplication for when elements cross each other
    # # mu[0, :] = -1.25*x[0, :] + 1.5*x[1, :] - 0.25*x[2, :]
    # # mu[-1, :] = 0.25*x[-3, :] - 1.5*x[-2, :] + 1.25*x[-1, :]
    return S


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
        rtype='force', beams=None, factor=1):
    m = len(edges)
    n = len(X)

    # Beams
    if beams:
        inds, indi, indf, EIx, EIy = beam_indices(beams)

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
    M = mass_matrix(Ct, E, A, l0, f0, c=factor)
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
        if beams:
            S = beam_shear(S, X, inds, indi, indf, EIx, EIy)
        R, res = residual(f, l, P, S, uvw, Ct, BC, Pn, f0, rtype=rtype)
        V += R / M
        Un = sum(0.5 * M * V * V)
        if Un < Uo:
            V *= 0
        Uo = Un
        X += V
        if ts % 100 == 0:
            print('Step: ' + str(ts) + '   ' + 'Residual: ' +
                  '{0:.3g}'.format(res))
        ts += 1

    # Summary
    print('-' * 50)
    print('Iterations: ' + str(ts - 1))
    print('Residual: ' + '{0:.3g}'.format(res))
    print('Time: ' + '{0:.3g}'.format(time() - tic) + 's')
    print('-' * 50)

    return X
