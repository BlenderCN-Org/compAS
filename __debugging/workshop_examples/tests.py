# this example requires PyOpenGL and PySide

from brg.datastructures.mesh import Mesh
from brg.geometry.elements.polyhedron import Polyhedron
from brg.datastructures.mesh.viewer import SubdMeshViewer
from brg.datastructures.mesh.algorithms import subdivide_mesh_doosabin

cube = Polyhedron.generate(6)

mesh = Mesh.from_vertices_and_faces(cube.vertices, cube.faces)

viewer = SubdMeshViewer(mesh, subdfunc=subdivide_mesh_doosabin, width=600, height=600)

viewer.axes.x_color = (0.1, 0.1, 0.1)
viewer.axes.y_color = (0.1, 0.1, 0.1)
viewer.axes.z_color = (0.1, 0.1, 0.1)

viewer.axes_on = False
viewer.grid_on = False

viewer.setup()
viewer.show()