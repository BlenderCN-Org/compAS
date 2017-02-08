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

obj = rs.GetObject("Select Mesh",32)
mesh = brg_rhino.mesh_from_guid(Mesh,obj)

# get all indices of fixed points along the boundaries
fixed = mesh.vertices_on_boundary()

smooth_mesh_area(mesh,fixed,kmax=100)
#smooth_mesh_centroid(mesh,fixed,kmax=100)
brg_rhino.draw_mesh(mesh)
