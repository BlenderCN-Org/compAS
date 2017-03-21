# ******************************************************************************
# creates a triangulated mesh from a given boundary curve and a edge
# target length
# ******************************************************************************

from __future__ import print_function

import os
import rhinoscriptsyntax as rs

import compas
import compas_rhino as rhino

from compas.datastructures.mesh import Mesh

from compas.datastructures.mesh.algorithms import delaunay_from_points
from compas.datastructures.mesh.algorithms import optimise_trimesh_topology

from compas_rhino.conduits.mesh import MeshConduit


def ufunc(mesh, i, args):
    conduit, vis = args
    if i % vis == 0:
        print("Iteration {0}".format(i))
        conduit.redraw()
        # screenshot for the docs
        n = str(i).zfill(5)
        filename = os.path.join(compas.TEMP, 'screenshots/mesh-remeshing-' + n + '.png')
        rhino.screenshot_current_view(filename, scale=0.5, draw_grid=True)


crv = rs.GetObject("Select Boundary Curve", 4)
trg = rs.GetReal("Select Edge Target Length", 2.5)
pts = rs.DivideCurve(crv, rs.CurveLength(crv) / trg)

faces = delaunay_from_points(pts, pts)
mesh = Mesh.from_vertices_and_faces(pts, faces)

conduit = MeshConduit(mesh)
conduit.Enabled = True

try:
    optimise_trimesh_topology(mesh, trg, kmax=250, ufunc=ufunc, ufunc_args=(conduit, 2))

except Exception as e:
    print(e)

else:
    rhino.draw_mesh(mesh)
    # screenshot for the docs
    n = str(172).zfill(5)
    filename = os.path.join(compas.TEMP, 'screenshots/mesh-remeshing-' + n + '.png')
    rhino.screenshot_current_view(filename, scale=0.5, draw_grid=True)

finally:
    conduit.Enabled = False
    del conduit
