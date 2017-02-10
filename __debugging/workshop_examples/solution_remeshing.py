import rhinoscriptsyntax as rs

from brg.datastructures.mesh import Mesh
from brg.datastructures.mesh.operations import swap_edge_trimesh

import brg_rhino

obj = rs.GetObject("Select Mesh",32)
mesh = brg_rhino.mesh_from_guid(Mesh,obj)
rs.DeleteObject(obj)

while True:
    brg_rhino.draw_mesh(mesh,show_faces=False)
    rs.EnableRedraw()
    pt_obj = rs.GetObject("Select Vertex",1)
    if not pt_obj: break
    key = rs.ObjectName(pt_obj).split('.')[-1]
    if mesh.vertex_degree(key) != 6:
        print("Vertex has not a degree of 6!")
        continue
    nbrs = mesh.vertex_neighbours(key, ordered=True)
    for nbr in nbrs[::2]:
        swap_edge_trimesh(mesh,key, nbr)