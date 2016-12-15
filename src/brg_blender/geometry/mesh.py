"""brg_blender.geometry.mesh : Manipulating Blender meshes."""

import bpy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 17, 2016'


def mesh_data(mesh):
    """ Return the mesh's nodes, edges and faces data.

    Parameters:
        mesh (obj): Blender mesh object.

    Returns:
        list: Mesh vertices.
        list: Mesh edges.
        list: Mesh faces.
    """
    vertices = [list(vertex.co) for vertex in mesh.data.vertices]
    edges = [list(edge.vertices) for edge in mesh.data.edges]
    faces = [list(face.vertices) for face in mesh.data.polygons]
    return vertices, edges, faces
