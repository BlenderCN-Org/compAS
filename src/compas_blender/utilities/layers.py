"""compas_blender.utilities.layers : Functions for manipulating Blender layers."""

from compas_blender.utilities.objects import delete_objects
from compas_blender.utilities.objects import get_objects_by_layer

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


def layer_clear(layer):
    """ Deletes all objects in a layer.

    Parameters:
        layer (int, str): Layer number or 'all'.

    Returns:
        None
    """
    if layer == 'all':
        for i in range(20):
            delete_objects(get_objects_by_layer(i))
    else:
        delete_objects(get_objects_by_layer(layer))


def layer_mask(layer):
    """ Creates a boolean layer mask.

    Parameters:
        layer (int): Layer number.

    Returns:
        tuple: With True at given layer number and False elsewhere.
    """
    return tuple(i == layer for i in range(20))


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
