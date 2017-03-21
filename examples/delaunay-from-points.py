# ******************************************************************************
# computes the delaunay triangulation for given set of points in rhino
# ******************************************************************************

import compas_rhino as rhino

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import delaunay_from_points

guids = rhino.select_points()
vertices = rhino.get_point_coordinates(guids)

faces = delaunay_from_points(vertices)

mesh = Mesh.from_vertices_and_faces(vertices, faces)

rhino.draw_mesh(mesh)
