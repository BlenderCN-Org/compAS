# ******************************************************************************
# computes the delaunay triangulation for given set of points and
# polygons to define boundaries in rhino
# ******************************************************************************

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import delaunay_from_points

import compas_rhino as rhino

guids = rhino.select_points()
vertices = rhino.get_point_coordinates(guids)

guid = rhino.select_polyline("Select boundary.")
boundary = rhino.get_polyline_coordinates(guid)

guids = rhino.select_polylines("Select holes.")
holes = [rhino.get_polyline_coordinates(guid) for guid in guids]

faces = delaunay_from_points(vertices, boundary, holes)

mesh = Mesh()
mesh = mesh.from_vertices_and_faces(vertices, faces)

rhino.draw_mesh(mesh)
