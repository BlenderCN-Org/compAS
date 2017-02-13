"""
.. _brg_rhino.utilities:

********************************************************************************
utilities
********************************************************************************

.. module:: brg_rhino.utilities


This package contains many convenience functions for working and interacting
with Rhino.


document
========

.. currentmodule:: brg_rhino.utilities.document

:mod:`brg_rhino.utilities.document`

.. autosummary::
    :toctree: generated/

    get_document_name
    get_document_filename
    get_document_path
    get_document_dirname


layers
======

.. currentmodule:: brg_rhino.utilities.layers

:mod:`brg_rhino.utilities.layers`

.. autosummary::
    :toctree: generated/

    create_layers
    clear_layers
    delete_layers


objects
=======

.. currentmodule:: brg_rhino.utilities.objects

:mod:`brg_rhino.utilities.objects`

.. note::

    Note that the meaning of the naming conventions used here is somewhat different
    than those used in Rhino and rhinoscriptsyntax modules.

    Functions prefixed with ``get_`` imply that guids are obtained by applying some
    kind of filter. For example, get all lines with a specified naming pattern, on a
    specific layer, or with a specific color.

    Functions prefixed with ``select_`` imply that guids are obtained by manual
    selection.


.. autosummary::
    :toctree: generated/

    get_objects
    get_object_names
    get_object_attributes
    get_object_attributes_from_name
    delete_object
    delete_objects
    purge_objects
    get_points
    get_curves
    get_lines
    get_polylines
    get_polygons
    get_point_coordinates
    get_line_coordinates
    get_polyline_coordinates
    get_polygon_coordinates
    get_meshes
    get_mesh_face_vertices
    get_mesh_vertex_coordinates
    get_mesh_vertex_colors
    set_mesh_vertex_colors
    get_mesh_vertices_and_faces
    get_mesh_vertex_index
    get_mesh_face_index
    get_mesh_edge_index
    select_point
    select_points
    select_curve
    select_curves
    select_line
    select_lines
    select_polyline
    select_polylines
    select_polygon
    select_polygons
    select_surface
    select_surfaces
    select_mesh
    select_meshes
    is_curve_line
    is_curve_polyline
    is_curve_polygon


scripts
=======

.. currentmodule:: brg_rhino.utilities.scripts

:mod:`brg_rhino.utilities.scripts`

.. autosummary::
    :toctree: generated/

    ScriptServer


misc
====

.. currentmodule:: brg_rhino.utilities.misc

:mod:`brg_rhino.utilities.misc`

.. autosummary::
    :toctree: generated/

    wait
    get_tolerance
    toggle_toolbargroup
    pick_point
    browse_for_folder
    browse_for_file
    print_display_on
    display_message
    display_text
    display_image
    display_html
    update_settings
    update_attributes
    update_named_values


drawing
=======

.. currentmodule:: brg_rhino.utilities.drawing

:mod:`brg_rhino.utilities.drawing`

.. autosummary::
    :toctree: generated/

    xdraw_labels
    xdraw_points
    xdraw_lines
    xdraw_polylines
    xdraw_faces
    xdraw_cylinders
    xdraw_pipes
    xdraw_spheres
    xdraw_mesh

"""

from .document import *
from .layers import *
from .objects import *
from .misc import *
from .drawing import *
