
********************************************************************************
Mesh
********************************************************************************

.. autoclass:: brg.datastructures.mesh.mesh.Mesh
   :show-inheritance:

   .. rst-class:: class-section
   .. rubric:: **Class attributes**

   .. rst-class:: class-section
   .. rubric:: **Class methods**

   .. automethod:: brg.datastructures.mesh.mesh.Mesh.from_boundary
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.from_data
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.from_dxf
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.from_json
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.from_obj
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.from_points
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.from_stl
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.from_vertices_and_faces
   .. rst-class:: class-section
   .. rubric:: **Descriptors**

   .. autoattribute:: brg.datastructures.mesh.mesh.Mesh.color
   .. autoattribute:: brg.datastructures.mesh.mesh.Mesh.data
   .. autoattribute:: brg.datastructures.mesh.mesh.Mesh.name
   .. autoattribute:: brg.datastructures.mesh.mesh.Mesh.x
   .. autoattribute:: brg.datastructures.mesh.mesh.Mesh.xy
   .. autoattribute:: brg.datastructures.mesh.mesh.Mesh.xyz
   .. autoattribute:: brg.datastructures.mesh.mesh.Mesh.y
   .. autoattribute:: brg.datastructures.mesh.mesh.Mesh.z
   .. rst-class:: class-section
   .. rubric:: **Magic methods**

   .. automethod:: brg.datastructures.mesh.mesh.Mesh.__contains__
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.__getitem__
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.__iter__
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.__len__
   .. rst-class:: class-section
   .. rubric:: **Methods**

   .. automethod:: brg.datastructures.mesh.mesh.Mesh.add_face
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.add_faces
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.add_vertex
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.add_vertices
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.copy
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.cull_unused_edges
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.cull_unused_vertices
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.draw
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.edge_length
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.edge_midpoint
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.edge_vector
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.edges
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.edges_enum
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.edges_iter
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.edges_on_boundary
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_adjacency
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_area
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_center
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_centroid
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_coordinates
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_neighbourhood
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_neighbours
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_normal
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_tree
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_vertex_neighbours
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.face_vertices
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.faces
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.faces_enum
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.faces_iter
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.faces_on_boundary
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.get_any_face
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.get_any_face_vertex
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.get_any_vertex
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.get_edge_attribute
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.get_face_attribute
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.get_vertex_attribute
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.has_edge
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.index_key
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.insert_vertex
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_closed
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_connected
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_edge_naked
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_manifold
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_orientable
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_planar
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_quadmesh
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_regular
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_trimesh
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_valid
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_vertex_connected
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_vertex_leaf
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_vertex_on_boundary
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.is_vertex_orphan
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.key_index
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.point_on_edge
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.remove_face
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.remove_vertex
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.set_dea
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.set_dfa
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.set_dva
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.set_edge_attribute
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.set_face_attribute
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.set_vertex_attribute
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.to_data
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.to_json
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.to_obj
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.to_quadmesh
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.to_trimesh
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_adjacency
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_ancestor
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_area
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_color
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_coordinates
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_cycle
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_degree
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_descendant
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_faces
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_neighbourhood
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_neighbours
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertex_normal
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertices
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertices_enum
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertices_iter
   .. automethod:: brg.datastructures.mesh.mesh.Mesh.vertices_on_boundary
