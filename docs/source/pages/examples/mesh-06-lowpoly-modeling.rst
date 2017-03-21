.. _examples_mesh-lowpoly-modeling:

********************************************************************************
Mesh low-poly modeling
********************************************************************************

.. _examples_mesh-control-skeleton-subdivision:

********************************************************************************
Smooth, 3D-printable meshes from a spatial network
********************************************************************************

.. image:: /_images/examples_mesh-control-skeleton-subdivision.*

:download:`geometry.3dm </_downloads/examples_mesh-control-skeleton-subdivision.3dm>`.

The following code computes a solidified smooth mesh from a spatial network of lines.
The shown method yields similar results as the exoskeleton plugin for Grasshopper 
to create meshes for 3D printing.

.. literalinclude:: /../../examples/examples_mesh-control-skeleton-subdivision.py
 
.. _notes:

    The simple implementation shown does not include angle checks between edges 
    meeting in one node. Hence, depending on the diameter of the cross section of 
    the "tubes", the location of the "inner cross sections" and the angles, the 
    code might produce incompatible convex hull geometries and therefore 
    degenerate subdivision meshes.  
 
 
.. seealso::

    * :func:`compas.geometry._convex_hull.convex_hull`
    * :func:`compas.datastructures.mesh.algorithms.subdivide_mesh_catmullclark`
    

