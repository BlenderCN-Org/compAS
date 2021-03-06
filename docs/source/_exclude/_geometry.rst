.. _geometry:

********************************************************************************
Geometry
********************************************************************************

* :mod:`compas.geometry`


.. raytracing?
.. polyhedral stuff?
.. bestfit intersection
.. bestfit plane
.. bestfit ...?
.. perpendicularisation
.. jiggle?
.. parallelisation
.. planarisation
.. is_convex?
.. closest point ...


.. contents::


Edge length
===========

.. code-block:: python

    import compas
    from compas.datastructures.network import Network
    from compas.geometry import distance_point_point

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    lengths = []

    for u, v in network.edges():
        a = network.vertex_coordinates(u)
        b = network.vertex_coordinates(v)
        l = distance_point_point(a, b)
        lengths.append(l)


.. plot::
    :include-source:

    import compas
    from compas.datastructures.network import Network

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    network.plot(
        vsize=0.05,
        elabel={(u, v): '%.1f' % network.edge_length(u, v) for u, v in network.edges_iter()}
    )


Face centroid
=============

.. code-block:: python

    import compas
    from compas.datastructures.mesh import Mesh
    from compas.geometry import centroid_points

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    centroids = []

    for fkey in mesh.face:
        vertices = mesh.faces_vertices(fkey)
        points = [mesh.vertex_coordinates(key) for key in vertices]
        c = centroid_points(points)
        centroids.append(c)


.. plot::
    :include-source:

    import compas
    from compas.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    mesh.plot(
        vsize=0.05,
        points=[{'pos': mesh.face_centroid(fkey), 'text': fkey, 'size': 0.2} for fkey in mesh.face]
    )


Vertex area
===========

.. code-block:: python

    # areas = [mesh.vertex_area(key) for key in mesh.vertex]

    from compas.geometry import centroid_points
    from compas.geometry import cross_vectors
    from compas.geometry import length_vector

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

    import compas
    from compas.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    mesh.plotter.vsize = 0.2
    mesh.plotter.vlabel = {key: '{0:.1f}'.format(mesh.vertex_area(key)) for key in mesh}
    mesh.plot()

