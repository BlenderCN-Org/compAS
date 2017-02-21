"""An example of dynamic relaxation for beam elements."""

from compas_blender.geometry.curve import bezier_curve_interpolate

from compas_blender.utilities.drawing import xdraw_mesh
from compas_blender.utilities.layers import layer_clear
from compas_blender.utilities.objects import get_objects_by_layer
from compas_blender.utilities.objects import select_objects_none

from compas.numerical.methods.dynamic_relaxation import run
from compas.numerical.linalg import normrow

from math import pi

from numpy import array
from numpy import arctan2
from numpy import cos
from numpy import hstack
from numpy import mean
from numpy import newaxis
from numpy import sin
from numpy import vstack
from numpy import zeros

from scipy.optimize import fmin_slsqp

from time import time

import bpy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Jan 28, 2017'


def fn_update(dofs, x, dx, L, edges, l0, A, E, BC, P, beams, bmesh, rtol,
              refresh, factor, Xt=None):
    ux1, uz1, ur1, ux2, uz2, ur2 = dofs
    if Xt is not None:
        pts = array(Xt)
        pts[0, :] = [ux1, 0, uz1]
        pts[-1, :] = [ux2, 0, uz2]
    else:    
        pts = hstack([x * (ux2 - ux1) + ux1, zeros((len(x), 1)), sin(pi * x / L)])
        pts[0, 2] += uz1
        pts[-1, 2] += uz2
    pts[1, :] = [dx * cos(ur1) + pts[0, 0], 0, dx * sin(ur1) + pts[0, 2]]
    pts[-2, :] = [dx * cos(ur2) + pts[-1, 0], 0, dx * sin(ur2) + pts[-1, 2]]
    verts = [list(i) for i in list(pts)]
    X = run(verts, edges, l0, A, E, BC, P, beams=beams, bmesh=bmesh,
            rtype='magnitude_{0}'.format(rtol), tol=100, refresh=refresh,
            factor=factor)
    return X


def fn_norm(dofs, *args):
    x, dx, L, edges, l0, A, E, BC, P, beams, bmesh, rtol, refresh, factor, Xt = args
    X = fn_update(dofs, x, dx, L, edges, l0, A, E, BC, P, beams, bmesh, rtol,
                  refresh, factor, Xt)
    norm = 1000 * mean(normrow(X - Xt))
    return norm


layer_clear(0)

# Input
L = 1.0
nx = 50
n = nx + 1
mr = list(range(nx))
nr = list(range(n))
E = [[mr, 5 * 10**9]]
A = [[mr, 0.001]]
EIx = [300] * n
EIy = [300] * n
rtol = 10
factor = 5
refresh = 50
du = 0.01
dr = 1 * pi / 180

# Setup
dx = L / nx
l0 = [dx] * nx
x = array([i * dx for i in range(n)])[:, newaxis]
edges = [[i, i + 1] for i in range(nx)]
BC = [[[0, 1, nx - 1, nx], [0, 0, 0]]]
P = None
beams = {'beam': {'nodes': nr, 'EIx': EIx, 'EIy': EIy}}
vertices = [[x[i], 0, 0] for i in range(n)]
bmesh = xdraw_mesh('mesh_beam', vertices, edges)

# Target
target_curve = get_objects_by_layer(4)[0]
Xt = array(bezier_curve_interpolate(target_curve, n))
edgesC = [[i, i + n] for i in range(n)]

select_objects_none()

# Manual run
manual = 1
if manual:
    ux1 = -0.35
    uz1 = -0.0
    ur1 = 100 * pi / 180
    ux2 = 0.5
    uz2 = 0.0
    ur2 = 140 * pi / 180
    dofs = ux1, uz1, ur1, ux2, uz2, ur2
    X = fn_update(dofs, x, dx, L, edges, l0, A, E, BC, P, beams, bmesh, rtol,
                  refresh, factor, Xt=None)
    vertsC = vstack([X, Xt])
    mesh = xdraw_mesh('norms', vertsC, edgesC)
    norm = 1000 * mean(normrow(X - Xt))
    print('Norm: {0:.3g} mm'.format(norm))

# Optimise
optimise = 1
if optimise:
    bounds = [(Xt[0][0] - du, Xt[0][0] + du),
              (Xt[0][2] - du, Xt[0][2] + du),
              (arctan2(Xt[1][2] - Xt[0][2], Xt[1][0] - Xt[0][0]) - dr,
               arctan2(Xt[1][2] - Xt[0][2], Xt[1][0] - Xt[0][0]) + dr),
              (Xt[-1][0] - du, Xt[-1][0] + du),
              (Xt[-1][2] - du, Xt[-1][2] + du),
              (arctan2(Xt[-2][2] - Xt[-1][2], Xt[-2][0] - Xt[-1][0]) - dr,
               arctan2(Xt[-2][2] - Xt[-1][2], Xt[-2][0] - Xt[-1][0]) + dr)]
    dof0 = [Xt[0][0], Xt[0][2], bounds[2][0],
            Xt[-1][0], Xt[-1][2], bounds[5][0]]
    args = x, dx, L, edges, l0, A, E, BC, P, beams, bmesh, rtol, refresh, factor, Xt
    tic = time()
    opt = fmin_slsqp(fn_norm, dof0, args=args, disp=1, bounds=bounds, full_output=1)
    dof_opt = opt[0]
    norm_opt = opt[1]
    X = fn_update(dof_opt, x, dx, L, edges, l0, A, E, BC, P, beams, bmesh, rtol,
                  refresh, factor, Xt)
    vertsC = vstack([X, Xt])
    mesh = xdraw_mesh('norms', vertsC, edgesC)
    print('Norm: {0:.3g} mm'.format(norm_opt))
    print(time() - tic)

print('\nSCRIPT FINISHED\n')
