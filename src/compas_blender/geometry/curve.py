"""compas_blender.geometry.curve : Manipulating Blender curves."""

try:
    import bpy
    from mathutils.geometry import interpolate_bezier
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Oct 17, 2016'


def curve_to_mesh(curve):
    """ Convert a curve object into a mesh edge.

    Note:
        A copy is created, original curve is not deleted.

    Parameters:
        curve (obj): Curve object.

    Returns:
        obj: Resulting mesh object.
    """
    mesh = curve.to_mesh(bpy.context.scene, True, 'PREVIEW')
    name = 'mesh_' + curve.name
    mesh_object = bpy.data.objects.new(name, mesh)
    mesh_object.location = curve.location
    bpy.context.scene.objects.link(mesh_object)
    return mesh_object


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
    co = [list(point.co) for point in points]
    left = [list(point.handle_left) for point in points]
    right = [list(point.handle_right) for point in points]
    return co, left, right


def bezier_curve_interpolate(curve, number):
    """ Interpolate points along a Bezier curve.

    Parameters:
        curve (obj): Bezier curve object.
        number (int): Total number of interpolation points.

    Returns:
        list: Interpolated points x, y, z.
    """
    co, left, right = bezier_curve_points(curve)
    vectors = interpolate_bezier(co[0], right[0], left[1], co[1], number)
    points = [list(i) for i in vectors]
    return points
