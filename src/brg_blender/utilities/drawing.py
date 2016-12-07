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


def material_create(name, color, alpha=1):
    """ Create a material.

    Parameters:
        name (str): Name of the material.
        color (tuple): (R, G, B) with values [0 1].
        alpha (float): Alpha value from [0, 1].

    Returns:
        obj: Created material object
    """
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.diffuse_shader = 'LAMBERT'
    material.diffuse_intensity = 1.0
    material.alpha = alpha
    material.ambient = 1
    return material


def material_delete_all():
    """ Delete all materials.

    Parameters:
        None

    Returns:
        None
    """
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)


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
    object_layer([object], layer)
    return object


def xdraw_lines(lines):
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


def xdraw_texts(texts):
    """ Draw a set of text objects.

    Parameters:
        texts (dic): 'radius', 'pos', 'color', 'name', 'text' as the keys.

    Returns:
        list: Created text objects.
    """
    objects = []
    bpy.ops.object.text_add(radius=1, view_align=True, location=[0, 0, 0],
                            layers=layer_mask(0))
    object = bpy.context.object
    for t in texts:
        copy = object.copy()
        copy.location = Vector(t['pos'])
        copy.data = copy.data.copy()
        copy.scale *= t['radius']
        copy.data.materials.append(bpy.data.materials[t['color']])
        copy.name = t['name']
        copy.data.body = t['text']
        objects.append(copy)
    delete_objects([object])
    for object in objects:
        bpy.context.scene.objects.link(object)
    return objects


material_delete_all()
material_create('red', (1, 0, 0))
material_create('orange', (1, 0.5, 0))
material_create('yellow', (1, 1, 0))
material_create('blue', (0, 0, 1))
material_create('green', (0, 1, 0))
material_create('white', (1, 1, 1))
material_create('black', (0, 0, 0))
material_create('grey', (0.5, 0.5, 0.5))

# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from brg_blender.utilities.objects import delete_objects_all

    delete_objects_all()

    vertices = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]]
    edges = [[1, 3], [2, 3]]
    faces = [[0, 1, 2]]
    xdraw_mesh('mesh', vertices, edges, faces, layer=0)

    lines = [{'start': [0, 0, 1], 'end': [0, 1, 1], 'name': 'line1',
              'layer': 1, 'radius': 0.1, 'color': 'blue'},
             {'start': [1, 0, 1], 'end': [1, 1, 1], 'name': 'line2',
              'layer': 2, 'radius': 0.2, 'color': 'red'}]
    xdraw_lines(lines)

    cubes = [{'name': 's1', 'pos': [1, 1, 1], 'radius': 0.5, 'color': 'red'},
             {'name': 's2', 'pos': [2, 2, 2], 'radius': 1.0, 'color': 'blue'}]
    xdraw_cubes(cubes)
    texts = [{'name': 't1', 'pos': [1, 1, 3], 'radius': 0.5, 'color': 'red',
              'text': 'T1'},
             {'name': 't2', 'pos': [2, 2, 4], 'radius': 1.0, 'color': 'blue',
              'text': 'T2'}]
    xdraw_texts(texts)
