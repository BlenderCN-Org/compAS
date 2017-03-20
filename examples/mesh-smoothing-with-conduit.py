# ******************************************************************************
# smoothening (relaxation) with fixed boundary points of a
# given input mesh in rhino
# using a user function (ufunc) and MeshConduit for visualization
# ******************************************************************************

from __future__ import print_function

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.algorithms import smooth_mesh_area

from compas_rhino.conduits.mesh import MeshConduit

import compas_rhino as rhino


def ufunc(mesh, i, args):
    conduit, vis = args
    if i % vis == 0:
        print("Iteration {0}".format(i))
        conduit.redraw()


guid = rhino.select_mesh()
mesh = rhino.mesh_from_guid(Mesh, guid)

fixed = mesh.vertices_on_boundary()

for key in [161, 256]:
    mesh.vertex[key]['z'] -= 20
    fixed.add(key)

try:
    conduit = MeshConduit(mesh)
    conduit.Enabled = True

    smooth_mesh_area(mesh, fixed, kmax=100, ufunc=ufunc, ufunc_args=(conduit, 5))

except Exception as e:
    print(e)

else:
    rhino.draw_mesh(mesh)

finally:
    conduit.Enabled = False
    del conduit
