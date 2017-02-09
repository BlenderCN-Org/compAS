.. _geometry:

********************************************************************************
Geometry
********************************************************************************

.. contents::


Edge length
===========

.. code-block:: python

    # lengths = [network.edge_length(u, v) for u, v in network.edges()]

    import brg
    from brg.datastructures.network import Network
    from brg.geometry import distance_point_point

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    lengths = []

    for u, v in network.edges():
        a = network.vertex_coordinates(u)
        b = network.vertex_coordinates(v)
        l = distance_point_point(a, b)
        lengths.append(l)


.. code-block:: python

    network.plotter.vsize = 0.05
    network.plotter.elabel = {(u, v): '%.1f' % network.edge_length(u, v) for u, v in network.edges_iter()}
    network.plot()


.. plot::

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    network.plotter.vsize = 0.05
    network.plotter.elabel = {(u, v): '%.1f' % network.edge_length(u, v) for u, v in network.edges_iter()}
    network.plot()


Edge midpoint
=============

.. code-block:: python

    # midpoints [network.edge_midpoint(u, v) for u, v in network.edges()]

    import brg
    from brg.datastructures.network import Network
    from brg.geometry import midpoint_line

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    midpoints = []

    for u, v in network.edges():
        a = network.vertex_coordinates(u)
        b = network.vertex_coordinates(v)
        m = midpoint_line(a, b)
        midpoints.append(m)


.. code-block:: python
    
    network.plotter.vsize = 0.05
    network.plotter.vertices_on = True
    network.plotter.points = [{'pos': network.edge_midpoint(u, v), 'text': str(index), 'size': 0.2, 'facecolor': '#eeeeee'} for index, u, v in network.edges_enum()]
    network.plot()


.. plot::

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    network.plotter.vsize = 0.05
    network.plotter.vertices_on = True
    network.plotter.points = [{'pos': network.edge_midpoint(u, v), 'text': str(index), 'size': 0.2, 'facecolor': '#eeeeee'} for index, u, v in network.edges_enum()]
    network.plot()


Face centroid
=============

.. code-block:: python

    # centroids = [mesh.face_centroid(fkey) for fkey in mesh.face]

    import brg
    from brg.datastructures.mesh import Mesh
    from brg.geometry import centroid_points

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    centroids = []

    for fkey in mesh.face:
        vertices = mesh.faces_vertices(fkey)
        points = [mesh.vertex_coordinates(key) for key in vertices]
        c = centroid_points(points)
        centroids.append(c)


.. code-block:: python

    mesh.plotter.vsize = 0.05
    mesh.plotter.points = [{'pos': mesh.face_centroid(fkey), 'text': fkey, 'size': 0.2} for fkey in mesh.face]
    mesh.plot()


.. plot::

    import brg
    from brg.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    mesh.plotter.vsize = 0.05
    mesh.plotter.points = [{'pos': mesh.face_centroid(fkey), 'text': fkey, 'size': 0.2} for fkey in mesh.face]
    mesh.plot()


Vertex area
===========

.. code-block:: python

    # areas = [mesh.vertex_area(key) for key in mesh.vertex]

    from brg.geometry import centroid_points
    from brg.geometry import cross_vectors
    from brg.geometry import length_vector

    fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.face}

    areas = []

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


.. code-block:: python
    
    mesh.plotter.vsize = 0.2
    mesh.plotter.vlabel = {key: '%.1f' % mesh.vertex_area(key) for key in mesh}
    mesh.plot()


.. plot::

    import brg
    from brg.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    mesh.plotter.vsize = 0.2
    mesh.plotter.vlabel = {key: '{0:.1f}'.format(mesh.vertex_area(key)) for key in mesh}
    mesh.plot()

