# ******************************************************************************
# smoothening (relaxation) with fixed boundary points of a
# given input mesh in rhino
# ******************************************************************************

import os
import compas

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import smooth_mesh_area

import compas_rhino as rhino

guid = rhino.select_mesh()
mesh = rhino.mesh_from_guid(Mesh, guid)

fixed = mesh.vertices_on_boundary()

smooth_mesh_area(mesh, fixed, kmax=100)

rhino.draw_mesh(mesh)

# make screenshot for the docs
filename = os.path.join(compas.TEMP, 'screenshots', 'mesh-smoothing.png')
rhino.screenshot_current_view(filename, draw_grid=True)