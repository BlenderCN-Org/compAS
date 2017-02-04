"""
.. _brg.geometry:

********************************************************************************
geometry
********************************************************************************

.. module:: brg.geometry


A package defining common geometric functions and objects.

The functions in this package expect input arguments to be structured in a certain
way. This is properly documented in their *docstrings* (or at least, it should be :).
In general the following is assumed.

* point: the xyz coordinates as iterable of floats.
* vector: the xyz coordinates of the end point. the start is always the origin.
* line: a tuple with two points.
* ray: a tuple with two points.
* segment: a tuple with two points.
* circle: a tuple with a point,
  the normal vector of the plane of the circle, and the radius as float.
* polygon: a sequence of points.
  first and last are not the same. the polygon is assumed closed.
* polyline: a sequence of points.
  first and last are the same if the polyline is closed.
  otherwise, it is assumed open.
* polyhedron: vertices and faces.


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
    cross
    cross_2d
    dot
    dot_2d
    vector_component
    vector_component_2d
    angles_points
    angles_points_2d
    angles_vectors
    angles_vectors_2d
    angle_smallest_points
    angle_smallest_points_2d
    angle_smallest_vectors
    angle_smallest_vectors_2d
    length_vector
    length_vector_2d
    length_vector_sqrd
    length_vector_sqrd_2d
    distance_point_point
    distance_point_point_2d
    distance_point_point_sqrd
    distance_point_point_sqrd_2d
    distance_point_line
    distance_point_line_2d
    distance_point_line_sqrd
    distance_point_line_sqrd_2d
    distance_point_plane
    distance_line_line
    normal_polygon
    normal_triangle
    area_polygon
    area_polygon_2d
    area_triangle
    area_triangle_2d
    volume_polyhedron
    centroid_points
    centroid_points_2d
    center_of_mass_polygon
    center_of_mass_polygon_2d
    center_of_mass_polyhedron
    midpoint_line
    midpoint_line_2d
    sort_points
    bounding_box
    bounding_box_2d
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
    normalize_vector
    normalize_vectors


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


intersections
=============

.. currentmodule:: brg.geometry.intersections

:mod:`brg.geometry.brg.geometry.intersections`

.. autosummary::
    :toctree: generated/

    line_line_intersection
    line_line_intersection_2d
    lines_intersection
    lines_intersection_2d
    circle_circle_intersections
    circle_circle_intersections_2d


transformations
===============

.. currentmodule:: brg.geometry.transformations

:mod:`brg.geometry.transformations`

.. autosummary::
    :toctree: generated/

    translate_points
    translate_lines
    rotate_points
    scale_vector
    scale_vectors
    mirror_points_line
    mirror_points_plane
    project_point_plane
    project_points_plane
    project_point_line
    project_points_line


utilities
=========

.. currentmodule:: brg.geometry.utilities

:mod:`brg.geometry.utilities`

.. autosummary::
    :toctree: generated/

    multiply_matrix_vector
    multiply_matrix_matrix

"""

from .basics import *
