"""compas_blender.geometry.curve : Manipulating Blender curves."""

from mathutils.geometry import interpolate_bezier

import bpy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


def bezier_curve_interpolate(curve, number=3):
    """ Interpolate points along a Bezier curve.

    Parameters:
        curve (obj): Bezier curve object.
        number (int): Number of interpolation points.

    Returns:
        list: Interpolated points [x, y, z.]
    """
    co, left, right = bezier_curve_points(curve)
    vectors = interpolate_bezier(co[0], right[0], left[1], co[1], number)
    points = [list(i) for i in vectors]
    return points


def bezier_curve_points(curve):
    """ Return a Bezier curve's control points.

    Parameters:
        curve (obj): Bezier curve object.

    Returns:
        list: Control point locations.
        list: Control point left handles.
        list: Control point right handles.
    """
    points = curve.data.splines[0].bezier_points
    co = [list(i.co) for i in points]
    left = [list(i.handle_left) for i in points]
    right = [list(i.handle_right) for i in points]
    return co, left, right


def curve_to_bmesh(curve, divisions=10, delete=False):
    """ Convert a Blender curve object into a bmesh of edges.

    Parameters:
        curve (obj): Curve object.
        divisions (int): Number of divisions along length.
        delete (bool): Delete original curve.

    Returns:
        obj: Resulting bmesh object.
    """
    curve.data.resolution_u = divisions
    mesh = curve.to_mesh(bpy.context.scene, True, 'PREVIEW')
    if delete:
        curve.select = True
        bpy.ops.object.delete()
    name = 'bmesh_{0}'.format(curve.name)
    bmesh = bpy.data.objects.new(name, mesh)
    bmesh.location = [0, 0, 0]
    bpy.context.scene.objects.link(bmesh)
    return bmesh


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities.objects import get_objects_by_layer

    curve = get_objects_by_layer(0)[0]
    curve_to_bmesh(curve, divisions=3)
    c, l, r = bezier_curve_points(curve)
    points = bezier_curve_interpolate(curve, number=3)
    print(points)
