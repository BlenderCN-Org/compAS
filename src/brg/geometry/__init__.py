"""
.. _brg.geometry:

********************************************************************************
geometry
********************************************************************************

.. module:: brg.geometry


A package defining common geometric functions and objects.


elements
========

.. currentmodule:: brg.geometry.elements

:mod:`brg.geometry.elements`

.. autosummary::
    :toctree: generated

    Line
    Plane
    Point
    Polygon
    Polyhedron
    Polyline
    Spline
    Surface
    Vector


basics
======

.. currentmodule:: brg.geometry.basics

:mod:`brg.geometry.basics`

.. autosummary::
    :toctree: generated/

    add_vectors
    subtract_vectors

.. autosummary::
    :toctree: generated/

    cross
    cross_2d
    dot
    dot_2d
    vector_component
    vector_component_2d

.. autosummary::
    :toctree: generated/

    angles_points
    angles_points_2d
    angles_vectors
    angles_vectors_2d
    angle_smallest_points
    angle_smallest_points_2d
    angle_smallest_vectors
    angle_smallest_vectors_2d

.. autosummary::
    :toctree: generated/

    length_vector
    length_vector_2d
    length_vector_sqrd
    length_vector_sqrd_2d

.. autosummary::
    :toctree: generated/

    distance_point_point
    distance_point_point_2d
    distance_point_point_sqrd
    distance_point_point_sqrd_2d
    distance_point_line
    distance_point_line_2d
    distance_point_line_sqrd
    distance_point_line_sqrd_2d
    distance_point_plane
    distance_point_plane_2d
    distance_point_plane_sqrd
    distance_point_plane_sqrd_2d

.. autosummary::
    :toctree: generated/

    normal_polygon
    normal_triangle
    area_polygon
    area_polygon_2d
    area_triangle
    area_triangle_2d
    volume_polyhedron

.. autosummary::
    :toctree: generated/

    centroid_points
    centroid_points_2d
    center_of_mass_polygon
    center_of_mass_polygon_2d
    center_of_mass_polyhedron
    midpoint_line
    midpoint_line_2d


planar
======

.. currentmodule:: brg.geometry.planar

:mod:`brg.geometry.planar`

.. autosummary::
    :toctree: generated/

    is_ccw
    is_polygon_convex
    are_segments_intersecting
    is_polyline_selfintersecting
    is_point_in_triangle
    is_point_in_polygon
    is_point_in_circle
    closest_part_of_triangle


spatial
=======

.. currentmodule:: brg.geometry.spatial

:mod:`brg.geometry.spatial`

.. autosummary::
    :toctree: generated/

    sort_points
    bounding_box
    closest_point
    closest_point_on_line
    closest_point_on_segment
    closest_point_on_polyline
    closest_point_on_plane
    is_colinear
    is_coplanar
    is_point_on_plane
    is_point_on_line
    is_point_on_segment
    is_point_on_polyline
    is_point_in_triangle


intersections
=============

.. currentmodule:: brg.geometry.intersections

:mod:`brg.geometry.brg.geometry.intersections`


transformations
===============

.. currentmodule:: brg.geometry.transformations

:mod:`brg.geometry.transformations`

.. autosummary::
    :toctree: generated/

    translate_points
    translate_lines
    rotate_points
    normalize_vectors
    scale_points
    mirror_points_line
    mirror_points_plane
    project_points_plane
    project_points_line

"""

from .basics import *


