"""brg_blender.utilities.objects : Selecting or editing of Blender objects."""

import bpy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 17, 2016'


def delete_objects(objects):
    """ Delete a list of objects.

    Parameters:
        objects (list): Objects to delete.

    Returns:
        None
    """
    for object in objects:
        object.select = True
        bpy.ops.object.delete()


def delete_objects_all():
    """ Delete all sccene objects.

    Parameters:
        None

    Returns:
        None
    """
    for object in bpy.context.scene.objects:
        object.select = True
        bpy.ops.object.delete()


def get_objects_by_layer(layer, names=False):
    """ Retrieves the scene objects that are on a given layer.

    Parameters:
        layer (int): Layer number.
        names (boolean): Return object names.

    Returns:
        list: List of the objects in the layer.
        list: List of the object names in the layer.
    """
    objects = [ob for ob in bpy.context.scene.objects if ob.layers[layer]]
    object_names = [ob.name for ob in objects]
    if names:
        return objects, object_names
    else:
        return objects


def object_layer(object, layer):
    """ Changes the layer of the object.

    Parameters:
        object (obj): Object whose layer is to change.
        layer (int): Layer number.

    Returns:
        None
    """
    mask = tuple(i == layer for i in range(20))
    object.layers = mask


def select_objects(objects):
    """ Select specific scene objects.

    Parameters:
        objects (obj): Objects to select.

    Returns:
        None
    """
    select_objects_none()
    for object in objects:
        object.select = True


def select_objects_by_layer(layer):
    """ Select all scene objects in a given layer.

    Parameters:
        layer (int): Layer number.

    Returns:
        None
    """
    select_objects_none()
    objects = [ob for ob in bpy.context.scene.objects if ob.layers[layer]]
    for object in objects:
        object.select = True


def select_objects_all():
    """ Select all scene objects.

    Parameters:
        None

    Returns:
        list: All scene objects.
    """
    objects = bpy.context.scene.objects
    for object in objects:
        object.select = True
    return objects


def select_objects_none():
    """ Deselect all scene objects.

    Parameters:
        None

    Returns:
        None
    """
    objects = bpy.context.scene.objects
    for object in objects:
        object.select = False
