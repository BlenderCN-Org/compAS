"""brg_blender.utilities.drawing : Functions for drawing in Blender."""

from brg_blender.utilities.layers import layer_mask

from brg_blender.utilities.objects import delete_objects
from brg_blender.utilities.objects import object_layer

from mathutils import Vector

import bpy

__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
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


def xdraw_mesh(name, vertices=[], edges=[], faces=[], layer=0):
    """ Draws a Blender mesh in the given layer.

    Parameters:
        name (str): Mesh name.
        vertices (list): Mesh vertices [x, y, z].
        edges (list): Mesh edges [vert1, vert2].
        faces (list): Mesh faces [vert1, vert2, ...].
        layer (int): Layer number.

    Returns:
        obj: Created mesh object.
    """
    mesh = bpy.data.meshes.new(name)
    object = bpy.data.objects.new(name, mesh)
    bpy.context.scene.objects.link(object)
    mesh.from_pydata(vertices, edges, faces)
    mesh.update(calc_edges=True)
    object_layer(object, layer)
    return object


def xdraw_lines(lines):
    # COLOR NOT YET IMPLEMENTED, FIX DUPLICATE NAME ERROR
    """ Draw a set of lines.

    Parameters:
        lines (dic): 'color', 'start', 'end', 'name', 'radius', 'layer' as keys.

    Returns:
        list: Created line objects.
    """
    objects = []
    for l in lines:
        # layer = l['layer']
        sp = l['start']
        ep = l['end']
        curve = bpy.data.curves.new(name=l['name'], type='CURVE')
        curve.dimensions = '3D'
        object = bpy.data.objects.new(l['name'], curve)
        object.location = [0, 0, 0]
        line = curve.splines.new('NURBS')
        line.points.add(2)
        line.points[0].co = sp + [1]
        line.points[1].co = ep + [1]
        line.order_u = len(line.points) - 1
        line.use_endpoint_u = True
        object.data.fill_mode = 'FULL'
        object.data.bevel_depth = l['radius']
        object.data.bevel_resolution = 0
        object.data.materials.append(bpy.data.materials[l['color']])
        objects.append(object)
    for object in objects:
        try:
            bpy.context.scene.objects.link(object)
        except:
            pass
    return objects


def xdraw_spheres(spheres, div=20):
    """ Draw a set of spheres.

    Parameters:
        spheres (dic): 'radius', 'pos', 'color', 'name' as the keys.
        div (int): Divisions for spheres.

    Returns:
        list: Created sphere objects.
    """
    objects = []
    bpy.ops.mesh.primitive_uv_sphere_add(size=1, location=[0, 0, 0],
                                         ring_count=div, segments=div,
                                         layers=layer_mask(0))
    object = bpy.context.object
    for s in spheres:
        copy = object.copy()
        copy.location = Vector(s['pos'])
        copy.data = copy.data.copy()
        copy.scale *= s['radius']
        copy.data.materials.append(bpy.data.materials[s['color']])
        copy.name = s['name']
        objects.append(copy)
    delete_objects([object])
    for object in objects:
        bpy.context.scene.objects.link(object)
    return objects


def xdraw_cubes(cubes):
    """ Draw a set of cubes.

    Parameters:
        cubes (dic): 'radius', 'pos', 'color', 'name' as the keys.

    Returns:
        list: Created cube objects.
    """
    objects = []
    bpy.ops.mesh.primitive_cube_add(radius=1, location=[0, 0, 0],
                                    layers=layer_mask(0))
    object = bpy.context.object
    for c in cubes:
        copy = object.copy()
        copy.location = Vector(c['pos'])
        copy.data = copy.data.copy()
        copy.scale *= c['radius']
        copy.data.materials.append(bpy.data.materials[c['color']])
        copy.name = c['name']
        objects.append(copy)
    delete_objects([object])
    for object in objects:
        bpy.context.scene.objects.link(object)
    return objects


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from brg_blender.utilities.objects import delete_objects_all

    delete_objects_all()

    vertices = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]]
    edges = [[1, 3], [2, 3]]
    faces = [[0, 1, 2]]
    xdraw_mesh('mesh', vertices, edges, faces, layer=5)

    lines = [{'start': [0, 0, 1], 'end': [0, 1, 1], 'name': 'line1',
              'layer': 1, 'radius': 0.1, 'color': 'blue'},
             {'start': [1, 0, 1], 'end': [1, 1, 1], 'name': 'line2',
              'layer': 2, 'radius': 0.2, 'color': 'red'}]
    xdraw_lines(lines)

    cubes = [{'name': 's1', 'pos': [1, 1, 1], 'radius': 0.5, 'color': 'red'},
               {'name': 's2', 'pos': [2, 2, 2], 'radius': 1.0, 'color': 'blue'}]
    #xdraw_cubes(cubes)
