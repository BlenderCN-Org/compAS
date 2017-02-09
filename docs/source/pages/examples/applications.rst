.. _applications:

********************************************************************************
Applications
********************************************************************************

.. contents::

.. brg_ags as scripts?


Equilibrium of a cablenet
=========================

.. split up and add images

.. code-block:: python

    import brg
    from brg.datastructures.network import network

    import brg_rhino as rhino

    # create layers

    layers = {'Cablenet': {}}

    rhino.create_layers(layers)

    # make a network

    network = Network.from_obj(brg.get_data('lines.obj'))

    # set default attributes

    network.set_dva({'px': 0.0, 'py': 0.0, 'pz': 0.0, 'is_fixed': False})
    network.set_dea({'q': 0.0, 'f': 0.0, 'l': 0.0})

    rhino.draw_network(
        network,
        layer='Cablenet',
        vertexcolor={k: '#ff0000' for k, a in network.vertices_iter(True) if a['is_fixed']},
        edgecolor='#666666'
    )

    # update vertex attributes

    while True:
        keys = rhino.select_network_vertices(network)

        if not keys:
            break

        if rhino.update_network_vertex_attributes(network, keys):
            rhino.draw_network(network)
        else:
            break

    # update edge attributes

    while True:
        keys = rhino.select_network_edges(network)

        if not keys:
            break

        if not rhino.update_network_edge_attributes(network, keys, names=['q']):
            break

    # compute equilibrium

    # display forces



Mesh modeling in Rhino
======================

All Rhino examples in this section are based on the following Rhino model
:download:`geometry.3dm </_downloads/geometry_tests.3dm>`.


.. code-block:: python

    import rhinoscriptsyntax as rs
    from brg.datastructures.mesh.algorithms.triangulation import delaunay_from_points

    objs = rs.GetObjects("Select Points",1)
    pts = [rs.PointCoordinates(obj) for obj in objs]

    faces = delaunay_from_points(pts)
    rs.AddMesh(pts,faces)


.. image:: /_images/imagetest.*


Algebraic Graph Statics
=======================

...
