
.. brg.datastructures.mesh.algorithms:

********************************************************************************
brg.datastructures.mesh.algorithms
********************************************************************************

Package for general mesh algorithms.

Algorithms have a global effect on the topology and/or geometry of the mesh.

Algorithms specifically designed for triangle or quad meshes can be found in the
subpackages `tri` and `quad`.





.. rubric:: **Packages**

.. toctree::
   :glob:
   :maxdepth: 1

   brg-datastructures-mesh-algorithms-quad
   brg-datastructures-mesh-algorithms-tri

.. rubric:: Modules

* `duality`_
* `geometry`_
* `orientation`_
* `smoothing`_
* `subdivision`_
* `triangulation`_

-------


duality
================================================================================



.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-duality-construct_dual_mesh



geometry
================================================================================

brg.datastructures.mesh.algorithms.geometry: Compute geometric properties of a mesh.

.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-geometry-mesh_planarize
   brg-datastructures-mesh-algorithms-geometry-mesh_circularize



orientation
================================================================================

brg.datastructures.mesh.algorithms.orientation: Algorithms related to mesh orientation and orientability.

.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-orientation-mesh_unify_cycle_directions
   brg-datastructures-mesh-algorithms-orientation-mesh_flip_cycle_directions



smoothing
================================================================================



.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-smoothing-mesh_smooth_centroid
   brg-datastructures-mesh-algorithms-smoothing-mesh_smooth_centerofmass
   brg-datastructures-mesh-algorithms-smoothing-mesh_smooth_length
   brg-datastructures-mesh-algorithms-smoothing-mesh_smooth_area



subdivision
================================================================================



.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-subdivision-subdivide
   brg-datastructures-mesh-algorithms-subdivision-subdivided
   brg-datastructures-mesh-algorithms-subdivision-tri_subdivision
   brg-datastructures-mesh-algorithms-subdivision-corner_subdivision
   brg-datastructures-mesh-algorithms-subdivision-quad_subdivision
   brg-datastructures-mesh-algorithms-subdivision-catmullclark_subdivision
   brg-datastructures-mesh-algorithms-subdivision-doosabin_subdivision



triangulation
================================================================================

This module defines algorithms for generating triangulations.

.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-triangulation-delaunay_from_mesh
   brg-datastructures-mesh-algorithms-triangulation-delaunay_from_points

