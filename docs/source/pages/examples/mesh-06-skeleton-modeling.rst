.. _examples_mesh-skeleton-modeling:

********************************************************************************
Mesh skeleton modeling: smooth, 3D-printable mesh from a spatial network
********************************************************************************

.. image:: /_images/examples_mesh-control-skeleton-subdivision.*


The following code computes a solidified smooth mesh from a spatial network of lines.
The shown method yields similar results as the exoskeleton plugin for Grasshopper 
to create meshes for 3D printing.


:download:`geometry.3dm </_downloads/examples_mesh-control-skeleton-subdivision.3dm>`


.. literalinclude:: /../../examples/examples_mesh-control-skeleton-subdivision.py

 
.. note::

    The simple implementation shown does not include angle checks between edges 
    meeting in one node. Hence, depending on the diameter of the cross section of 
    the "tubes", the location of the "inner cross sections" and the angles, the 
    code might produce incompatible convex hull geometries and therefore 
    degenerate subdivision meshes.  
 
 
.. seealso::

    * :func:`compas.geometry._convex_hull.convex_hull`
    * :func:`compas.datastructures.mesh.algorithms.subdivide_mesh_catmullclark`
    

