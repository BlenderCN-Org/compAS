"""
.. _brg_rhino.utilities:

********************************************************************************
utilities
********************************************************************************

.. module:: brg_rhino.utilities

:mod:`brg_rhino.utilities`


document
========

.. currentmodule:: brg_rhino.utilities.document

:mod:`brg_rhino.utilities.document`

.. rubric:: Functions

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

.. rubric:: Functions

.. autosummary::
    :toctree: generated/
    
    create_layers
    clear_layers
    delete_layers


objects
=======

.. currentmodule:: brg_rhino.utilities.objects

:mod:`brg_rhino.utilities.objects`


Note that the meaning of the naming conventions used here is somewhat different
than those used in Rhino and rhinoscriptsyntax modules.

Functions prefixed with ``get_`` imply that guids are obtained by applying some
kind of filter. For example, get all lines with a specified naming pattern, on a
specific layer, or with a specific color.

Functions prefixed with ``select_`` imply that guids are obtained by manual
selection.


.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    get_objects

.. autosummary::
    :toctree: generated/

    get_object_names
    get_object_attributes
    get_object_attributes_from_name

.. autosummary::
    :toctree: generated/

    delete_object
    delete_objects
    
.. autosummary::
    :toctree: generated/

    purge_object
    purge_objects

.. autosummary::
    :toctree: generated/

    get_points
    get_curves
    get_lines
    get_polylines
    get_polygons

.. autosummary::
    :toctree: generated/

    get_point_coordinates
    get_line_coordinates
    get_polyline_coordinates
    get_polygon_coordinates

.. autosummary::
    :toctree: generated/

    get_meshes
    get_mesh_face_vertices
    get_mesh_vertex_coordinates
    get_mesh_vertex_colors
    set_mesh_vertex_colors
    get_mesh_vertices_and_faces
    get_mesh_vertex_index
    get_mesh_face_index
    get_mesh_edge_index

.. autosummary::
    :toctree: generated/

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

.. autosummary::
    :toctree: generated/

    is_curve_line
    is_curve_polyline
    is_curve_polygon


scripts
=======

.. currentmodule:: brg_rhino.utilities.scripts

:mod:`brg_rhino.utilities.scripts`

.. rubric:: Classes

.. autosummary::
    :toctree: generated/

    ScriptServer


misc
====

.. currentmodule:: brg_rhino.utilities.misc

:mod:`brg_rhino.utilities.misc`

.. rubric:: Functions

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

.. rubric:: Functions

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

from .document import get_document_name
from .document import get_document_filename
from .document import get_document_path
from .document import get_document_dirname

from .layers import create_layers
from .layers import clear_layers
from .layers import delete_layers

from .objects import get_objects
from .objects import delete_object
from .objects import delete_objects
from .objects import purge_object
from .objects import purge_objects
from .objects import get_object_names
from .objects import get_object_attributes
from .objects import get_object_attributes_from_name
from .objects import is_curve_line
from .objects import is_curve_polyline
from .objects import is_curve_polygon
from .objects import select_point
from .objects import select_points
from .objects import select_curve
from .objects import select_curves
from .objects import select_line
from .objects import select_lines
from .objects import select_polyline
from .objects import select_polylines
from .objects import select_polygon
from .objects import select_polygons
from .objects import select_surface
from .objects import select_surfaces
from .objects import select_mesh
from .objects import select_meshes
from .objects import get_points
from .objects import get_curves
from .objects import get_lines
from .objects import get_polylines
from .objects import get_polygons
# rename
from .objects import get_point_coordinates
from .objects import get_line_coordinates
from .objects import get_polyline_coordinates
from .objects import get_polygon_coordinates
from .objects import get_meshes
from .objects import get_mesh_edge_index
from .objects import get_mesh_edge_vertex_indices
from .objects import get_mesh_face_index
from .objects import get_mesh_face_indices
from .objects import get_mesh_vertex_coordinates
from .objects import get_mesh_vertex_index
from .objects import get_mesh_vertex_indices
from .objects import get_mesh_edge_vertex_indices
from .objects import get_mesh_face_vertex_indices
from .objects import get_mesh_vertex_face_indices
from .objects import get_mesh_face_vertices
from .objects import get_mesh_vertices_and_faces
from .objects import get_mesh_vertex_colors
from .objects import set_mesh_vertex_colors

from .misc import browse_for_folder
from .misc import browse_for_file
from .misc import print_display_on
from .misc import display_message
from .misc import display_text
from .misc import display_image
from .misc import display_html
from .misc import get_tolerance
from .misc import toggle_toolbargroup
from .misc import pick_point
from .misc import update_settings
from .misc import update_attributes
from .misc import update_named_values
from .misc import wait

from .drawing import xdraw_labels
from .drawing import xdraw_points
from .drawing import xdraw_lines
from .drawing import xdraw_polylines
from .drawing import xdraw_faces
from .drawing import xdraw_cylinders
from .drawing import xdraw_pipes
from .drawing import xdraw_spheres
from .drawing import xdraw_mesh
