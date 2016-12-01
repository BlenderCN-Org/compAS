"""brg.numerical.solvers.differential_evolution : Differential evolution."""

from numpy import array
from numpy import argmin
from numpy import min
from numpy import newaxis
from numpy import tile
from numpy import where
from numpy import zeros
from numpy.random import rand

from random import sample

from functools import partial

import matplotlib.pyplot as plt

import multiprocessing


__author__     = ['Andrew Liew <liew@arch.ethz.ch>', ]
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.10'
__date__       = '10.10.2016'


def de_solver(fn, bounds, population, iterations, results=None, threads=0, args=()):
    """ Call the differential evolution solver.

    Note:
        fn returns vectorised output for input (k, population) if threads=0.

    Parameters:
        fn (obj): The function to evaluate and minimise.
        bounds (list): List of tuples defining bounds for each DoF.
        population (int): Number of agents in the population.
        iterations (int): Number of cross-over cycles or steps to perform.
        results (boolean): Store results or not.
        threads (int): Number of threads/processes for multiprocessing.
        arg (seq): Sequence of optional arguments to pass to fn.

    Returns:
        float: Optimal value of objective function.
        array: Values that give optimum (minimised) function.
        array: Data for plotting.

    Examples:
        >>> def fn(u, *args):
        >>>     # Booth's function, fopt=0, xopt=(1, 3)
        >>>     x = u[0, :]
        >>>     y = u[1, :]
        >>>     z = (x + 2*y - 7)**2 + (2*x + y - 5)**2
        >>>     return z
        >>> bounds = [(-10, 10) for i in range(2)]
        >>> fopt, xopt = solver(fn, bounds, population=100, iterations=150)
        Iteration: 0 fopt: 9.29475634582
        Iteration: 1 fopt: 0.714845258545
        Iteration: 2 fopt: 0.714845258545
        ...
        Iteration: 148 fopt: 4.22441611201e-22
        Iteration: 149 fopt: 4.22441611201e-22
        Iteration: 150 fopt: 5.18467217924e-23
        >>> print(xopt)
        array([ 1.,  3.])
    """
    F = 0.8
    CR = 0.9
    k = len(bounds)
    b_ran = array([bound[1] - bound[0] for bound in bounds])[:, newaxis]
    b_min = array([bound[0] for bound in bounds])[:, newaxis]
    agents = (rand(k, population) * tile(b_ran, (1, population)) +
              tile(b_min, (1, population)))
    candidates = [list(range(population)) for i in range(population)]
    for i in range(population):
        del candidates[i][i]
    candidates = array(candidates)
    ts = 0
    if threads:
        t = range(population)
        pool = multiprocessing.Pool(processes=threads)
        func = partial(funct, agents, args)
        fun = array(pool.map(func, t))
        pool.close()
        pool.join()
    else:
        fun = fn(agents, args)
    fopt = min(fun)
    print('Iteration: ' + str(ts) + ' fopt: ' + str(fopt))
    ac = zeros((k, population))
    bc = zeros((k, population))
    cc = zeros((k, population))
    data = zeros((iterations, population))
    while ts < iterations:
        if results:
            data[ts, :] = fun
        ind = rand(k, population) < CR
        for i in range(population):
            inds = candidates[i, sample(range(population - 1), 3)]
            ac[:, i] = agents[:, inds[0]]
            bc[:, i] = agents[:, inds[1]]
            cc[:, i] = agents[:, inds[2]]
        agents_ = ind * (ac + F * (bc - cc)) + ~ind * agents
        if threads:
            t = range(population)
            pool = multiprocessing.Pool(processes=threads)
            func = partial(funct, agents_, args)
            fun_ = array(pool.map(func, t))
            pool.close()
            pool.join()
        else:
            fun_ = fn(agents_, args)
        log = where((fun - fun_) > 0)[0]
        agents[:, log] = agents_[:, log]
        fun[log] = fun_[log]
        fopt = min(fun)
        xopt = agents[:, argmin(fun)]
        ts += 1
        ac *= 0
        bc *= 0
        cc *= 0
        print('Iteration: ' + str(ts) + ' fopt: ' + str(fopt))
    if results:
        return fopt, xopt, data
    else:
        return fopt, xopt


def plot(data, ms, path):
    """ Plot the differential evolution results.

    Parameters:
        data (array): Data array (iterations x population).
        ms (float): Markersize of points.
        path (str): Path to save figure.

    Returns:
        None
    """
    n = data.shape[0]
    m = data.shape[1]
    nt = tile(array(list(range(1, n + 1)))[:, newaxis], (1, m))
    plt.plot(nt.ravel(), data.ravel(), 'o', markersize=ms)
    plt.grid(True)
    plt.xlabel('Evolution')
    plt.ylabel('Function')
    plt.savefig(path + 'data.png')


# ==============================================================================
# Debugging
# ==============================================================================

# ------------------------------------------------------------------------------
# USE THIS SPACE FOR MULTIPROCESSING FUNCTIONS
# ------------------------------------------------------------------------------

from brg.datastructures.network.network import Network

from brg.numerical.matrices import connectivity_matrix
from brg.numerical.linalg import normrow
from brg.numerical.spatial import closest_points_points

from numpy import abs
from numpy import array
from numpy import mean
from numpy import newaxis
from numpy import shape
from numpy import sum
from numpy import tile
from numpy import zeros
from numpy import where
from numpy.random import rand

