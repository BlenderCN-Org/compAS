from __future__ import print_function


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'unweld_vertices_mesh',
]


def unweld_vertices_mesh(mesh, fkey, where=None):
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

    import compas
    from compas.datastructures.mesh.mesh import Mesh

    data = compas.get_data('faces.obj')
    mesh = Mesh.from_obj(data)

    fkey  = '12'
    where = mesh.face_vertices(fkey)[0:1]
    xyz   = mesh.face_centroid(fkey)

    unweld_vertices_mesh(mesh, fkey, where)

    # move the unwelded vertex to the original centroid of the face it (partially)
    # disconnects
    mesh.vertex['36']['x'] = xyz[0]
    mesh.vertex['36']['y'] = xyz[1]
    mesh.vertex['36']['z'] = xyz[2]

    print(mesh)

    mesh.draw(
        show_vertices=True,
        face_label=dict((fkey, fkey) for fkey in mesh.face)
    )
