"""brg_blender.drawing : Functions for drawing in Blender."""

import bpy

from brg_blender.utilities.layers import layer_mask


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 17, 2016'


def color_vertex(object, vertices, color):
    """ Color the vertex of a Blender mesh.

    Parameters:
        object (obj): Mesh object.
        vertices (list, str): List of vertices to color, or 'all'.
        color (list): RGB colour.

    Returns:
        None
    """
    mesh = object.data
    bpy.context.scene.objects.active = object
    object.select = True
    if mesh.vertex_colors:
        col = mesh.vertex_colors.active
    else:
        col = mesh.vertex_colors.new()
    for face in mesh.polygons:
        for i in face.loop_indices:
            j = mesh.loops[i].vertex_index
            if vertices == 'all':
                col.data[i].color = color
            elif j in vertices:
                col.data[i].color = color


def xdraw_mesh(name, vertices=[], edges=[], faces=[]):
    """ Draws a Blender mesh in the current layer.

    Parameters:
        name (str): Mesh name.
        vertices (list): Mesh vertices [x, y, z].
        edges (list): Mesh edges [vert1, vert2].
        faces (list): Mesh faces [vert1, vert2 ...].

    Returns:
        obj: Created mesh object.
    """
    mesh = bpy.data.meshes.new(name)
    object = bpy.data.objects.new(name, mesh)
    bpy.context.scene.objects.link(object)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update(calc_edges=True)
    return object


def xdraw_spheres(spheres):
    """ Draw a set of spheres.

    Parameters:
        spheres (dic): 'radius', 'pos', 'layer', 'color' as the keys.

    Returns:
        list: Created sphere objects.
    """
    objects = []
    for s in spheres:
        radius = s['radius']
        pos = s['pos']
        layer = s['layer']
        bpy.ops.mesh.primitive_uv_sphere_add(
            size=radius,
            location=pos,
            layers=layer_mask(layer))
        color = s['color']
        object = bpy.context.scene.objects.active
        objects.append(object)
        color_vertex(object, 'all', color)
    return objects