from scipy.optimize import differential_evolution
from scipy.optimize import fmin_l_bfgs_b
from scipy.optimize import fmin_slsqp

from time import time

import json


def funct(agents, args, t):
    return fn(agents[:, t], args)


def update(ub, C, Ct, Xn, l0, ks, P, Pn, V, BC, M, ind, tol, steps):
    u = zeros(shape(l0))
    u[ind] = array(ub)[:, newaxis]
    l0p = l0 + u
    ts, Uo = 0, 0
    res = 1000 * tol
    V *= 0
    while (ts <= steps) and (res > tol):
        uvw = C.dot(Xn)
        l = normrow(uvw)
        f = ks * (l - l0p)
        f *= f > 0
        R = (P - Ct.dot(uvw * tile(f / l, (1, 3)))) * BC
        Rn = normrow(R)
        res = 100 * mean(Rn / Pn)
        V += R / M
        Un = sum(0.5 * M * V * V)
        if Un < Uo:
            V *= 0
        Uo = Un
        Xn += V
        ts += 1
    return Xn, f, u


def fn(ub, args):
    C, Ct, X, l0, ks, P, Pn, V, BC, M, ind, tol, steps = args
    Xn, f, u = update(ub, C, Ct, X, l0, ks, P, Pn, V, BC, M, ind, tol, steps)
    norms = normrow(Xn - Xt)
    return mean(norms)

# ------------------------------------------------------------------------------
# USE THIS SPACE FOR MULTIPROCESSING FUNCTIONS
# ------------------------------------------------------------------------------

if __name__ == "__main__":

    # def fn(u, *args):
    #     # Booth's function, fopt=0, xopt=(1, 3)
    #     x = u[0]
    #     y = u[1]
    #     z = (x + 2*y - 7)**2 + (2*x + y - 5)**2
    #     return z

    # bounds = [(-10, 10) for i in range(2)]
    # fopt, xopt, data = solver(fn, bounds, population=100, iterations=20,
    #                           results=True, threads=1)
    # plot(data, 5, '/home/al/Temp/')

    # Import
    ipath = '/home/al/Dropbox/idata.json'
    opath = '/home/al/Dropbox/odata.json'
    spath = '/home/al/Dropbox/sdata.json'
    png_path = '/home/al/Temp/'
    network = Network.from_json(ipath)
    with open(spath, 'r') as fp:
        settings = json.load(fp)

    # Extract settings
    tol = settings['tol']
    steps = settings['steps']
    trials = settings['trials']
    solver = settings['solver']
    threads = 4

    # Extract data
    E = array(network.get_edges_attribute('E'))[:, newaxis]
    A = array(network.get_edges_attribute('A'))[:, newaxis]
    s0 = array(network.get_edges_attribute('s0'))[:, newaxis]
    ur = array(network.get_edges_attributes(('umin', 'umax')))
    P = array(network.get_vertices_attributes(('px', 'py', 'pz')))
    X = array(network.get_vertices_attributes(('x', 'y', 'z')))
    BC = array(network.get_vertices_attributes(('bcx', 'bcy', 'bcz')))

    # X and Xt mapping
    print('\nMapping target to actual surface ...')
    Xt = array(settings['target'])
    mapping = closest_points_points(X, Xt, threshold=10**2, distances=False)
    Xt = Xt[mapping, :]
    norms0 = normrow(X - Xt)

    # Connectivity
    ik = network.index_key()
    ki = network.key_index()
    edges = [(ki[u], ki[v]) for u, v in network.edges()]
    C = connectivity_matrix(edges, 'csr')
    Ct = C.transpose()

    # Initial
    l0 = normrow(C.dot(X))
    ks = E * A / l0
    M = tile(abs(Ct).dot(ks), (1, 3))
    V = zeros(P.shape)
    Pn = normrow(P)

    # Boundary
    urt = sum(abs(ur), 1)
    ind = where(urt > 0)[0]
    bounds = [tuple(uri) for uri in list(ur[ind, :])]

    # Optimisation
    tic = time()
    args = (C, Ct, X, l0, ks, P, Pn, V, BC, M, ind, tol, steps)
    print('Optimisation started...')
    fopt, uopt, data = de_solver(fn, bounds, population=settings['pop_factor'],
                iterations=trials, results=True, threads=threads, args=args)
    plot(data, 5, png_path)

    # Update network
    Xn, f, u = update(uopt, C, Ct, X, l0, ks, P, Pn, V, BC, M, ind, tol, steps)
    norms = normrow(Xn - Xt)
    for c, key in enumerate(network.vertices()):
        network.vertex[key]['norm'] = norms[c, 0]
        network.vertex[key]['x'] = X[c, 0]
        network.vertex[key]['y'] = X[c, 1]
        network.vertex[key]['z'] = X[c, 2]
    c = 0
    for i, j in edges:
        network.edge[ik[i]][ik[j]]['u'] = u[c, 0]
        network.edge[ik[i]][ik[j]]['f'] = f[c, 0]
        c += 1
    network.to_json(opath)

    toc = "{0:.3g}".format(time() - tic)
    print('------------------------------------------------------------------')
    print('Optimisation finished: ' + solver)
    print('Time taken: ' + toc + ' s')
    print('Starting norm: ' + str(int(1000 * mean(norms0))) + ' mm')
    print('Final norm: ' + str(int(1000 * mean(norms))) + ' mm')
    print('------------------------------------------------------------------')
