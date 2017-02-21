"""compas_blender.utilities.ui : Blender UI functions."""

import bpy


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__date__       = 'Oct 17, 2016'


def cursor_xyz():
    """ Returns the co-ordinates of the cursor.

    Parameters:
        None

    Returns:
        list: x, y and z position.
    """
    return list(bpy.context.scene.cursor_location.copy())
