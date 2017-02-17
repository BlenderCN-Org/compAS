"""
.. _brg.datastructures.mesh:

********************************************************************************
mesh
********************************************************************************

.. module:: brg.datastructures.mesh


Package for working with mesh objects.


.. autosummary::
    :toctree: generated/

    Mesh

.. autosummary::
    :toctree: generated/

    plotter.MeshPlotter2D
    viewer.MeshViewer
    viewer.SubdMeshViewer


operations
==========

.. currentmodule:: brg.datastructures.mesh.operations

:mod:`brg.datastructures.mesh.operations`

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

.. autosummary::
    :toctree: generated/

    construct_dual_mesh
    planarize_mesh
    circularize_mesh
    unify_cycles_mesh
    flip_cycles_mesh
    smooth_mesh_centroid
    smooth_mesh_centerofmass
    smooth_mesh_length
    smooth_mesh_area
    smooth_mesh_angle
    subdivide_mesh
    subdivide_mesh_tri
    subdivide_mesh_quad
    subdivide_mesh_catmullclark
    subdivide_mesh_doosabin
    subdivide_trimesh_loop
    delaunay_from_points
    voronoi_from_points
    optimise_trimesh_topology


numerical
=========

.. currentmodule:: brg.datastructures.mesh.numerical

:mod:`brg.datastructures.mesh.numerical`

.. autosummary::
    :toctree: generated/

    mesh_adjacency_matrix
    mesh_connectivity_matrix
    mesh_laplacian_matrix
    trimesh_edge_cotangent
    trimesh_edge_cotangents
    trimesh_cotangent_laplacian_matrix
    trimesh_positive_cotangent_laplacian_matrix
    mesh_contours
    plot_mesh_contours
    mesh_isolines
    plot_mesh_isolines

"""

from .mesh import Mesh

