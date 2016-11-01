"""Package for general mesh algorithms.

Algorithms have a global effect on the topology and/or geometry of the mesh.

Algorithms specifically designed for triangle or quad meshes can be found in the
subpackages `tri` and `quad`.

"""

docs = [
    {'duality'     : ['construct_dual_mesh', ]},
    {'geometry'    : []},
    {'orientation' : ['mesh_unify_cycle_directions', 'mesh_flip_cycle_directions', ]},
    {'smoothing'   : ['mesh_smooth', ]},
    {'subdivision' : ['subdivide', 'subdivided', 'tri_subdivision', 'corner_subdivision', 'quad_subdivision', 'catmullclark_subdivision']}
]
