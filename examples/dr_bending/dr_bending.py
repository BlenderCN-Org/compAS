"""An example of dynamic relaxation for beam elements."""

from brg_blender.utilities.drawing import xdraw_mesh
from brg_blender.utilities.layers import layer_clear

from brg.numerical.methods import dr_functions

import bpy
import imp

imp.reload(dr_functions)


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Oct 20, 2016'


# Create mesh from lines
L = 1.0
nx = 100
dx = L / nx
x = [i * dx for i in range(nx + 1)]
X = [[xi, 0, 0.1] for xi in x]
edges = [[i, i + 1] for i in range(nx)]
layer_clear(0)
mesh = xdraw_mesh('mesh_beam', vertices=X, edges=edges)

# Dynamic Relaxation
m = len(edges)
n = len(X)
ind_m = list(range(m))
ind_n = list(range(n))
E = [[ind_m, 5 * 10**9]]
A = [[ind_m, 0.001]]
P = [[ind_n, [0, 0, 100]]]
BC = [[[0], [0, 0, 0]],
      [[n - 1], [0, 0, 0]]]
EIx = [5 * 10**9 * 7.955532**(-8)] * n
EIy = [5 * 10**9 * 7.955532**(-8)] * n
beams = {'nodes': [ind_n], 'EIx': [EIx], 'EIy': [EIy]}
Xn = dr_functions.run(X, edges, BC, P, E, A, tol=1, steps=10000, beams=beams,
                      factor=5)
for c, i in enumerate(Xn):
    bpy.data.objects['mesh_beam'].data.vertices[c].co = i
bpy.context.scene.update()

print('\nSCRIPT FINISHED\n')
