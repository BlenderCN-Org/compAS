import rhinoscriptsyntax as rs

from brg.datastructures.mesh import Mesh
from brg.utilities import i_to_rgb
import brg_rhino


obj = rs.GetObject("Select Mesh",32)
mesh = brg_rhino.mesh_from_guid(Mesh,obj)

edge_lengths = {(u,v) : mesh.edge_length(u,v,) for u, v in mesh.edges()}

max_val = max(edge_lengths.values())
print "The maximum edge length is {0}".format(max_val)
min_val = min(edge_lengths.values())
print "The minimum edge length is {0}".format(min_val)
length_norm = {}
for u,v in mesh.edges():
    length_norm[(u,v)] = (edge_lengths[u,v] - min_val)  / (max_val - min_val)

color_e = {(u, v): i_to_rgb(length_norm[(u,v)]) for u, v in mesh.edges()}

#print "The maximum edge length is {0}".format(max(edge_lengths))
#print color_e
if mesh.is_trimesh():
    brg_rhino.draw_mesh(mesh,
                  name='mesh',
                  layer=None,
                  clear=True,
                  redraw=True,
                  show_faces=False,
                  show_vertices=True,
                  show_edges=True,
                  vertex_color=None,
                  edge_color=color_e,
                  face_color=None)