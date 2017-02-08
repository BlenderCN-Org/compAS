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
from brg.datastructures.mesh.algorithms import smooth_mesh_centroid
from brg.datastructures.mesh.algorithms import smooth_mesh_area
import brg_rhino
from brg_rhino.conduits.mesh import MeshConduit

def wrapper(conduit, vis):
    def ufunc(mesh,i):
        for key, a in mesh.vertices_iter(True):
           if a['guide_srf']:
               pt = (a['x'], a['y'], a['z'])
               point = rs.coerce3dpoint(pt)
               pt = a['guide_srf'].ClosestPoint(point)
               mesh.vertex[key]['x'] = pt[0]
               mesh.vertex[key]['y'] = pt[1]
               mesh.vertex[key]['z'] = pt[2] 
        if i%vis==0:
            rs.Prompt("Iteration {0}".format(i))
            conduit.redraw()
    return ufunc

obj = rs.GetObject("Select Mesh",32)

mesh = brg_rhino.mesh_from_guid(Mesh, obj)
mesh.set_dva({'guide_srf': None})

fixed = mesh.vertices_on_boundary()

srf = rs.GetObject("Select Guide Surface",8)
srf_id = rs.coerceguid(srf, True)
brep = rs.coercebrep(srf_id, False)

for key in mesh.vertices():
    if key not in fixed:
        mesh.vertex[key]['guide_srf'] = brep


conduit = MeshConduit(mesh)
conduit.Enabled = True
ufunc = wrapper(conduit, vis=1)

try:
    #smooth_mesh_area(mesh, fixed, kmax=100, ufunc=ufunc)
    smooth_mesh_centroid(mesh,fixed, kmax=100, ufunc=ufunc)
except Exception as e:
    print e
else:
    brg_rhino.draw_mesh(mesh)

finally:
    conduit.Enabled = False
    del conduit



