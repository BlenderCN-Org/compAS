__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'construct_dual_mesh',
]


def construct_dual_mesh(mesh, cls=None):
    """Construct the dual of a mesh."""
    if not cls:
        cls = type(mesh)
    fkey_center = dict((fkey, mesh.face_center(fkey)) for fkey in mesh.face)
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


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
