"""brg.numerical.solvers.vec_diff_evo : Vectorised differential evolution."""

from numpy import array
from numpy import argmin
from numpy import min
from numpy import newaxis
from numpy import tile
from numpy import zeros
from numpy.random import rand

from random import sample


__author__     = ['Andrew Liew <liew@arch.ethz.ch>', ]
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.10'
__date__       = '10.10.2016'


def solver(fn, bounds, population, iterations, *args):
    """ Call the vectorised differential evolution solver.

        Note:
            - fn must return vectorised output for input (k, population).

        Parameters:
            fn (obj): The function to evaluate and minimise.
            bounds (list): List of tuples defining bounds for each DoF.
            population (int): Number of agents in the population.
            iterations (int): Number of cross-over cycles or steps to perform.
            arg (seq): Sequence of optional arguments to pass to fn.

        Returns:
            float: Optimal value of objective function.
            array: Values that give optimum (minimised) function.

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
    fun = fn(agents, args)
    fopt = min(fun)
    print('Iteration: ' + str(ts) + ' fopt: ' + str(fopt))
    ac = zeros((k, population))
    bc = zeros((k, population))
    cc = zeros((k, population))
    while ts < iterations:
        ind = rand(k, population) < CR
        for i in range(population):
            inds = candidates[i, sample(range(population - 1), 3)]
            ac[:, i] = agents[:, inds[0]]
            bc[:, i] = agents[:, inds[1]]
            cc[:, i] = agents[:, inds[2]]
        agents_ = ind*(ac + F*(bc-cc)) + ~ind*agents
        fun_ = fn(agents_, args)
        log = (fun - fun_) > 0
        logt = tile(log, (k, 1))
        agents[logt] = agents_[logt]
        fun[log] = fun_[log]
        fopt = min(fun)
        xopt = agents[:, argmin(fun)]
        ts += 1
        ac *= 0
        bc *= 0
        cc *= 0
        print('Iteration: ' + str(ts) + ' fopt: ' + str(fopt))
    return fopt, xopt


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
