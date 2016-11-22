import sys
sys.path.append('D:/bb/brg_framework/src/')

from brg.datastructures.network.network import Network

from brg.numerical.geometry import lengths
from brg.numerical.matrices import connectivity_matrix
from brg.numerical.matrices import mass_matrix
from brg.numerical.linalg import normrow

from numpy import abs
from numpy import array
from numpy import max
from numpy import mean
from numpy import newaxis
from numpy import sum
from numpy import tile
from numpy import zeros

from time import time

import json


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 20, 2016'


def residual(f, l, P, S, uvw, Ct, BC, Pn, f0, rtype='force'):
    R = (P - S - Ct.dot(uvw * tile(f/l, (1, 3)))) * BC
    Rn = normrow(R)
    if  rtype == 'force':
        res = mean(Rn / Pn)
    elif rtype == 'prestress':
        res = mean(Rn / mean(abs(f0)))
    elif 'magnitude' in rtype:
        res = max(Rn / float(rtype.split('_')[1]))
    return R, 100*res


# Import
debug = 0
if  debug:
    ipath = '/home/al/Dropbox/idata.json'
    opath = '/home/al/Dropbox/odata.json'
    spath = '/home/al/Dropbox/sdata.json'
else:
    ipath = sys.argv[1]
    opath = sys.argv[2]
    spath = sys.argv[3]
network = Network.from_json(ipath)
with open(spath, 'r') as fp:
    settings = json.load(fp)

# Extract data
E = array(network.get_edges_attribute('E'))[:, newaxis]
A = array(network.get_edges_attribute('A'))[:, newaxis]
s0 = array(network.get_edges_attribute('s0'))[:, newaxis]
P = array(network.get_vertices_attributes(('px', 'py', 'pz')))
X = array(network.get_vertices_attributes(('x', 'y', 'z')))
BC = array(network.get_vertices_attributes(('bcx', 'bcy', 'bcz')))

# Connectivity
ki = network.key_index()
edges = [(ki[u], ki[v]) for u, v in network.edges()]
C = connectivity_matrix(edges, 'csr')
Ct = C.transpose()

# Initial
f0 = s0*A
uvw0, l0 = lengths(C, X)
ks = E*A/l0
M = mass_matrix(Ct, E, A, l0, f0, c=settings['factor'])
S = zeros(P.shape)
V = zeros(P.shape)
Pn = normrow(P)

# Main loop
ts, Uo = 0, 0
res = 10**6
tic = time()
while (ts <= settings['steps']) and (res > settings['tol']):
    uvw, l = lengths(C, X)
    f = f0 + ks*(l-l0)
    if  settings['ct'] == 't':
        f *= f > 0
    elif settings['ct'] == 'c':
        f *= f < 0
    R, res = residual(f, l, P, S, uvw, Ct, BC, Pn, f0, rtype=settings['rtype'])
    V += R/M
    Un = sum(0.5*M*V*V)
    if  Un < Uo:
        V *= 0
    Uo = Un
    X += V
    if  ts % 100 == 0:
        print('ts:' + str(ts) + ' res:' + str(res))
    ts += 1
print('-' * 50)
print('Iterations: ' + str(ts-1))
print('Residual: ' + '{0:.3g}'.format(res))
print('Time: ' + '{0:.3g}'.format(time() - tic) + 's')
print('-' * 50)

# Export network
for c, i in enumerate(network.vertices()):
    network.vertex[i]['x'] = X[c, 0]
    network.vertex[i]['y'] = X[c, 1]
    network.vertex[i]['z'] = X[c, 2]
c = 0
ik = network.index_key()
for u, v in edges:
    network.edge[ik[u]][ik[v]]['f'] = f[c, 0]
    c += 1
network.to_json(opath)
