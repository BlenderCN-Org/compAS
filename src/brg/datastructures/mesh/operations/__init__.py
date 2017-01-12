"""This package defines basic operations on meshes.

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

"""

docs = [
    {'quad'     : []},
    {'tri'      : []},
    {'cycling'  : ['cycle_face', ]},
    {'insert'   : ['insert_edge', ]},
    {'split'    : ['split_edge', 'split_face', ]},
    {'welding'  : ['unweld', ]}
]
