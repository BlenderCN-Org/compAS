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
from brg.datastructures.mesh import Mesh
from brg.datastructures.mesh.algorithms import smooth_mesh_centroid
from brg.datastructures.mesh.algorithms import smooth_mesh_area
import brg_rhino
from brg_rhino.conduits.mesh import MeshConduit

def wrapper(conduit, vis):
    def ufunc(mesh,i):
        if i%vis==0:
            rs.Prompt("Iteration {0}".format(i))
            conduit.redraw()
    return ufunc

obj = rs.GetObject("Select Mesh",32)
mesh = brg_rhino.mesh_from_guid(Mesh,obj)

# get all indices of fixed points along the boundaries
fixed = mesh.vertices_on_boundary()

conduit = MeshConduit(mesh)
conduit.Enabled = True
ufunc = wrapper(conduit, vis=2)

keys = ['161','256']
for key in keys:
    mesh.vertex[key]['z'] -= 20
    fixed.add(key)  

try:
    smooth_mesh_area(mesh, fixed, kmax=100, ufunc=ufunc)
    #smooth_mesh_centroid(mesh, fixed, kmax=150, ufunc=ufunc)
except Exception as e:
    print e
else:
    brg_rhino.draw_mesh(mesh)

finally:
    conduit.Enabled = False
    del conduit



