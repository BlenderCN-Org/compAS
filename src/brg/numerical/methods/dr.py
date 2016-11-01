import time

from numpy import array
from numpy import isnan
from numpy import isinf
from numpy import zeros
from numpy import ones
from numpy import sqrt
from numpy import sum

from scipy.linalg import norm

from scipy.sparse import diags

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


class Coeff():
    def __init__(self, c):
        self.c = c
        self.a = (1 - c * 0.5) / (1 + c * 0.5)
        self.b = 0.5 * (1 + self.a)


def rk1(a, v0, dt):
    raise NotImplementedError


def rk2(a, v0, dt):
    K = [
        [0.0, ],
        [0.5, 0.5, ],
    ]
    B = [0.0, 1.0]
    K0 = dt * a(K[0][0] * dt, v0)
    K1 = dt * a(K[1][0] * dt, v0 + K[1][1] * K0)
    dv = B[0] * K0 + B[1] * K1
    return dv


def rk3(a, v0, dt):
    raise NotImplementedError


def rk4(a, v0, dt):
    K = [
        [0.0, ],
        [0.5, 0.5, ],
        [0.5, 0.0, 0.5, ],
        [1.0, 0.0, 0.0, 1.0, ],
    ]
    B = [1. / 6., 1. / 3., 1. / 3., 1. / 6.]
    K0 = dt * a(K[0][0] * dt, v0)
    K1 = dt * a(K[1][0] * dt, v0 + K[1][1] * K0)
    K2 = dt * a(K[2][0] * dt, v0 + K[2][1] * K0 + K[2][2] * K1)
    K3 = dt * a(K[3][0] * dt, v0 + K[3][1] * K0 + K[3][2] * K1 + K[3][3] * K2)
    dv = B[0] * K0 + B[1] * K1 + B[2] * K2 + B[3] * K3
    return dv


# --------------------------------------------------------------------------
# adaptive, explicit RK schemes
# --------------------------------------------------------------------------
# def rk5():
#     K  = [
#         [0.0, ],
#         [0.25, 0.25, ],
#         [3. / 8., 3. / 32., 9. / 32., ],
#         [12. / 13., 1932. / 2197., -7200. / 2197., 7296. / 2197., ],
#         [1.0, 439. / 216., -8., 3680. / 513., -845. / 4104., ],
#         [0.5, -8. / 27., 2.0, -3544. / 2565., 1859. / 4104., -11. / 40., ]
#     ]
#     B5 = [16. / 135., 0.0, 6656. / 12825., 28561. / 56430., -9. / 50., 2. / 55.]
#     B4 = [25. / 216., 0.0, 1408. / 2565., 2197. / 4104., -1. / 5., 0.0]
#     K0 = dt * a(K[0][0] * dt, v0)
#     K1 = dt * a(K[1][0] * dt, v0 + K[1][1] * K0)
#     K2 = dt * a(K[2][0] * dt, v0 + K[2][1] * K0 + K[2][2] * K1)
#     K3 = dt * a(K[3][0] * dt, v0 + K[3][1] * K0 + K[3][2] * K1 + K[3][3] * K2)
#     K4 = dt * a(K[4][0] * dt, v0 + K[4][1] * K0 + K[4][2] * K1 + K[4][3] * K2 + K[4][4] * K3)
#     K5 = dt * a(K[5][0] * dt, v0 + K[5][1] * K0 + K[5][2] * K1 + K[5][3] * K2 + K[5][4] * K3 + K[5][5] * K4)
#     dv = B5[0] * K0 + B5[1] * K1 + B5[2] * K2 + B5[3] * K3 + B5[4] * K4 + B5[5] * K5
#     e  = (B5[0] - B4[0]) * K0 + (B5[1] - B4[1]) * K1 + (B5[2] - B4[2]) * K2 + (B5[3] - B4[3]) * K3 + (B5[4] - B4[4]) * K4 + (B5[5] - B4[5]) * K5
#     e  = sqrt(sum(e ** 2) / num_v)
#     return dv, e
# --------------------------------------------------------------------------
# implicit RK schemes
# --------------------------------------------------------------------------
# def rk2_(K1):
#     K = [
#         [0.0, 0.0, 0.0, ],
#         [1.0, 0.5, 0.5, ],
#     ]
#     B2 = [0.5, 0.5, ]
#     B1 = [1.0, 0.0, ]
#     K0 = dt * a(K[0][0] * dt, v0)
#     K1 = dt * a(K[1][0] * dt, v0 + K[1][1] * K0 + K[1][2] * K1)
#     dv = B2[0] * K0 + B2[1] * K1
#     return dv, K1


