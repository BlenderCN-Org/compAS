
********************************************************************************
brg.datastructures.mesh.algorithms
********************************************************************************

Package for general mesh algorithms.

Algorithms have a global effect on the topology and/or geometry of the mesh.

Algorithms specifically designed for triangle or quad meshes can be found in the
subpackages `tri` and `quad`.





.. rubric:: **Subpackages**

.. toctree::
   :glob:
   :maxdepth: 1

   brg-datastructures-mesh-algorithms-quad
   brg-datastructures-mesh-algorithms-tri


brg.datastructures.mesh.algorithms.duality
================================================================================

<docstring missing>

.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-duality-construct_dual_mesh



brg.datastructures.mesh.algorithms.geometry
================================================================================

brg.datastructures.mesh.algorithms.geometry: Compute geometric properties of a mesh.

.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-geometry-mesh_contours
   brg-datastructures-mesh-algorithms-geometry-mesh_isolines
   brg-datastructures-mesh-algorithms-geometry-mesh_gradient
   brg-datastructures-mesh-algorithms-geometry-mesh_curvature



brg.datastructures.mesh.algorithms.orientation
================================================================================

brg.datastructures.mesh.algorithms.orientation: Algorithms related to mesh orientation and orientability.

.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-orientation-mesh_unify_cycle_directions
   brg-datastructures-mesh-algorithms-orientation-mesh_flip_cycle_directions



brg.datastructures.mesh.algorithms.smoothing
================================================================================

<docstring missing>

.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-smoothing-mesh_smooth_centroid
   brg-datastructures-mesh-algorithms-smoothing-mesh_smooth_centerofmass
   brg-datastructures-mesh-algorithms-smoothing-mesh_smooth_length
   brg-datastructures-mesh-algorithms-smoothing-mesh_smooth_area



brg.datastructures.mesh.algorithms.subdivision
================================================================================

<docstring missing>

.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-subdivision-subdivide
   brg-datastructures-mesh-algorithms-subdivision-subdivided
   brg-datastructures-mesh-algorithms-subdivision-tri_subdivision
   brg-datastructures-mesh-algorithms-subdivision-corner_subdivision
   brg-datastructures-mesh-algorithms-subdivision-quad_subdivision
   brg-datastructures-mesh-algorithms-subdivision-catmullclark_subdivision
   brg-datastructures-mesh-algorithms-subdivision-doosabin_subdivision



brg.datastructures.mesh.algorithms.triangulation
================================================================================

This module defines algorithms for generating triangulations.

.. toctree::
   :glob:

   brg-datastructures-mesh-algorithms-triangulation-delaunay_from_mesh
   brg-datastructures-mesh-algorithms-triangulation-delaunay_from_points

