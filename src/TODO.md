# brg: ToDo list

## Naming

- construct_dual_mesh != construct_network_dual


## Reorganization

- move spatial into datastructures
- move drawing functionality (matplotlib) to viewers packages
- viewer2 vs. viewer3
- add geometry2
- reorganize the mesh package:
    * mesh.poly.poly
    * mesh.poly.algorithms
    * mesh.poly.helpers
    * mesh.quad.quad
    * mesh.quad.algorithms
    * mesh.quad.helpers
    * mesh.tri.tri
    * mesh.tri.algorithms
    * mesh.tri.helpers
    * mesh.utilities (join, weld, cut, cull, ...)


## Miscellaneous

- use mesh as base for formdiagram?
- general network vs. "facenetwork"
- use "dualdata" *object* for storing face data
- ordering of vertex neighbours (cw vs. ccw)
- ordered vs ordering
- ordering dependent on global datastructure parameter (?)


