
.. brg.geometry:

********************************************************************************
brg.geometry
********************************************************************************

brg.geometry : A package defining common geometric functions and objects.



.. rubric:: **Packages**

.. toctree::
   :glob:
   :maxdepth: 1

   brg-geometry-elements
   brg-geometry-shapes

.. rubric:: Modules

* `arithmetic`_
* `functions`_
* `intersections`_
* `planar`_
* `queries`_
* `spatial`_
* `transformations`_
* `utilities`_

-------


arithmetic
================================================================================



.. toctree::
   :glob:

   brg-geometry-arithmetic-add_vectors
   brg-geometry-arithmetic-subtract_vectors



functions
================================================================================

This module defines basic geometry functions.

All functions assume the provided input is three-dimensional. A corresponding
two-dimensional function can be accessed by appending ``_2d`` to the function
name.

>>> from brg.geometry import cross
>>> from brg.geometry import cross_2d
>>> u = [1.0, 0.0, 0.0]
>>> v = [0.0, 1.0, 0.0]
>>> cross(u, v)
[0.0, 0.0, 1.0]
>>> cross_2d(u, v)
[0.0, 0.0, 1.0]


For notes and algorithms dealing with polygons and meshes see [paulbourke]_

.. rubric:: References

.. [paulbourke] `<http://paulbourke.net/geometry/polygonmesh/>`_


.. toctree::
   :glob:

   brg-geometry-functions-angles
   brg-geometry-functions-angle_smallest
   brg-geometry-functions-length
   brg-geometry-functions-length_sqrd
   brg-geometry-functions-distance
   brg-geometry-functions-distance_sqrd
   brg-geometry-functions-area
   brg-geometry-functions-centroid
   brg-geometry-functions-center_of_mass
   brg-geometry-functions-midpoint
   brg-geometry-functions-normal
   brg-geometry-functions-vector_component



intersections
================================================================================



.. toctree::
   :glob:

   brg-geometry-intersections-line_line_intersection
   brg-geometry-intersections-line_line_intersection_2d
   brg-geometry-intersections-lines_intersection
   brg-geometry-intersections-lines_intersection_2d
   brg-geometry-intersections-circle_circle_intersections
   brg-geometry-intersections-circle_circle_intersections_2d



planar
================================================================================



.. toctree::
   :glob:

   brg-geometry-planar-is_ccw
   brg-geometry-planar-is_convex
   brg-geometry-planar-is_intersecting
   brg-geometry-planar-is_selfintersecting
   brg-geometry-planar-is_point_in_polygon
   brg-geometry-planar-is_point_in_triangle
   brg-geometry-planar-closest_part_of_triangle



queries
================================================================================



.. toctree::
   :glob:

   brg-geometry-queries-is_colinear
   brg-geometry-queries-is_coplanar
   brg-geometry-queries-is_coplanar4
   brg-geometry-queries-is_point_on_plane
   brg-geometry-queries-is_point_on_line
   brg-geometry-queries-is_point_on_segment
   brg-geometry-queries-is_point_on_polyline



spatial
================================================================================



.. toctree::
   :glob:

   brg-geometry-spatial-sort_points
   brg-geometry-spatial-closest_point
   brg-geometry-spatial-closest_point_on_line
   brg-geometry-spatial-closest_point_on_segment
   brg-geometry-spatial-closest_point_on_polyline
   brg-geometry-spatial-closest_point_on_plane



transformations
================================================================================



.. toctree::
   :glob:

   brg-geometry-transformations-translate
   brg-geometry-transformations-rotate
   brg-geometry-transformations-normalize
   brg-geometry-transformations-scale
   brg-geometry-transformations-mirror
   brg-geometry-transformations-project



utilities
================================================================================



.. toctree::
   :glob:


