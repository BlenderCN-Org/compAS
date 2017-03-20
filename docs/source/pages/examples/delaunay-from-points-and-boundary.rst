.. _examples_delaunay-from-points-and-boundary:

********************************************************************************
Delaunay Triangulation from Points and Boundary
********************************************************************************

.. image:: /_images/delaunay-from-points-and-boundary.*

:download:`geometry.3dm </_downloads/geometry_tests.3dm>`.

A plain delaunay triangulation will always form a convex boundary and a continuous 
mesh without 'holes'. The following code shows how to include specific boundaries. 

.. literalinclude:: /../../examples/delaunay-from-points-and-boundary.py
 
.. seealso::

    * :func:`brg.datastructures.mesh.algorithms.triangulation.delaunay_from_points`
    * Sloan, S. W. (1987) A fast algorithm for constructing Delaunay triangulations in the plane
