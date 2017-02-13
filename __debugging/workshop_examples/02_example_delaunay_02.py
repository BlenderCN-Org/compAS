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
import brg_rhino

objs = rs.GetObjects("Select Points",1)
pts = [rs.PointCoordinates(obj) for obj in objs]

poly = rs.GetObject("Select polygon bondary",4)
boundary_polyline = []
if poly:
    boundary_polyline = rs.CurveEditPoints(poly)

polys = rs.GetObjects("Select polygon holes",4)
holes_polylines = []
if polys:
    for poly in polys:
        holes_polylines.append(rs.CurveEditPoints(poly))
faces = delaunay_from_points(pts,boundary_polyline,holes_polylines)

mesh = Mesh()
mesh = mesh.from_vertices_and_faces(pts,faces)
brg_rhino.draw_mesh(mesh)

