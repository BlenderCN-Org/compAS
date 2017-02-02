"""An example of dynamic relaxation for beam elements."""

from brg_blender.geometry.curve import bezier_curve_interpolate
from brg_blender.geometry.mesh import mesh_data
from brg_blender.geometry.mesh import mesh_edge_lengths

from brg_blender.utilities.drawing import xdraw_mesh
from brg_blender.utilities.drawing import xdraw_lines
from brg_blender.utilities.layers import layer_clear
from brg_blender.utilities.objects import get_objects_by_layer
from brg_blender.utilities.objects import select_objects_none

from brg.numerical.methods.dynamic_relaxation import run
from brg.numerical.spatial import closest_points_points
from brg.numerical.linalg import normrow

from math import sin, cos, pi

from numpy import array
from numpy import newaxis

import bpy

__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Jan 28, 2017'

    
layer_clear(0)

# Create starting mesh from lines
ux1 = -0.11
ux2 = 0.45
uy1 = -0.04
uy2 = -0.03
ur1 = 1.2 * pi / 2
ur2 = 1.2 * pi / 2
L = 1.0
nx = 100
n = nx + 1
dx = L / nx
x = [i * dx for i in range(nx + 1)]
edges = [[i, i + 1] for i in range(nx)]
vertices = [[x[i] * (ux2 - ux1) + ux1, 0, 0.2 * sin(pi * x[i] / L)] 
            for i in range(n)]
vertices[0][2] += uy1
vertices[-1][2] += uy2

# Boundaries
BC = [[[0], [0, 0, 0]],
      [[nx], [0, 0, 0]]]
if ur1 is not None:
    vertices[1] = [dx * cos(ur1) + vertices[0][0], 0, 
                   dx * sin(ur1) + vertices[0][2]]
    BC.append([[1], [0, 0, 0]])
if ur2 is not None:
    vertices[-2] = [dx * cos(ur2) + vertices[-1][0], 0, 
                    dx * sin(ur2) + vertices[-1][2]]
    BC.append([[nx - 1], [0, 0, 0]])

# Dynamic Relaxation set-up
mr = list(range(nx))
nr = list(range(n))
E = [[mr, 5 * 10**9]]
A = [[mr, 0.001]]
EIx = [5 * 10**9 * 7.955532**(-8)] * n
EIy = [5 * 10**9 * 7.955532**(-8)] * n
beams = {'beam_0': {'nodes': nr, 'EIx': EIx, 'EIy': EIy}}
l0 = [dx] * nx
mesh = xdraw_mesh('mesh_beam', vertices=vertices, edges=edges)
select_objects_none()

# Analyse
X = run(vertices, edges, l0, A, E, BC, beams=beams, rtype='magnitude_0.1', 
        tol=100, refresh=100, factor=10)
for c, i in enumerate(X):
    bpy.data.objects['mesh_beam'].data.vertices[c].co = i
dL, L = mesh_edge_lengths(mesh) 
print(L)

# Norms
target = get_objects_by_layer(4)[0]
points = bezier_curve_interpolate(target, 20)
ind = closest_points_points(points, X, distances=False)
lines = []
norms = []
for c, i in enumerate(ind):
    start = points[c]
    end = list(X[i, :])
    dU = (array(end) - array(start))
    norms.append(dU)
    lines.append({'start': start, 'end': end, 'layer': 0, 
                 'radius': 0.002, 'color': 'white', 'name': '{0}'.format(i)})
    xdraw_lines(lines)
print(array(norms))

print('\nSCRIPT FINISHED\n')