def dr(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius, ufunc=None, **kwargs):
    # --------------------------------------------------------------------------
    # configuration
    # --------------------------------------------------------------------------
    kmax  = kwargs.get('kmax', 10000)
    dt    = kwargs.get('dt', 1.0)
    tol1  = kwargs.get('tol1', 1e-3)
    tol2  = kwargs.get('tol2', 1e-6)
    coeff = Coeff(kwargs.get('c', 0.1))
    ca    = coeff.a 
    cb    = coeff.b 
    # --------------------------------------------------------------------------
    # attribute lists
    # --------------------------------------------------------------------------
    num_v = len(vertices)
    num_e = len(edges)
    free  = list(set(range(num_v)) - set(fixed))
    # --------------------------------------------------------------------------
    # attribute arrays
    # --------------------------------------------------------------------------
    xyz       = array(vertices, dtype=float).reshape((-1, 3))                   # m
    p         = array(loads, dtype=float).reshape((-1, 3))                      # kN
    qpre      = array(qpre, dtype=float).reshape((-1, 1))
    fpre      = array(fpre, dtype=float).reshape((-1, 1))                       # kN
    lpre      = array(lpre, dtype=float).reshape((-1, 1))                       # m
    linit     = array(linit, dtype=float).reshape((-1, 1))                      # m
    E         = array(E, dtype=float).reshape((-1, 1))                          # kN/mm2
    radius    = array(radius, dtype=float).reshape((-1, 1))                     # mm
    # --------------------------------------------------------------------------
    # sectional properties
    # --------------------------------------------------------------------------
    A  = 3.14159 * radius ** 2                                                  # mm2
    EA = E * A                                                                  # kN
    # --------------------------------------------------------------------------
    # create the connectivity matrices
    # after spline edges have been aligned
    # --------------------------------------------------------------------------
    C   = connectivity_matrix(edges, 'csr')
    Ct  = C.transpose()
    Ci  = C[:, free]
    Cit = Ci.transpose()
    Ct2 = Ct.copy()
    Ct2.data **= 2
    # --------------------------------------------------------------------------
    # if none of the initial lengths are set,
    # set the initial lengths to the current lengths
    # --------------------------------------------------------------------------
    if all(linit == 0):
        linit = normrow(C.dot(xyz))
    # --------------------------------------------------------------------------
    # initial values
    # --------------------------------------------------------------------------
    q = ones((num_e, 1), dtype=float)
    l = normrow(C.dot(xyz))
    f = q * l
    v = zeros((num_v, 3), dtype=float)
    r = zeros((num_v, 3), dtype=float)
    # --------------------------------------------------------------------------
    # acceleration
    # --------------------------------------------------------------------------
    def a(t, v):
        dx        = v * t
        xyz[free] = xyz0[free] + dx[free]
        r[free]   = p[free] - D.dot(xyz)
        return cb * r / mass
    # --------------------------------------------------------------------------
    # start iterating
    # --------------------------------------------------------------------------
    for i in xrange(kmax):
        q_fpre = fpre / l
        q_lpre = f / lpre
        q_EA   = EA * (l - linit) / (linit * l)
        q_lpre[isinf(q_lpre)] = 0
        q_lpre[isnan(q_lpre)] = 0
        q_EA[isinf(q_EA)]     = 0
        q_EA[isnan(q_EA)]     = 0
        q      = qpre + q_fpre + q_lpre + q_EA
        Q      = diags([q[:, 0]], [0])
        D      = Cit.dot(Q).dot(C)
        mass   = 0.5 * dt ** 2 * Ct2.dot(qpre + q_fpre + q_lpre + EA / linit)
        xyz0   = xyz.copy()
        # ----------------------------------------------------------------------
        # RK
        # ----------------------------------------------------------------------
        v0        = ca * v.copy()
        dv        = rk2(a, v0, dt)
        v         = v0 + dv
        dx        = v * dt
        xyz[free] = xyz0[free] + dx[free]
        # update
        uvw = C.dot(xyz)
        l   = normrow(uvw)
        f   = q * l
        r   = p - Ct.dot(Q).dot(uvw)
        # crits
        crit1 = norm(r[free])
        crit2 = norm(dx[free])
        # ufunc
        if ufunc:
            ufunc(i, crit1, crit2)
        # convergence
        if crit1 < tol1:
            break
        if crit2 < tol2:
            break
    return Result(xyz, q, f, l, r)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg
    from brg.datastructures import Network

    import matplotlib.pyplot as plt

    from brg.datastructures.network.drawing import draw_network


    Network.default_vertex_attributes.update({
        'is_fixed': False,
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
        'px': 0.0,
        'py': 0.0,
        'pz': 0.0,
        'rx': 0.0,
        'ry': 0.0,
        'rz': 0.0,
    })

    Network.default_edge_attributes.update({
        'qpre': 1.0,
        'fpre': 0.0,
        'lpre': 0.0,
        'linit': 0.0,
        'E': 0.0,
        'radius': 0.0,
    })

    network = Network.from_obj(brg.get_data('lines.obj'))

    for key, attr in network.vertices_iter(True):
        attr['is_fixed'] = network.degree(key) == 1

    count = 1
    for u, v, attr in network.edges_iter(True):
        attr['qpre'] = count
        count += 1

    k2i = dict((key, index) for index, key in network.vertices_enum())

    vertices = [network.vertex_coordinates(key) for key in network.vertex]
    edges    = [(k2i[u], k2i[v]) for u, v in network.edges_iter()]
    fixed    = [k2i[key] for key, attr in network.vertices_iter(True) if attr['is_fixed']]
    loads    = [(attr['px'], attr['py'], attr['pz']) for key, attr in network.vertices_iter(True)]
    qpre     = [attr['qpre'] for u, v, attr in network.edges_iter(True)]
    fpre     = [attr['fpre'] for u, v, attr in network.edges_iter(True)]
    lpre     = [attr['lpre'] for u, v, attr in network.edges_iter(True)]
    linit    = [attr['linit'] for u, v, attr in network.edges_iter(True)]
    E        = [attr['E'] for u, v, attr in network.edges_iter(True)]
    radius   = [attr['radius'] for u, v, attr in network.edges_iter(True)]

    xdata  = []
    ydata1 = []
    ydata2 = []

    plt.show()

    axes   = plt.gca()
    line1, = axes.plot(xdata, ydata1, 'r-')
    line2, = axes.plot(xdata, ydata2, 'b-')
    axes.set_ylim(-10, 60)
    axes.set_xlim(0, 100)

    def plot_iterations(i, crit1, crit2):
        print i, crit1, crit2
        xdata.append(i)
        ydata1.append(crit1)
        ydata2.append(crit2)
        line1.set_xdata(xdata)
        line1.set_ydata(ydata1)
        line2.set_xdata(xdata)
        line2.set_ydata(ydata2)
        plt.draw()
        plt.pause(1e-17)

    res = dr(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius, ufunc=plot_iterations)

    plt.show()

    for key, attr in network.vertices_iter(True):
        index = k2i[key]
        attr['x'] = res.xyz[index][0]
        attr['y'] = res.xyz[index][1]
        attr['z'] = res.xyz[index][2]

    draw_network(network)
