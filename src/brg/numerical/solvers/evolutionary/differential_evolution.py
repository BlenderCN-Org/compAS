"""brg.numerical.solvers.evolutionary : Differential evolution."""

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

import json
import multiprocessing


__author__     = ['Andrew Liew <liew@arch.ethz.ch>', ]
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.10'
__date__       = '10.10.2016'


def de_solver(fn, bounds, population, iterations, results=None, threads=1,
              F=0.8, CR=0.9, name='Differential evolution', args=()):
    """ Call the differential evolution solver.

    Note:
        fn returns vectorised output for input (k, population) if threads=0.

    Parameters:
        fn (obj): The function to evaluate and minimise.
        bounds (list): List of tuples defining bounds for each DoF.
        population (int): Number of agents in the population.
        iterations (int): Number of cross-over cycles or steps to perform.
        results (str): Where to store results files.
        threads (int): Number of threads/processes for multiprocessing.
        F (float): Differential evolution parameter.
        CR (float): Differential evolution cross-over ratio parameter.
        name (str): Name of the analysis.
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
        >>> fopt, xopt = solver(fn, bounds, population=100, iterations=150,
                                threads=0)
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

    # Setup population
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
    if threads > 1:
        t = range(population)
        pool = multiprocessing.Pool(processes=threads)
        func = partial(funct, agents, args)
        fun = array(pool.map(func, t))
        pool.close()
        pool.join()
    elif threads == 1:
        fun = zeros(population)
        for i in range(population):
            fun[i] = fn(agents[:, i], args)
    else:
        fun = fn(agents, args)
    fopt = min(fun)
    print('Iteration: {0}  fopt: {1}'.format(ts, fopt))
    ac = zeros((k, population))
    bc = zeros((k, population))
    cc = zeros((k, population))
    data = zeros((iterations, population))

    # Start evolution
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
        if threads > 1:
            t = range(population)
            pool = multiprocessing.Pool(processes=threads)
            func = partial(funct, agents_, args)
            fun_ = array(pool.map(func, t))
            pool.close()
            pool.join()
        elif threads == 1:
            fun_ = zeros(population)
            for i in range(population):
                fun_[i] = fn(agents_[:, i], args)
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
        print('Iteration: {0}  fopt: {1}'.format(ts, fopt))

        # Save generation
        if results:
            fnm = results + 'generation_{0:0>4}_population.pop'.format(ts - 1)
            with open(fnm, 'w') as f:
                f.write('Generation\n')
                f.write('{0}\n'.format(ts - 1))
                f.write('\n')
                f.write('Number of individuals per generation\n')
                f.write('{0}\n'.format(population))
                f.write('\n')
                f.write('Population scaled variables\n')
                for i in range(population):
                    entry = [str(i)] + [str(j) for j in list(agents[:, i])]
                    f.write(', '.join(entry) + '\n')
                f.write('\n')
                f.write('Population fitness value\n')
                for i in range(population):
                    f.write('{0}, {1}\n'.format(i, fun[i]))
                f.write('\n')

    # Save parameters
    if results:
        parameters = {
            'num_pop': population,
            'fit_name': name,
            'min_fit': None,
            'fit_type': 'min',
            'end_gen': ts,
            'num_gen': iterations,
            'start_from_gen': 0}
        fnm = '{0}parameters.json'.format(results)
        with open(fnm, 'w+') as fp:
            json.dump(parameters, fp)

    return fopt, xopt


def funct(agents, args, t):
    return fn(agents[:, t], args)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    def fn(u, *args):
        # Booth's function, fopt=0, xopt=(1, 3)
        x = u[0]
        y = u[1]
        z = (x + 2 * y - 7)**2 + (2 * x + y - 5)**2
        return z

    bounds = [(-10, 10) for i in range(2)]
    fopt, xopt = de_solver(fn, bounds, population=20, iterations=100, threads=0)
