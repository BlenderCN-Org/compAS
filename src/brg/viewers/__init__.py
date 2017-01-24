"""
.. _brg.viewers:

********************************************************************************
viewers
********************************************************************************

.. module:: brg.viewers


Standalone (OpenGL) viewers for visualisation outside of CAD environments.


.. autosummary::
    :toctree: generated/
    
    Viewer
    ViewerApp


drawing
=======

.. currentmodule:: brg.viewers.drawing

:mod:`brg.viewers.drawing`

.. autosummary::
    :toctree: generated/

    draw_points
    draw_lines
    draw_faces
    draw_sphere
    xdraw_points
    xdraw_lines
    xdraw_polygons


helpers
=======

.. currentmodule:: brg.viewers.helpers

:mod:`brg.viewers.helpers`

.. autosummary::
    :toctree: generated/

    Axes
    Camera
    Grid
    Mouse    


widgets
=======

.. currentmodule:: brg.viewers.widgets

:mod:`brg.viewers.widgets`

.. autosummary::
    :toctree: generated/

    BrowserWidget
    ScreenWidget

"""

from .viewer import Viewer
from .app import ViewerApp
