"""
.. _brg_rhino.helpers:

********************************************************************************
helpers
********************************************************************************

.. module:: brg_rhino.helpers

:mod:`brg_rhino.helpers`


mesh
====

.. currentmodule:: brg_rhino.helpers.mesh

:mod:`brg_rhino.helpers.mesh`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/


network
=======

.. currentmodule:: brg_rhino.helpers.network

:mod:`brg_rhino.helpers.network`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/


volmesh
=======

.. currentmodule:: brg_rhino.helpers.volmesh

:mod:`brg_rhino.helpers.volmesh`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

"""

from .network import draw_network
from .network import select_network_vertices
from .network import select_network_vertex
from .network import select_network_edges
from .network import select_network_edge
from .network import display_network_vertex_labels
from .network import display_network_edge_labels
from .network import display_network_face_labels
from .network import update_network_attributes
from .network import update_network_vertex_attributes
from .network import update_network_edge_attributes
# from .network import move_network_vertex
# from .network import move_network_vertices

from .mesh import mesh_from_guid
from .mesh import mesh_from_surface
from .mesh import mesh_from_surface_uv
from .mesh import mesh_from_surface_heightfield
from .mesh import draw_mesh
# from .mesh import select_mesh_vertices
# from .mesh import select_mesh_vertex
# from .mesh import select_mesh_faces
# from .mesh import select_mesh_face
# from .mesh import select_mesh_edges
# from .mesh import select_mesh_edge
# from .mesh import display_mesh_vertex_labels
# from .mesh import display_mesh_edge_labels
# from .mesh import display_mesh_face_labels
# from .mesh import update_mesh_attributes
# from .mesh import update_mesh_vertex_attributes
# from .mesh import update_mesh_face_attributes
# from .mesh import update_mesh_edge_attributes

from .volmesh import volmesh_from_polysurfaces
from .volmesh import volmesh_from_wireframe
from .volmesh import draw_volmesh
