#"""An example of dynamic relaxation for controlling beam elements."""

from compas_blender.geometry.curve import bezier_curve_interpolate
from compas_blender.geometry.mesh import network_from_bmesh

from compas_blender.utilities.drawing import draw_bmesh
from compas_blender.utilities.drawing import xdraw_lines
from compas_blender.utilities.layers import layer_clear
from compas_blender.utilities.objects import get_objects_by_layer
from compas_blender.utilities.objects import select_objects_none

from compas.numerical.methods.dynamic_relaxation import run
from compas.numerical.linalg import normrow

from numpy import array
from numpy import arctan2
from numpy import cos
from numpy import mean
from numpy import newaxis
from numpy import pi
from numpy import sin

from scipy.optimize import fmin_slsqp

from time import time


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


def update(dofs, network, dx, factor=1, tol=100, refresh=0, beams=None, Xt=None, scale=0.1, bmesh=None):
    x1, z1, r1, x2, z2, r2 = dofs
    for c, Xi in enumerate(Xt):
        network.set_vertex_attributes(c, {'x': Xi[0], 'y': Xi[1], 'z': Xi[2]})
    sp, ep = network.leaves()
    network.set_vertex_attributes(sp, {'x': x1, 'z': z1})
    network.set_vertex_attributes(sp + 1, {'x': dx * cos(r1) + x1, 'z': dx * sin(r1) + z1})
    network.set_vertex_attributes(ep, {'x': x2, 'z': z2})
    network.set_vertex_attributes(ep - 1, {'x': dx * cos(r2) + x2, 'z': dx * sin(r2) + z2})
    X, f, l = run(network, factor, tol, refresh=refresh, beams=beams, bmesh=bmesh, scale=scale)
    return X


def fn(dofs, *args):
    network, dx, factor, tol, refresh, beams, Xt, scale, bmesh = args
    X = update(dofs, network, dx, factor, tol, refresh, beams, Xt, scale, bmesh)
    norm = 1000 * mean(normrow(X - Xt))
    return norm


select_objects_none()
layer_clear(19)

# Input
L = 0.99732
nx = 50
tol = 1000
factor = 2
refresh = 100
du = 0.01
dr = 10 * pi / 180

# Setup
dx = L / nx
l0 = [dx] * nx
x = array([i * dx for i in range(nx + 1)])[:, newaxis]
xyz = [[x[i], 0, 0] for i in range(len(x))]
edges = [[i, i + 1] for i in range(nx)]
beams = {'beam': {'nodes': list(range(nx + 1))}}
bmesh = draw_bmesh('beam', xyz, edges)
target = get_objects_by_layer(1)[0]
Xt = array(bezier_curve_interpolate(target, nx + 1))

# Network
network = network_from_bmesh(bmesh)
network.set_vertices_attributes(network.vertices(), {'BC': [1, 1, 1], 'P': [0, 0, 0], 'EIx': 300, 'EIy': 300})
network.set_edges_attributes(network.edges(), {'E': 5 * 10**9, 'A': 0.001, 's0': 0, 'CT': 'CT', 'L0': None})
for fixed in [0, 1, nx - 1, nx]:
    network.set_vertex_attributes(fixed, {'BC': [0, 0, 0]})

layer_clear(0)

# Manual run
manual = 1
if manual:
    x1 = -0.35
    x2 = 0.3
    z1 = -0.1
    z2 = 0.0
    r1 = 100 * pi / 180
    r2 = 140 * pi / 180
    dofs = x1, z1, r1, x2, z2, r2
    X = update(dofs, network, dx, factor, tol, refresh, beams, Xt, scale=0.01, bmesh=True)

# Optimise
optimise = 0
if optimise:
    bnds = [(Xt[0, 0] - du, Xt[0, 0] + du), (Xt[0, 2] - du, Xt[0, 2] + du),
              (arctan2(Xt[1, 2] - Xt[0, 2], Xt[1, 0] - Xt[0, 0]) - dr,
               arctan2(Xt[1, 2] - Xt[0, 2], Xt[1, 0] - Xt[0, 0]) + dr),
              (Xt[-1, 0] - du, Xt[-1, 0] + du), (Xt[-1, 2] - du, Xt[-1, 2] + du),
              (arctan2(Xt[-2, 2] - Xt[-1, 2], Xt[-2, 0] - Xt[-1, 0]) - dr,
               arctan2(Xt[-2, 2] - Xt[-1, 2], Xt[-2, 0] - Xt[-1, 0]) + dr)]
    dof0 = [Xt[0, 0], Xt[0, 2], bnds[2][0], Xt[-1, 0], Xt[-1, 2], bnds[5][0]]
    r = 0.001
    col = 'green'
    xl, xu = bnds[0]
    zl, zu = bnds[1]
    al, au = bnds[3]
    bl, bu = bnds[4]
    lines = [
        {'colour': col, 'start': [xl, 0, zl], 'end': [xu, 0, zl], 'name': 'b1', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [xl, 0, zu], 'end': [xu, 0, zu], 'name': 't1', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [xl, 0, zl], 'end': [xl, 0, zu], 'name': 'l1', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [xu, 0, zl], 'end': [xu, 0, zu], 'name': 'r1', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [al, 0, bl], 'end': [au, 0, bl], 'name': 'b2', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [al, 0, bu], 'end': [au, 0, bu], 'name': 't2', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [al, 0, bl], 'end': [al, 0, bu], 'name': 'l2', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [au, 0, bl], 'end': [au, 0, bu], 'name': 'r2', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [Xt[0, 0], 0, Xt[0, 2]], 'end': [xu, 0, +du * sin(dr)], 'name': 'rp1', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [Xt[0, 0], 0, Xt[0, 2]], 'end': [xu, 0, -du * sin(dr)], 'name': 'rm1', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [Xt[-1, 0], 0, Xt[-1, 2]], 'end': [al, 0, Xt[-1, 2] + du * sin(dr)], 'name': 'rp2', 'radius': r, 'layer': 0},
        {'colour': col, 'start': [Xt[-1, 0], 0, Xt[-1, 2]], 'end': [al, 0, Xt[-1, 2] - du * sin(dr)], 'name': 'rm2', 'radius': r, 'layer': 0}]
    xdraw_lines(lines)
    args = network, dx, factor, tol, refresh, beams, Xt, 0, bmesh
    tic = time()
    opt = fmin_slsqp(fn, dof0, args=args, disp=1, bounds=bnds, full_output=1)
    dof_opt = opt[0]
    norm_opt = opt[1]
    X = update(dof_opt, network, dx, factor, tol, refresh, beams, Xt, scale=0.011, bmesh=True)
    print('Norm: {0:.3g} mm'.format(norm_opt))
    print(time() - tic)

select_objects_none()
