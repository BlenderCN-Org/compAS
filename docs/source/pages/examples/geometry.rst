.. _geometry:

********************************************************************************
Geometry
********************************************************************************

.. contents::

.. normals => 3D plotting
.. crossing edges

.. pull to mesh (i.e. to closest point on mesh)


.. code-block:: python

    import brg

    from brg.datastructures.mesh import Mesh
    from brg.datastructures.network import Network

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    network = Network.from_obj(brg.get_data('lines.obj'))


Edge length
===========

.. code-block:: python

    from brg.geometry import subtract_vectors
    from brg.geometry import length_vector
    from brg.geometry import distance_point_point

    lengths = []

    for u, v in network.edges():
        a = network.vertex_coordinates(u)
        b = network.vertex_coordinates(v)
        l = length_vector(subtract_vectors(b, a))
        # l = distance_point_point(a, b)
        lengths.append(l)

    print lengths
    print [network.edge_length(u, v) for ]
    
    network.plotter.elabel = {(u, v): network.edge_length(u, v) for u, v in network.edges_iter()}
    network.plot()


.. plot::

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('lines.obj'))

    network.plotter.elabel = {(u, v): network.edge_length(u, v) for u, v in network.edges_iter()}
    network.plot()


Edge midpoint
=============

.. code-block:: python

    from brg.geometry import centroid_points
    from brg.geometry import midpoint_line

    midpoints = []

    for u, v in network.edges():
        a = network.vertex_coordinates(u)
        b = network.vertex_coordinates(v)
        # m = centroid_points([a, b])        
        m = midpoint_line(a, b)
        midpoints.append(m)

    print midpoints
    print [network.edge_midpoint(u, v) for u, v in network.edges_iter()]

    network.plotter.points = [{'pos': network.edge_midpoint(u, v), 'text': index} for index, u, v in network.edges_enum()]
    network.plot()


.. plot::

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('lines.obj'))

    network.plotter.vertices_on = False
    network.plotter.points = [{'pos': network.edge_midpoint(u, v), 'text': index} for index, u, v in network.edges_enum()]
    network.plot()


Face centroid
=============

.. code-block:: python

    from brg.geometry import centroid_points

    centroids = []

    for fkey in mesh.face:
        vertices = mesh.faces_vertices(fkey)
        points = [mesh.vertex_coordinates(key) for key in vertices]
        centroid = centroid_points(points)
        centroids.append(centroid)

    print centroids
    print [mesh.face_centroid(fkey) for fkey in mesh.face]

    mesh.plotter.vertices_on = False
    mesh.plotter.points = [{'pos': mesh.face_centroid(fkey), 'text': fkey} for fkey in mesh.face]
    mesh.plot()


.. plot::

    import brg
    from brg.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    mesh.plotter.points = [{'pos': mesh.face_centroid(fkey), 'text': fkey} for fkey in mesh.face]
    mesh.plot()


Vertex area
===========

.. code-block:: python

    from brg.geometry import centroid_points
    from brg.geometry import cross_vectors
    from brg.geometry import length_vector

    areas = []
    fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.face}

    for key in mesh.vertex:
        area = 0
        a = mesh.vertex_coordinates(key)

        for nbr in mesh.vertex_neighbours(key):
            b = self.vertex_coordinates(nbr)
            ab = subtract_vectors(b, a)

            fkey = self.halfedge[key][nbr]

            if fkey:
                c = fkey_centroid[fkey]
                ac = subtract_vectors(c, a)
                area += 0.25 * length_vector(cross_vectors(ab, ac))

            fkey = self.halfedge[nbr][key]

            if fkey:
                d = fkey_centroid[fkey]
                ad = subtract_vectors(d, a)
                area += 0.25 * length_vector(cross_vectors(ab, ad))

        areas.append(area)

    print areas

.. code-block:: python

    print [mesh.vertex_area(key) for key in mesh.vertex]


.. code-block:: python

    mesh.plotter.vlabel = {key: '{0:.1f}'.format(mesh.vertex_area(key)) for key in mesh}
    mesh.plot()


.. plot::

    import brg
    from brg.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    mesh.plotter.vlabel = {key: '{0:.1f}'.format(mesh.vertex_area(key)) for key in mesh}
    mesh.plot()


Crossing edges
==============

.. code-block:: python

    # prrt
