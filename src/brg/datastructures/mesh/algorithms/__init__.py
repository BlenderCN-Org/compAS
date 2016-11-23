"""Package for general mesh algorithms.

Algorithms have a global effect on the topology and/or geometry of the mesh.

Algorithms specifically designed for triangle or quad meshes can be found in the
subpackages `tri` and `quad`.

"""

docs = [
    {'quad'          : []},
    {'tri'           : []},
    {'duality'       : ['construct_dual_mesh', ]},
    {'geometry'      : ['mesh_contours', 'mesh_isolines', 'mesh_gradient', 'mesh_curvature', ]},
    {'orientation'   : ['mesh_unify_cycle_directions', 'mesh_flip_cycle_directions', ]},
    {'smoothing'     : ['mesh_smooth_centroid', 'mesh_smooth_centerofmass', 'mesh_smooth_length', 'mesh_smooth_area', ]},
    {'subdivision'   : ['subdivide', 'subdivided', 'tri_subdivision', 'corner_subdivision', 'quad_subdivision', 'catmullclark_subdivision', 'doosabin_subdivision', ]},
    {'triangulation' : ['delaunay_from_mesh', 'delaunay_from_points', ]}
]
