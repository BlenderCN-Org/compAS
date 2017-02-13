import rhinoscriptsyntax as rs

from brg.datastructures.mesh import Mesh
from brg.datastructures.mesh.algorithms.duality import construct_dual_mesh
from brg.geometry.planar import circle_from_points_2d

import brg_rhino

def construct_voronoi_mesh(mesh, cls=None):
    """Construct the voronoi dual of a mesh."""
    def circumference(vkeys):
        pts = [mesh.vertex_coordinates(vkey) for vkey in vkeys]
        a,b,c = pts
        pt,rad = circle_from_points_2d(a,b,c)
        return pt[0],pt[1],0.0
    
    if not cls:
        cls = type(mesh)
    fkey_center = dict((fkey, circumference(mesh.face_vertices(fkey))) for fkey in mesh.face)
    boundary = mesh.vertices_on_boundary()
    inner = list(set(mesh.vertex) - set(boundary))
    vertices = {}
    faces = {}
    for key in inner:
        fkeys = mesh.vertex_faces(key, ordered=True)
        for fkey in fkeys:
            if fkey not in vertices:
                vertices[fkey] = fkey_center[fkey]
        faces[key] = fkeys
    dual = cls()
    for key, (x, y, z) in vertices.items():
        dual.add_vertex(key, x=x, y=y, z=z)
    for fkey, vertices in faces.items():
        dual.add_face(vertices, fkey)
    return dual


obj = rs.GetObject("Select Mesh",32)
mesh = brg_rhino.mesh_from_guid(Mesh,obj)

if mesh.is_trimesh():
    voronoi = construct_voronoi_mesh(mesh)
    brg_rhino.draw_mesh(voronoi, show_faces=False)
                  
