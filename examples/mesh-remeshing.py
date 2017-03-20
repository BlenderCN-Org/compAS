# ******************************************************************************
# creates a triangulated mesh from a given boundary curve and a edge
# target length
# ******************************************************************************

import rhinoscriptsyntax as rs

import compas_rhino as rhino

from compas.datastructures.mesh import Mesh

from compas.datastructures.mesh.algorithms import delaunay_from_points
from compas.datastructures.mesh.algorithms import optimise_trimesh_topology

from compas_rhino.conduits.mesh import MeshConduit


def wrapper(conduit, vis):
    def ufunc(mesh, i):
        if i % vis == 0:
            rs.Prompt("Iteration {0}".format(i))
            conduit.redraw()
    return ufunc


crv = rs.GetObject("Select Boundary Curve", 4)
trg = rs.GetReal("Select Edge Target Length", 2.5)

pts = rs.DivideCurve(crv, rs.CurveLength(crv) / trg)

faces = delaunay_from_points(pts, pts)
mesh = Mesh.from_vertices_and_faces(pts, faces)

conduit = MeshConduit(mesh)
conduit.Enabled = True
ufunc = wrapper(conduit, vis=1)

try:
    optimise_trimesh_topology(mesh, trg, kmax=250, ufunc=ufunc)

except Exception as e:
    print e

else:
    rhino.draw_mesh(mesh)

finally:
    conduit.Enabled = False
    del conduit
