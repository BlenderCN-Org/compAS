"""Vectorised differential evolution solver.

..  Copyright 2016 BLOCK Research Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        `http://www.apache.org/licenses/LICENSE-2.0`_

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

__author__     = 'Andrew Liew'
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'GNU - General Public License'
__version__    = '0.10'
__email__      = 'liew@arch.ethz.ch'
__status__     = 'Development'
__date__       = '10.10.2016'
__contact__    = """ETH Zurich,
Institute for Technology in Architecture,
BLOCK Research Group,
Stefano-Franscini-Platz 5,
HIL H 47,
8093 Zurich, Switzerland
"""

from numpy import array
from numpy import argmin
from numpy import min
from numpy import newaxis
from numpy import tile
from numpy import zeros
from numpy.random import rand
from random import sample


def solver(fn, bounds, population, iterations, *args):
    """ Call the differential evolution solver.

        Notes:
            - fn must return vectorised output for input (k, population).

        Parameters:
            fn         (obj)  : The function to evaluate and minimise.
            bounds     (list) : List of tuples defining bounds for each DoF.
            population (int)  : Number of agents in the population.
            iterations (int)  : Number of cross-over cycles to perform.
            arg        (seq)  : Sequence of optional arguments to pass to fn.

        Returns:
            None

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

    def fn1(u, *args):
        # Booth's function, fopt=0, xopt=(1, 3)
        x = u[0, :]
        y = u[1, :]
        z = (x + 2*y - 7)**2 + (2*x + y - 5)**2
        return z

    def fn2(u, *args):
        # Beale's function, fopt=0, xopt=(3, 0.5)
        x = u[0, :]
        y = u[1, :]
        z = ((1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 +
             (2.625 - x + x*y**3)**2)
        return z

    dof = 2
    population = 100
    iterations = 150
    bounds = [(-10, 10) for i in range(dof)]
    fopt, xopt = solver(fn1, bounds, population, iterations)
    print(xopt)
