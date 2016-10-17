
********************************************************************************
brg.datastructures.volmesh
********************************************************************************

<docstring missing>



.. rubric:: **Subpackages**

.. toctree::
   :glob:
   :maxdepth: 1

   brg-datastructures-volmesh-algorithms
   brg-datastructures-volmesh-numerical
   brg-datastructures-volmesh-operations


brg.datastructures.volmesh.drawing
================================================================================

<docstring missing>

.. toctree::
   :glob:




brg.datastructures.volmesh.viewer
================================================================================

<docstring missing>

.. toctree::
   :glob:




brg.datastructures.volmesh.volmesh
================================================================================

This module defines the base class for cellular meshes.

The implementation of the base class is based on the notion of `x-maps` [xmaps]_
and the concepts behind the `OpenVolumeMesh` library [ovm]_.

In short, we add an additional entity compared to polygonal meshes, the `cell`,
and relate cells not through `half-edges`, but `half-planes`.

Half-edges only exist unambiguously in the context of faces...


.. rubric:: References

.. [xmaps] Cazier, D. and Kraemer, P. [2010] X-maps: an efficient model for non-manifold modeling, IEEE Interntional Conference on Shape Modeling and Applications 2010.
.. [ovm] `OpenVolumeMesh <http://openvolumemesh.org>`_



.. toctree::
   :glob:

   brg-datastructures-volmesh-volmesh-VolMesh

