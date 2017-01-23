""".. _brg.numerical:

********************************************************************************
numerical
********************************************************************************

.. module:: brg.numerical

:mod:`brg.numerical`

A package for numerical computation.

.. rubric:: Submodules

.. toctree::
    :maxdepth: 1

    brg.numerical.euler
    brg.numerical.gpu
    brg.numerical.methods
    brg.numerical.solvers


geometry
========

.. currentmodule:: brg.numerical.geometry

:mod:`brg.numerical.geometry`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    lengths


linalg
======

.. currentmodule:: brg.numerical.linalg

:mod:`brg.numerical.linalg`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    nullspace
    rank
    dof
    pivots
    nonpivots
    rref
    chofactor
    lufactorized
    normrow
    normalizerow
    rot90
    solve_with_known
    spsolve_with_known


matrices
========

.. currentmodule:: brg.numerical.matrices

:mod:`brg.numerical.matrices`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    adjacency_matrix
    degree_matrix
    connectivity_matrix
    laplacian_matrix
    face_matrix
    mass_matrix
    stiffness_matrix
    equilibrium_matrix


operators
=========

.. currentmodule:: brg.numerical.operators

:mod:`brg.numerical.operators`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    grad
    div
    curl


spatial
=======

.. currentmodule:: brg.numerical.spatial

:mod:`brg.numerical.spatial`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    closest_points_points
    project_points_heightfield
    iterative_closest_point
    bounding_box_2d
    bounding_box_3d


statistics
==========

.. currentmodule:: brg.numerical.statistics

:mod:`brg.numerical.statistics`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    principal_components


utilities
=========

.. currentmodule:: brg.numerical.utilities

:mod:`brg.numerical.utilities`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    set_array_print_precision
    unset_array_print_precision


xforms
======

.. currentmodule:: brg.numerical.xforms

:mod:`brg.numerical.xforms`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    translation_matrix
    rotation_matrix
    random_rotation_matrix
    scale_matrix
    projection_matrix

"""
