# -*- coding: utf-8 -*-
# @Date      : 2016-10-18 21:56:20
# @Author    : Tom Van Mele (vanmelet@ethz.ch)
# @Copyright : 2016, Block Research Group
# @License   : MIT License


def unweld(mesh, fkey, where=None):
    face = []
    vertices = mesh.face_vertices(fkey, ordered=True)
    if not where:
        where = vertices
    for key in vertices:
        if key in where:
            x, y, z = mesh.vertex_coordinates(key)
            key = mesh.add_vertex(x=x, y=y, z=z)
        face.append(key)
    mesh.add_face(face)
    fface = mesh.face[fkey]
    rface = dict((v, u) for u, v in fface.iteritems())
    for key in where:
        d = fface[key]
        a = rface[key]
        mesh.halfedge[a][key] = None
        mesh.halfedge[key][d] = None
    del mesh.face[fkey]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
