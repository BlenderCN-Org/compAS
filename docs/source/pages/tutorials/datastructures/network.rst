.. _network:

********************************************************************************
Network
********************************************************************************

* :mod:`brg.datastructures.network`
* :class:`brg.datastructures.network.Network`


The ``Network`` is an edge graph. It is suited for describing general networks
of connected nodes or vertices, both planar and non-planar. It is
*edge-oriented*, but provides support for face topology if the network is planar.


Structure of the data
=====================

.. code-block:: python

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('lines.obj'))

    # structure of the vertex dict

    for key in network.vertex:
        print key, network.vertex[key]

    # structure of the edge dict

    for u in network.edge:
        for v in network.edge[u]:
            print u, v, network.edge[u][v]

    # structure of the halfedge dict

    for u in network.halfedge:
        for v in network.halfedge[u]:
            f1 = network.halfedge[u][v]
            f2 = network.halfedge[v][u]
            if f1 is not None:
                print network.face[f1]
            if f2 is not None:
                print network.face[f2]

    # structure of the face dict

    for fkey in network.face:
        print fkey, network.face[fkey]

    # structure of the facedata dict


Create a network
================

.. plot::
    :include-source:

    from brg.datastructures.network import Network

    network = Network()

    a = network.add_vertex()
    b = network.add_vertex('5', x=1.0, y=0.0)
    c = network.add_vertex('1', attr_dict={'y': 1.0})
    d = network.add_vertex(x=-1.0)
    e = network.add_vertex(key='e', attr_dict={'y': 3.0}, y=-1.0)

    network.add_edge(a, b)
    network.add_edge(a, c)
    network.add_edge(a, d)
    network.add_edge(a, e)

    network.plot(
        vsize=0.05,
        vlabel={key: key for key in network},
        elabel={(u, v): '{0}-{1}'.format(u, v) for u, v in network.edges()}
    )


.. important::

    As exemplified above, the vertex keys do not necessarily form a continuous
    sequence. There can be gaps as the result of the user intentionally skipping
    certain values, or as a result of vertices being removed. For example,
    several algorithms and operations add and remove keys as part of their
    internal procedure. Gaps are not filled up, unless this is done manually by
    the user. The automatic assignment of keys simply continues to increment the
    next available value.

    In general, unless for good reason, the assignment of keys should be left to
    the ``add_xxx`` functions and the constructors. In almost all cases it is
    irrelevant what the keys actually are. An exception to this rule is, for
    example, the creation of a dual. In which case, ideally, the faces of the one
    correspond to the vertices of the other, and vice versa.


.. warning::

    Currently, all keys are converted to their string representation before they
    are added to the respective dictionaries. This will change in future version,
    whwere all hashable types will be accepted.


Constructors
============

.. code-block:: python
    
    from brg.datastructures.network import Network

    vertices = [[0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [-1.0, 0.0, 0.0],
                [0.0, -1.0, 0.0]]

    edges = [(0, 1), (0, 2), (0, 3), (0, 4)]

    network = Network.from_vertices_and_edges(vertices, edges)


.. plot::
    :include-source:

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    network.plot(
        vsize=0.2,
        vlabel={key: key for key in network}
    )


.. important::

    Always use the ``.add_xxx`` functions or one of the constructors to create
    a network (or mesh, or volmesh). Using these functions ensures that the
    topological relations are properly set up.


Accessors
=========

.. code-block:: python

    # lists

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    print network.vertices()
    print network.vertices(data=True)

    print network.edges()
    print network.edges(data=True)


.. code-block:: python

    # iterators

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    for key in network.vertices_iter():
        print key

    for key, attr in network.vertices_iter(True):
        print key, attr

    for u, v in network.edges_iter():
        print u, v

    for u, v, attr in network.edges_iter(True):
        print u, v, attr


.. code-block:: python

    # enumerators

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    for index, key in network.vertices_enum():
        print index, key

    for index, key, attr in network.vertices_enum(True):
        print index, key, attr

    for index, u, v in network.edges_enum():
        print index, u, v

    for index, u, v, attr in network.edges_enum(True):
        print index, u, v, attr


Attributes
==========

.. code-block:: python

    network.set_vertex_attribute(a, 'color', (255, 0, 0))

    # network.vertex[a]['color'] = (255, 0, 0)

    network.set_vertices_attribute('color', (255, 0, 0))

    # for key, attr in network.vertices_iter(True):
    #     attr['color'] = (255, 0, 0) 

    network.set_edge_attribute(a, b, 'color', (0, 255, 0))

    # network.edge[a][b]['color'] = (0, 255, 0)

    network.set_edges_attribute('color', (0, 255, 0))

    # for u, v, attr in network.edges_iter(True):
    #     attr['color'] = (0, 255, 0)


.. rubric:: Exercise

Randomly assign one of the following colors to each of the vertices of the network
described in ``'grid_irregular.obj'``. Then plot the network with these colors.


.. plot::
    :include-source:
    
    import random
    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    for key, attr in network.vertices_iter(True):
        attr['color'] = random.choice(colors)

    network.plot(
        vsize=0.2,
        vcolor={key: attr['color'] for key, attr in network.vertices_iter(True)}
    )


Topology
========

.. plot::
    :include-source:

    # adjacency

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    vertices = network.neighbours(0) + [0]

    network.plot(
        vsize=0.2,
        vlabel={key: key for key in vertices},
        vcolor={key: (255, 0, 0) for key in vertices},
        ecolor={(u, v): (0, 255, 0) for u, v in network.connected_edges(0)}
    )


.. plot::
    :include-source:

    # degree

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    network.plot(
        vsize=0.2,
        vlabel={key: network.degree(key) for key in network}
    )    


.. rubric:: Exercise

Find all the leaves of the network in the sample file ``'grid_irregular.obj'``.
Leaves are vertices with only one neighbour.
Print the keys of these vertices and give them a different color in a plot.


Customisation
=============

.. code-block:: python

    import brg_rhino
   
    class Cablenet(Network):
       
        def __init__(self):
            super(Cablenet, self).__init__()
            self.dva.update({
                'rx': 0.0,
                'ry': 0.0,
                'rz': 0.0
            })
            self.dea.update({
                'q': 0.0,
                'f': 0.0,
                'l': 0.0
            })

        @property
        def xyz(self):
            return [self.vertex_coordinates(key) for key in self]

        @property
        def q(self):
            return [attr['q'] for u, v, attr in self.edges_iter(True)]

        def draw(self):
            brg_rhino.draw_network(self)

