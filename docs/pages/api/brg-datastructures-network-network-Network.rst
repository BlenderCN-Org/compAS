
********************************************************************************
Network
********************************************************************************

.. autoclass:: brg.datastructures.network.network.Network

   .. rst-class:: class-section
   .. rubric:: **Class attributes**

   .. rst-class:: class-section
   .. rubric:: **Class methods**

   .. automethod:: brg.datastructures.network.network.Network.from_data
   .. automethod:: brg.datastructures.network.network.Network.from_json
   .. automethod:: brg.datastructures.network.network.Network.from_lines
   .. automethod:: brg.datastructures.network.network.Network.from_obj
   .. automethod:: brg.datastructures.network.network.Network.from_vertices_and_edges
   .. rst-class:: class-section
   .. rubric:: **Descriptors**

   .. autoattribute:: brg.datastructures.network.network.Network.color
   .. autoattribute:: brg.datastructures.network.network.Network.data
   .. autoattribute:: brg.datastructures.network.network.Network.name
   .. rst-class:: class-section
   .. rubric:: **Magic methods**

   .. automethod:: brg.datastructures.network.network.Network.__contains__
   .. automethod:: brg.datastructures.network.network.Network.__getitem__
   .. automethod:: brg.datastructures.network.network.Network.__iter__
   .. automethod:: brg.datastructures.network.network.Network.__len__
   .. rst-class:: class-section
   .. rubric:: **Methods**

   .. automethod:: brg.datastructures.network.network.Network._vertex_area
   .. automethod:: brg.datastructures.network.network.Network.add_edge
   .. automethod:: brg.datastructures.network.network.Network.add_face
   .. automethod:: brg.datastructures.network.network.Network.add_vertex
   .. automethod:: brg.datastructures.network.network.Network.boundary_edges
   .. automethod:: brg.datastructures.network.network.Network.boundary_faces
   .. automethod:: brg.datastructures.network.network.Network.boundary_vertices
   .. automethod:: brg.datastructures.network.network.Network.breakpoints
   .. automethod:: brg.datastructures.network.network.Network.degree
   .. automethod:: brg.datastructures.network.network.Network.degree_in
   .. automethod:: brg.datastructures.network.network.Network.degree_out
   .. automethod:: brg.datastructures.network.network.Network.edge_coordinates
   .. automethod:: brg.datastructures.network.network.Network.edge_length
   .. automethod:: brg.datastructures.network.network.Network.edge_midpoint
   .. automethod:: brg.datastructures.network.network.Network.edge_name
   .. automethod:: brg.datastructures.network.network.Network.edge_vector
   .. automethod:: brg.datastructures.network.network.Network.edges
   .. automethod:: brg.datastructures.network.network.Network.edges_enum
   .. automethod:: brg.datastructures.network.network.Network.edges_iter
   .. automethod:: brg.datastructures.network.network.Network.face_adjacency
   .. automethod:: brg.datastructures.network.network.Network.face_ancestor
   .. automethod:: brg.datastructures.network.network.Network.face_area
   .. automethod:: brg.datastructures.network.network.Network.face_center
   .. automethod:: brg.datastructures.network.network.Network.face_centroid
   .. automethod:: brg.datastructures.network.network.Network.face_descendant
   .. automethod:: brg.datastructures.network.network.Network.face_edges
   .. automethod:: brg.datastructures.network.network.Network.face_name
   .. automethod:: brg.datastructures.network.network.Network.face_tree
   .. automethod:: brg.datastructures.network.network.Network.face_vertices
   .. automethod:: brg.datastructures.network.network.Network.faces
   .. automethod:: brg.datastructures.network.network.Network.faces_iter
   .. automethod:: brg.datastructures.network.network.Network.get_edge_attribute
   .. automethod:: brg.datastructures.network.network.Network.get_edges_attribute
   .. automethod:: brg.datastructures.network.network.Network.get_edges_attributes
   .. automethod:: brg.datastructures.network.network.Network.get_face_attribute
   .. automethod:: brg.datastructures.network.network.Network.get_faces_attribute
   .. automethod:: brg.datastructures.network.network.Network.get_faces_attributes
   .. automethod:: brg.datastructures.network.network.Network.get_vertex_attribute
   .. automethod:: brg.datastructures.network.network.Network.get_vertices_attribute
   .. automethod:: brg.datastructures.network.network.Network.get_vertices_attributes
   .. automethod:: brg.datastructures.network.network.Network.has_edge
   .. automethod:: brg.datastructures.network.network.Network.has_vertex
   .. automethod:: brg.datastructures.network.network.Network.index_key
   .. automethod:: brg.datastructures.network.network.Network.index_uv
   .. automethod:: brg.datastructures.network.network.Network.is_vertex_leaf
   .. automethod:: brg.datastructures.network.network.Network.key_index
   .. automethod:: brg.datastructures.network.network.Network.leaves
   .. automethod:: brg.datastructures.network.network.Network.neighbours
   .. automethod:: brg.datastructures.network.network.Network.neighbours_in
   .. automethod:: brg.datastructures.network.network.Network.neighbours_out
   .. automethod:: brg.datastructures.network.network.Network.plot
   .. automethod:: brg.datastructures.network.network.Network.plot3
   .. automethod:: brg.datastructures.network.network.Network.set_dea
   .. automethod:: brg.datastructures.network.network.Network.set_dfa
   .. automethod:: brg.datastructures.network.network.Network.set_dva
   .. automethod:: brg.datastructures.network.network.Network.set_edge_attribute
   .. automethod:: brg.datastructures.network.network.Network.set_edges_attribute
   .. automethod:: brg.datastructures.network.network.Network.set_face_attribute
   .. automethod:: brg.datastructures.network.network.Network.set_faces_attribute
   .. automethod:: brg.datastructures.network.network.Network.set_vertex_attribute
   .. automethod:: brg.datastructures.network.network.Network.set_vertices_attribute
   .. automethod:: brg.datastructures.network.network.Network.to_data
   .. automethod:: brg.datastructures.network.network.Network.to_json
   .. automethod:: brg.datastructures.network.network.Network.to_lines
   .. automethod:: brg.datastructures.network.network.Network.to_obj
   .. automethod:: brg.datastructures.network.network.Network.to_vertices_and_edges
   .. automethod:: brg.datastructures.network.network.Network.uv_index
   .. automethod:: brg.datastructures.network.network.Network.vertex_area
   .. automethod:: brg.datastructures.network.network.Network.vertex_color
   .. automethod:: brg.datastructures.network.network.Network.vertex_coordinates
   .. automethod:: brg.datastructures.network.network.Network.vertex_faces
   .. automethod:: brg.datastructures.network.network.Network.vertex_name
   .. automethod:: brg.datastructures.network.network.Network.vertices
   .. automethod:: brg.datastructures.network.network.Network.vertices_enum
   .. automethod:: brg.datastructures.network.network.Network.vertices_iter
