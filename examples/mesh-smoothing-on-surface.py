# ******************************************************************************
# smoothening (relaxation) of a given input mesh in rhino on a target
# surface with fixed boundary points
# using a user function (ufunc) to constrain the points to the target
# surface and MeshConduit for visualization
# ******************************************************************************

from __future__ import print_function

from compas.datastructures.mesh import Mesh

from compas.datastructures.mesh.algorithms import smooth_mesh_centroid

from compas_rhino.conduits.mesh import MeshConduit
from compas_rhino.geometry import RhinoSurface

import compas_rhino as rhino


def ufunc(mesh, i, args):
    conduit, vis, surface, fixed = args
    for key, attr in mesh.vertices_iter(True):
        if key in fixed:
            continue
        xyz = mesh.vertex_coordinates(key)
        point = surface.closest_point(xyz)
        mesh.vertex[key]['x'] = point[0]
        mesh.vertex[key]['y'] = point[1]
        mesh.vertex[key]['z'] = point[2]
    if i % vis == 0:
        print("Iteration {0}".format(i))
        conduit.redraw()


guid = rhino.select_mesh()
mesh = rhino.mesh_from_guid(Mesh, guid)

mesh.set_default_vertex_attributes({'guide_srf': None})

fixed = mesh.vertices_on_boundary()

guid = rhino.select_surface()
surface = RhinoSurface(guid)

try:
    conduit = MeshConduit(mesh)
    conduit.Enabled = True

    smooth_mesh_centroid(mesh, fixed, kmax=100, ufunc=ufunc, ufunc_args=(conduit, 2, surface, fixed))

except Exception as e:
    print(e)

else:
    rhino.draw_mesh(mesh)

finally:
    conduit.Enabled = False
    del conduit
