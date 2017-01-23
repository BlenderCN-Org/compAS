"""
.. _brg.datastructures.mesh:

********************************************************************************
mesh
********************************************************************************

.. module:: brg.datastructures.mesh

:mod:`brg.datastructures.mesh`

Package for working with mesh objects.

.. rubric:: Classes

.. autosummary::
    :toctree: generated/

    Mesh


operations
==========

.. currentmodule:: brg.datastructures.mesh.operations

:mod:`brg.datastructures.mesh.operations`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    collapse_edge_mesh
    collapse_edge_trimesh
    cycle_face_mesh
    insert_edge_mesh
    split_edge_mesh
    split_edge_trimesh
    split_face_mesh
    swap_edge_trimesh
    unweld_vertices_mesh


algorithms
==========

.. currentmodule:: brg.datastructures.mesh.algorithms

:mod:`brg.datastructures.mesh.algorithms`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    construct_dual_mesh

.. autosummary::
    :toctree: generated/

    planarize_mesh
    circularize_mesh
    mesh_contours
    mesh_isolines
    mesh_gradient
    mesh_curvature

.. autosummary::
    :toctree: generated/

    unify_cycles_mesh
    flip_cycles_mesh

.. autosummary::
    :toctree: generated/

    smooth_mesh_centroid
    smooth_mesh_centerofmass
    smooth_mesh_length
    smooth_mesh_area
    smooth_mesh_angle

.. autosummary::
    :toctree: generated/

    subdivide_mesh
    subdivide_mesh_tri
    subdivide_mesh_quad
    subdivide_mesh_catmullclark
    subdivide_mesh_doosabin
    subdivide_trimesh_loop

.. autosummary::
    :toctree: generated/

    delaunay_from_mesh
    delaunay_from_points
    delaunay_from_boundary

.. autosummary::
    :toctree: generated/

    optimise_trimesh_topology


numerical
=========

.. currentmodule:: brg.datastructures.mesh.numerical

:mod:`brg.datastructures.mesh.numerical`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/
    
    mesh_adjacency_matrix
    mesh_connectivity_matrix
    mesh_laplacian_matrix
    trimesh_edge_cotangent
    trimesh_edge_cotangents
    trimesh_cotangent_laplacian_matrix
    trimesh_positive_cotangent_laplacian_matrix


utilities
=========

.. currentmodule:: brg.datastructures.mesh.utilities

:mod:`brg.datastructures.mesh.utilities`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

"""

from .mesh import Mesh

