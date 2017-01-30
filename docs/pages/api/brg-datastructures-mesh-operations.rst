
.. brg.datastructures.mesh.operations:

********************************************************************************
brg.datastructures.mesh.operations
********************************************************************************

This package defines basic operations on meshes.

A mesh modification is considered an operation (as opposed to an algorithm)
if its effect is local. Examples of mesh modifications that are operations are:

- splitting an edge
- flipping an edge
- inserting a vertex
- ...

Mesh functions that don't modify the mesh are also considered operations.
Examples are:

- cycling a face
- ...





.. rubric:: **Packages**

.. toctree::
   :glob:
   :maxdepth: 1

   brg-datastructures-mesh-operations-quad
   brg-datastructures-mesh-operations-tri

.. rubric:: Modules

* `cycling`_
* `insert`_
* `split`_
* `welding`_

-------


cycling
================================================================================



.. toctree::
   :glob:

   brg-datastructures-mesh-operations-cycling-cycle_face



insert
================================================================================



.. toctree::
   :glob:

   brg-datastructures-mesh-operations-insert-insert_edge



split
================================================================================



.. toctree::
   :glob:

   brg-datastructures-mesh-operations-split-split_edge
   brg-datastructures-mesh-operations-split-split_face



welding
================================================================================



.. toctree::
   :glob:

   brg-datastructures-mesh-operations-welding-unweld

