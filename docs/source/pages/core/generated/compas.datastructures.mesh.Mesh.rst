Mesh
===============================

.. currentmodule:: compas.datastructures.mesh

.. autoclass:: Mesh

   
   
   .. rubric:: Methods

   .. autosummary::
   
      ~Mesh.__init__
      ~Mesh.add_face
      ~Mesh.add_faces
      ~Mesh.add_vertex
      ~Mesh.add_vertices
      ~Mesh.clear
      ~Mesh.copy
      ~Mesh.cull_unused_edges
      ~Mesh.cull_unused_vertices
      ~Mesh.delete_face
      ~Mesh.delete_vertex
      ~Mesh.edge_length
      ~Mesh.edge_midpoint
      ~Mesh.edge_vector
      ~Mesh.edges
      ~Mesh.edges_enum
      ~Mesh.edges_iter
      ~Mesh.edges_on_boundary
      ~Mesh.face_adjacency
      ~Mesh.face_area
      ~Mesh.face_center
      ~Mesh.face_centroid
      ~Mesh.face_coordinates
      ~Mesh.face_neighbourhood
      ~Mesh.face_neighbours
      ~Mesh.face_normal
      ~Mesh.face_tree
      ~Mesh.face_vertex_neighbours
      ~Mesh.face_vertices
      ~Mesh.faces
      ~Mesh.faces_enum
      ~Mesh.faces_iter
      ~Mesh.faces_on_boundary
      ~Mesh.from_data
      ~Mesh.from_dxf
      ~Mesh.from_json
      ~Mesh.from_lines
      ~Mesh.from_obj
      ~Mesh.from_stl
      ~Mesh.from_vertices_and_faces
      ~Mesh.get_any_face
      ~Mesh.get_any_face_vertex
      ~Mesh.get_any_vertex
      ~Mesh.get_edge_attribute
      ~Mesh.get_edge_attributes
      ~Mesh.get_edges_attribute
      ~Mesh.get_edges_attributes
      ~Mesh.get_face_attribute
      ~Mesh.get_face_attributes
      ~Mesh.get_faces_attribute
      ~Mesh.get_faces_attributes
      ~Mesh.get_vertex_attribute
      ~Mesh.get_vertex_attributes
      ~Mesh.get_vertices_attribute
      ~Mesh.get_vertices_attributes
      ~Mesh.has_edge
      ~Mesh.index_key
      ~Mesh.insert_vertex
      ~Mesh.is_closed
      ~Mesh.is_connected
      ~Mesh.is_edge_naked
      ~Mesh.is_manifold
      ~Mesh.is_orientable
      ~Mesh.is_planar
      ~Mesh.is_quadmesh
      ~Mesh.is_regular
      ~Mesh.is_trimesh
      ~Mesh.is_valid
      ~Mesh.is_vertex_connected
      ~Mesh.is_vertex_extraordinary
      ~Mesh.is_vertex_leaf
      ~Mesh.is_vertex_on_boundary
      ~Mesh.is_vertex_orphan
      ~Mesh.key_index
      ~Mesh.plot
      ~Mesh.point_on_edge
      ~Mesh.remove_vertex
      ~Mesh.set_edge_attribute
      ~Mesh.set_edge_attributes
      ~Mesh.set_edges_attribute
      ~Mesh.set_edges_attributes
      ~Mesh.set_face_attribute
      ~Mesh.set_face_attributes
      ~Mesh.set_faces_attribute
      ~Mesh.set_faces_attributes
      ~Mesh.set_vertex_attribute
      ~Mesh.set_vertex_attributes
      ~Mesh.set_vertices_attribute
      ~Mesh.set_vertices_attributes
      ~Mesh.to_data
      ~Mesh.to_json
      ~Mesh.to_lines
      ~Mesh.to_obj
      ~Mesh.to_points
      ~Mesh.to_vertices_and_faces
      ~Mesh.update_default_edge_attributes
      ~Mesh.update_default_face_attributes
      ~Mesh.update_default_vertex_attributes
      ~Mesh.vertex_adjacency
      ~Mesh.vertex_ancestor
      ~Mesh.vertex_area
      ~Mesh.vertex_color
      ~Mesh.vertex_coordinates
      ~Mesh.vertex_cycle
      ~Mesh.vertex_degree
      ~Mesh.vertex_descendant
      ~Mesh.vertex_faces
      ~Mesh.vertex_neighbourhood
      ~Mesh.vertex_neighbours
      ~Mesh.vertex_normal
      ~Mesh.vertices
      ~Mesh.vertices_enum
      ~Mesh.vertices_iter
      ~Mesh.vertices_on_boundary
      ~Mesh.view
   
   

   
   
   .. rubric:: Attributes

   .. autosummary::
   
      ~Mesh.data
      ~Mesh.name
      ~Mesh.plotter
      ~Mesh.x
      ~Mesh.xy
      ~Mesh.xyz
      ~Mesh.y
      ~Mesh.z
   
   