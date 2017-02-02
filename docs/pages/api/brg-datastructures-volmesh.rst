
.. brg.datastructures.volmesh:

********************************************************************************
brg.datastructures.volmesh
********************************************************************************

<...docstring missing...>



.. rubric:: **Packages**

.. toctree::
   :glob:
   :maxdepth: 1

   brg-datastructures-volmesh-algorithms
   brg-datastructures-volmesh-numerical
   brg-datastructures-volmesh-operations
   brg-datastructures-volmesh-utilities

.. rubric:: Modules

* `volmesh`_
* `viewer`_

-------


volmesh
================================================================================

This module defines the base class for cellular meshes.

The implementation of the base class is based on the notion of *x-maps* [xmaps]_
and the concepts behind the *OpenVolumeMesh* library [ovm]_. In short, we add an
additional entity compared to polygonal meshes, the *cell*, and relate cells not
through *half-edges*, but *half-planes*.



.. toctree::
   :glob:

   brg-datastructures-volmesh-volmesh-VolMesh



viewer
================================================================================



.. toctree::
   :glob:

   brg-datastructures-volmesh-viewer-VolMeshViewer

