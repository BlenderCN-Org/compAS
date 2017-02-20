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
* line: a tuple with two points representing a continuous line (ray).
* segment: a tuple with two points representing a line segment.
* plane: a tuple with a base point and normal vector.
* circle: a tuple with a point,
  the normal vector of the plane of the circle, and the radius as float.
* polygon: a sequence of points.
  first and last are not the same. the polygon is assumed closed.
* polyline: a sequence of points.
  first and last are the same if the polyline is closed.
  otherwise, it is assumed open.
* polyhedron: vertices and faces.


spatial
=======

.. currentmodule:: brg.geometry.spatial

:mod:`brg.geometry.spatial`

constructors
------------

.. autosummary::
    :toctree: generated/

    vector_from_points
    plane_from_points
    bestfit_plane_from_points
    circle_from_points

miscellaneous
-------------

.. autosummary::
    :toctree: generated/

    vector_component

operations
----------

.. autosummary::
    :toctree: generated/

    add_vectors
    subtract_vectors
    scale_vector
    normalize_vector
    normalize_vectors
    dot_vectors
    cross_vectors

length and distance
-------------------

.. autosummary::
    :toctree: generated/

    length_vector
    length_vector_sqrd
    distance_point_point
    distance_point_point_sqrd
    distance_point_line
    distance_point_line_sqrd
    distance_point_plane
    distance_line_line

angles
------

.. autosummary::
    :toctree: generated/

    angles_points
    angles_vectors
    angle_smallest_points
    angle_smallest_vectors

average
-------

.. autosummary::
    :toctree: generated/

    centroid_points
    center_of_mass_polygon
    center_of_mass_polyhedron
    midpoint_line

area and volume
---------------

.. autosummary::
    :toctree: generated/

    area_polygon
    area_triangle
    volume_polyhedron
    bounding_box

proximity
---------

.. autosummary::
    :toctree: generated/

    closest_point_in_cloud
    closest_point_on_line
    closest_point_on_segment
    closest_point_on_polyline
    closest_point_on_plane

orientation
-----------

.. autosummary::
    :toctree: generated/

    normal_polygon
    normal_triangle

queries
-------

.. autosummary::
    :toctree: generated/

    is_colinear
    is_coplanar
    is_polygon_convex
    is_point_on_plane
    is_point_on_line
    is_point_on_segment
    is_closest_point_on_segment
    is_point_on_polyline
    is_point_in_triangle
    is_point_in_circle
    is_intersection_line_line
    is_intersection_line_plane
    is_intersection_segment_plane
    is_intersection_plane_plane
    is_intersection_line_triangle
    is_intersection_box_box

intersections
-------------

.. autosummary::
    :toctree: generated/

    intersection_line_line
    intersection_circle_circle
    intersection_line_triangle
    intersection_line_plane
    intersection_segment_plane
    intersection_plane_plane
    intersection_plane_plane_plane
    intersection_lines
    intersection_planes

transformations
---------------

.. autosummary::
    :toctree: generated/

    translate_points
    translate_lines
    rotate_points
    mirror_point_point
    mirror_points_point
    mirror_point_line
    mirror_points_line
    mirror_point_plane
    mirror_points_plane
    project_point_plane
    project_points_plane
    project_point_line
    project_points_line


planar
======================================

.. currentmodule:: brg.geometry.planar

:mod:`brg.geometry.planar`

.. autosummary::
    :toctree: generated/

    vector_from_points_2d
    circle_from_points_2d
    vector_component_2d
    add_vectors_2d
    subtract_vectors_2d
    scale_vector_2d
    normalize_vector_2d
    normalize_vectors_2d
    dot_vectors_2d
    cross_vectors_2d
    length_vector_2d
    length_vector_sqrd_2d
    distance_two_points_2d
    distance_two_points_sqrd_2d
    distance_point_line_2d
    distance_point_line_sqrd_2d
    distance_two_lines_2d
    distance_two_lines_sqrd_2d
    angles_points_2d
    angles_vectors_2d
    angle_smallest_points_2d
    angle_smallest_vectors_2d
    midpoint_two_points_2d
    centroid_points_2d
    center_of_mass_polygon_2d
    area_polygon_2d
    area_triangle_2d
    bounding_box_2d
    closest_point_on_line_2d
    closest_point_on_segment_2d
    closest_point_on_polygon_2d
    closest_part_of_triangle
    is_ccw_2d
    is_colinear_2d
    is_polygon_convex_2d
    is_point_on_line_2d
    is_point_on_segment_2d
    is_point_on_polygon_2d
    is_point_in_triangle_2d
    is_point_in_polygon_2d
    is_intersection_line_line_2d
    is_intersection_segment_segment_2d
    intersection_line_line_2d
    intersection_lines_2d
    intersection_circle_circle_2d
    translate_points_2d
    translate_lines_2d
    rotate_points_2d
    mirror_point_point_2d
    mirror_points_point_2d
    mirror_point_line_2d
    mirror_points_line_2d
    project_point_line_2d
    project_points_line_2d


elements
========

The objects defined in this package provide an object-oriented interface to most
of the functionality in the geometry package.

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

"""

from .spatial import *
