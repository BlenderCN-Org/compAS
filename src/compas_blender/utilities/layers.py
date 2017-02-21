"""brg_blender.utilities.layers : Manipulating Blender layers."""

from compas_blender.utilities.objects import delete_objects
from compas_blender.utilities.objects import get_objects_by_layer

import bpy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Oct 17, 2016'


def layer_clear(layer):
    """ Deletes all objects in a layer.

    Parameters:
        layer (int, str): Layer number or 'all'.

    Returns:
        None
    """
    if layer == 'all':
        for i in range(20):
            objects = get_objects_by_layer(i)
            delete_objects(objects)
    else:
        objects = get_objects_by_layer(layer)
        delete_objects(objects)


def layer_mask(layer):
    """ Creates a boolean layer mask.

    Parameters:
        layer (int): Layer number.

    Returns:
        tuple: With True at given layer number and False elsewhere.
    """
    return tuple(i == layer for i in range(20))
