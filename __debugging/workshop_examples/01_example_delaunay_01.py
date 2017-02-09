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

objs = rs.GetObjects("Select Points",1)
pts = [rs.PointCoordinates(obj) for obj in objs]

faces = delaunay_from_points(pts)
rs.AddMesh(pts,faces)
