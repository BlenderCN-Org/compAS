.. _applications:

********************************************************************************
Applications
********************************************************************************

.. contents::

.. cablenet constrained smoothing
.. cablenet equilibrium

.. brg_ags as scripts?


All Rhino examples are based on the following Rhino model :download:`geometry.3dm </_downloads/geometry_tests.3dm>`.


.. code-block:: python

    import rhinoscriptsyntax as rs
    from brg.datastructures.mesh.algorithms.triangulation import delaunay_from_points

    objs = rs.GetObjects("Select Points",1)
    pts = [rs.PointCoordinates(obj) for obj in objs]

    faces = delaunay_from_points(pts)
    rs.AddMesh(pts,faces)
