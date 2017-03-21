"""compas_blender.geometry.mesh : Manipulating Blender meshes."""

from numpy import array
from numpy import sum

from compas.datastructures.network import Network
from compas.datastructures.mesh import Mesh

from compas.numerical.linalg import normrow

from compas_blender.utilities.objects import select_objects

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


def colour_bmesh_vertices(bmesh, vertices, colours):
    """ Colour the vertices of a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.
        vertices (list): List of vertices to colour.
        colour (list): List of RGB colours [0, 1] (list).

    Returns:
        None
    """
    mesh = bmesh.data
    bpy.context.scene.objects.active = bmesh
    bmesh.select = True
    if mesh.vertex_colors:
        col = mesh.vertex_colors.active
    else:
        col = mesh.vertex_colors.new()
    for face in mesh.polygons:
        for i in face.loop_indices:
            j = mesh.loops[i].vertex_index
            if j in vertices:
                ind = vertices.index(j)
                col.data[i].color = colours[ind]


def bmesh_data(bmesh):
    """ Return the Blender mesh's vertices, edges and faces data.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Vertices.
        list: Edges.
        list: Faces.
    """
    vertices = [list(vertex.co) for vertex in bmesh.data.vertices]
    edges = [list(edge.vertices) for edge in bmesh.data.edges]
    faces = [list(face.vertices) for face in bmesh.data.polygons]
    return vertices, edges, faces


def bmesh_edge_lengths(bmesh):
    """ Retrieve the edge legnths of a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        array: Lengths of each edge.
        float: Total length.
    """
    vertices, edges, _ = bmesh_data(bmesh)
    X = array(vertices)
    uv = array(edges)
    lengths = normrow(X[uv[:, 1], :] - X[uv[:, 0], :])
    L = sum(lengths)[0]
    return lengths, L


def bmesh_remove_duplicate_vertices(bmesh):
    """ Remove duplicate overlapping vertices of a Blender mesh object.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        obj: New Blender mesh.
    """
    select_objects([bmesh])
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
    mesh = bmesh.from_edit_mesh(bpy.context.object.data)
    for vertex in mesh.verts:
        vertex.select = True
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')
    return mesh


def mesh_from_bmesh(bmesh):
    """ Create a Mesh datastructure from a Blender mesh's faces.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        obj: Mesh object.
    """
    vertices, edges, faces = bmesh_data(bmesh)
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    return mesh


def network_from_bmesh(bmesh):
    """ Create a Network datastructure from a Blender mesh's edges.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        obj: Network object.
    """
    vertices, edges, faces = bmesh_data(bmesh)
    network = Network.from_vertices_and_edges(vertices, edges)
    return network


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
