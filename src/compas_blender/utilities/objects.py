"""compas_blender.utilities.objects : Selecting or editing of Blender objects."""

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
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


def objects_layer(objects, layer):
    """ Changes the layer of the objects.

    Parameters:
        objects (list): Objects whose layer to change.
        layer (int): Layer number.

    Returns:
        None
    """
    mask = tuple(i == layer for i in range(20))
    for object in objects:
        object.layers = mask


def object_name_show(objects, show=True):
    """ Display the name of listed objects.

    Parameters:
        objects (obj): Objects to display name.
        show (boolean): show=True or False.

    Returns:
        None
    """
    for object in objects:
        object.show_name = show


def objects_join(objects):
    """ Join a list of objects.

    Parameters:
        objects (list): Objects to join.

    Returns:
        obj: Joined object.
    """
    for object in bpy.context.scene.objects:
        object.select = False
    for object in objects:
        object.select = True
    bpy.context.scene.objects.active = objects[0]
    bpy.ops.object.join()
    return objects[0]


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
