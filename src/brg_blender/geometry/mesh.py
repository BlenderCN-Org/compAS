"""brg_blender.geometry.mesh : Manipulating Blender meshes."""

from numpy import array

from brg.numerical.linalg import normrow

import bpy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Oct 17, 2016'


def mesh_edge_lengths(mesh):
    """ Retrieve the edge legnths of a mesh.

    Parameters:
        mesh (obj): Mesh object.

    Returns:
        array: Lengths of each edge.
        float: Total length.
    """
    vertices, edges, _ = mesh_data(mesh)
    X = array(vertices)
    uv = array(edges)
    dL = normrow(X[uv[:, 1], :] - X[uv[:, 0], :])
    L = sum(dL)[0]
    return dL, L


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


def mesh_remove_duplicate_vertices(mesh):
    """ Remove duplicate overlapping vertices of a mesh object.

    Parameters:
        mesh (obj): Mesh object to remove vertex duplicates.

    Returns:
        None
    """
    select_objects([mesh])
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
    mesh = bmesh.from_edit_mesh(bpy.context.object.data)
    for vertex in mesh.verts:
        vertex.select = True
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')
