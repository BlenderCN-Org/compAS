"""
.. _brg.datastructures.network:

********************************************************************************
network
********************************************************************************

.. module:: brg.datastructures.network


Package for working with network objects.


.. autosummary::
    :toctree: generated/

    Network


operations
==========

.. currentmodule:: brg.datastructures.network.operations

:mod:`brg.datastructures.network.operations`

.. autosummary::
    :toctree: generated/

    split_edge_network


algorithms
==========

.. currentmodule:: brg.datastructures.network.algorithms

:mod:`brg.datastructures.network.algorithms`

.. autosummary::
    :toctree: generated/

    network_vertex_coloring

.. autosummary::
    :toctree: generated/

    construct_dual_network
    find_network_faces

.. autosummary::
    :toctree: generated/

    is_network_crossed
    are_network_edges_crossed
    count_network_crossings
    is_network_2d
    is_network_planar
    is_network_planar_embedding
    embed_network_in_plane

.. autosummary::
    :toctree: generated/

    smooth_network_mixed
    smooth_network_centroid
    smooth_network_area
    smooth_network_mass
    smooth_network_length
    smooth_network_angle


numerical
=========

.. currentmodule:: brg.datastructures.network.numerical

:mod:`brg.datastructures.network.numerical`

.. autosummary::
    :toctree: generated/

    network_adjacency_matrix
    network_degree_matrix
    network_connectivity_matrix
    network_laplacian_matrix
    network_face_matrix

"""

from .network import Network
