.. _network-algorithms:

********************************************************************************
Network algorithms
********************************************************************************

:mod:`brg.datastructures.network.algorithms`


.. contents::


Shortest paths
==============

.. plot::
    :include-source:

    # shortest path
    # when not all edge weights are the same
    # => use Dijkstra algorithm

    import brg

    from brg.datastructures.network import Network
    from brg.datastructures.network.algorithms import network_dijkstra_path

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    weight = dict(((u, v), network.edge_length(u, v)) for u, v in network.edges())
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    start = 21
    end = 22

    path = network_dijkstra_path(network.adjacency, weight, start, end)

    edges = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if v not in network.edge[u]:
            u, v = v, u
        edges.append([u, v])

    network.plot(
        vlabel={key: key for key in (start, end)},
        vcolor={key: (255, 0, 0) for key in (path[0], path[-1])},
        vsize=0.15,
        ecolor={(u, v): (255, 0, 0) for u, v in edges},
        ewidth={(u, v): 2.0 for u, v in edges},
        elabel={(u, v): '{:.1f}'.format(weight[(u, v)]) for u, v in network.edges()}
    )


Dual networks
=============

.. plot::
    :include-source:

    # find faces
    # and construct the dual

    import brg

    from brg.datastructures.network import Network
    from brg.datastructures.network.algorithms import find_network_faces
    from brg.datastructures.network.algorithms import construct_dual_network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    find_network_faces(network, network.leaves())

    dual = construct_dual_network(network)

    dual.plot()


Edge parallelisation
====================

...


Vertex coloring
===============

...


Smoothing
=========

...
