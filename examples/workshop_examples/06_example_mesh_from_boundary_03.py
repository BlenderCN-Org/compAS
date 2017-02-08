__author__    = 'Matthias Rippmann'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'rippmann@arch.ethz.ch'

# **************************************************************************
# **************************************************************************
# use with geometry_tests.3dm
# computes the delaunay triangulation for given set of points
# **************************************************************************
# **************************************************************************

import rhinoscriptsyntax as rs
from brg.datastructures.mesh.algorithms.triangulation import delaunay_from_points
from brg.datastructures.mesh import Mesh
from brg.datastructures.mesh.algorithms import optimise_trimesh_topology
import brg_rhino
from brg_rhino.conduits.mesh import MeshConduit


def wrapper(conduit, vis):
    def ufunc(mesh,i):
        if i%vis==0:
            rs.Prompt("Iteration {0}".format(i))
            conduit.redraw()
    return ufunc

crv = rs.GetObject("Select Boundary Curve",4)
trg = rs.GetReal("Select Edge Target Length",2.5)

pts = rs.DivideCurve(crv,rs.CurveLength(crv)/trg)

faces = delaunay_from_points(pts,pts)
mesh = Mesh()
mesh = mesh.from_vertices_and_faces(pts,faces)

conduit = MeshConduit(mesh)
conduit.Enabled = True
ufunc = wrapper(conduit, vis=1)

try:
    optimise_trimesh_topology(mesh,trg,kmax=250,ufunc=ufunc)
except Exception as e:
    print e
else:
    brg_rhino.draw_mesh(mesh)

finally:
    conduit.Enabled = False
    del conduit

