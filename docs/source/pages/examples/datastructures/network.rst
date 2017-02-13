.. _network:

********************************************************************************
Network
********************************************************************************

* :mod:`brg.datastructures.network`
* :class:`brg.datastructures.network.Network`


The ``Network`` is an edge graph. It is suited for describing general networks
of connected nodes or vertices, both planar and non-planar. It is
*edge-oriented*, but provides support for face topology if the network is planar.


Create a network
================

.. code-block:: python

    from brg.datastructures.network import Network

    network = Network()

    a = network.add_vertex()
    b = network.add_vertex('5', x=1.0, y=0.0)
    c = network.add_vertex('1', attr_dict('y': 1.0))
    d = network.add_vertex(x=-1.0)
    e = network.add_vertex(key='e', attr_dict={'y': 3.0}, y=-1.0)
    
    network.add_edge(a, b)
    network.add_edge(a, c)
    network.add_edge(a, d)
    network.add_edge(a, e)

    network.plotter.vlabel = {key: key for key in network}
    network.plottet.elabel = {(u, v): '{0}-{1}'.format(u, v) for u, v in network.edges()}
    network.plot()


.. plot::

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

    network.plotter.vsize = 0.05
    network.plotter.vlabel = {key: key for key in network}
    network.plotter.elabel = {(u, v): '{0}-{1}'.format(u, v) for u, v in network.edges()}
    network.plot()


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


.. code-block:: python
    
    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    network.plotter.vsize = 0.2
    network.plotter.vlabel = {key: key for key in network}
    network.plot()


.. plot::

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    network.plotter.vsize = 0.2
    network.plotter.vlabel = {key: key for key in network}
    network.plot()


.. important::

    Always use the ``.add_xxx`` functions or one of the constructors to create
    a network (or mesh, or volmesh). Using these functions ensures that the
    topological relations are properly set up.


Topology
========

.. code-block:: python

    # adjacency


.. code-block:: python

    # adjacency

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    vlabel = {key: key for key in network.neighbours('0')}
    vlabel['0'] = '0'

    vcolor = {key: (255, 0, 0) for key in vlabel}

    network.plotter.vsize = 0.2
    network.plotter.vlabel = vlabel
    network.plotter.vcolor = vcolor
    network.plotter.ecolor = {(u, v): (0, 255, 0) for u, v in network.connected_edges('0')}
    network.plot()


.. plot::

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    vlabel = {key: key for key in network.neighbours('0')}
    vlabel['0'] = '0'

    vcolor = {key: (255, 0, 0) for key in vlabel}

    network.plotter.vsize = 0.2
    network.plotter.vlabel = vlabel
    network.plotter.vcolor = vcolor
    network.plotter.ecolor = {(u, v): (0, 255, 0) for u, v in network.connected_edges('0')}
    network.plot()    


.. code-block:: python

    # degree

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    network.plotter.vsize = 0.2
    network.plotter.vlabel = {key: network.degree(key) for key in network}
    network.plotter.vcolor = {key: (255, 0, 0) for key in network.leaves()}
    network.plot()    


.. plot::

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    network.plotter.vsize = 0.2
    network.plotter.vlabel = {key: network.degree(key) for key in network}
    network.plotter.vcolor = {key: (255, 0, 0) for key in network.leaves()}
    network.plot()    


Attributes
==========

.. code-block:: python

    # set all attributes of a specific vertex

    network.vertex[a] = {'x': 0.0, 'y': -2.0}
    network.set_vertex_attributes(a, {'x': 0.0, 'y': -2.0})

    # set a specific attribute of a specific vertex

    network.vertex[a]['color'] = (255, 255, 255)
    network.set_vertex_attribute(a, 'color', (255, 255, 255))

    # set a specific attribute of all vertices

    for key in network:
        network[key]['color'] = (255, 255, 255)

    for key in network.vertex:
        network.vertex[key]['color'] = (255, 255, 255)

    for key in network.vertices():
        network[key]['color'] = (255, 255, 255)

    for key in network.vertices_iter():
        network[key]['color'] = (255, 255, 255)

    for key, attr in network.vertices(True):
        attr['color'] = (255, 255, 255)

    for key, attr in network.vertices_iter(True):
        attr['color'] = (255, 255, 255)

    network.set_vertices_attribute('color', (255, 255, 255))

    # set the default attributes of all vertices
    # this also affects vertices that are added later

    network.set_dva({'x': 0.0, 'y': 0.0, 'color': (255, 255, 255)})


.. code-block:: python

    # set all attributes of a specific edge

    network.edge[a][b] = {}
    network.set_edge_attributes(a, b, {})

    # set a specific attribute of a specific edge

    network.edge[a][b]['color'] = (0, 0, 0)
    network.set_edge_attribute(a, b, 'color', (0, 0, 0))

    # set a specific attribute of all edges

    for u in network.edge:
        for v in network.edge[u]:
            network.edge[u][v]['color'] = (0, 0, 0)

    for u, v in network.edges():
        network.edge[u][v]['color'] = (0, 0, 0)

    for u, v in network.edges_iter():
        network.edge[u][v]['color'] = (0, 0, 0)

    for u, v, attr in network.edges(True):
        attr['color'] = (0, 0, 0)

    for u, v, attr in network.edges_iter(True):
        attr['color'] = (0, 0, 0)

    network.set_edges_attribute('color', (0, 0, 0))

    # set the default attributes of all edges
    # this also affects edges that are added later

    network.set_dea({'color': (0, 0, 0)})


.. code-block:: python

    # get all attributes of a specific vertex

    print network.vertex[a]
    print network.get_vertex_attributes(a)

    # get a specific attribute of a specific vertex

    print network.vertex[a]['color']
    print network.get_vertex_attribute(a, 'color')
    print network.get_vertex_attribute(a, 'color', (255, 255, 255))

    # get a specific attribute of all vertices

    color = []
    for key, attr in network.vertices_iter(True):
        color.append(attr['color'])

    color = network.get_vertices_attribute('color')

    print color

    # get multiple attributes of all vertices
    # (with a default value)

    xy = []
    for key, attr in network.vertices_iter(True):
        x = attr.get('x', 0.0)
        y = attr.get('y', 0.0)
        xy.append((x, y))

    xy = network.get_vertices_attributes(('x', 'y'), (0.0, 0.0))

    print xy


.. code-block:: python
    
    import random
    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    for key, attr in network.vertices_iter(True):
        attr['color'] = random.choice(colors)

    network.plotter.vsize = 0.2
    network.plotter.vcolor = {key: attr['color'] for key, attr in network.vertices_iter(True)}
    network.plot()


.. plot::

    import random
    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    for key, attr in network.vertices_iter(True):
        attr['color'] = random.choice(colors)

    network.plotter.vsize = 0.2
    network.plotter.vcolor = {key: attr['color'] for key, attr in network.vertices_iter(True)}
    network.plot()


Geometry
========

.. code-block:: python

    # vertex coordinates

    xy = []
    for key, attr in network.vertices_iter(True):
        x = attr['x']
        y = attr['y']
        xy.append([x, y])

    xy = [network.vertex_coordinates(key, 'xy') for key in network]

    xy = network.xy


.. code-block:: python

    # edge lengths

    lengths = []
    for u, v in network.edges_iter():
        ax, ay = network.vertex_cooridnates(u, 'xy')
        bx, by = network.vertex_cooridnates(v, 'xy')
        l = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
        lengths.append(l)

    lengths = [network.edge_length(u, v) for u, v in network.edges_iter()]



Customisation
=============

.. give cablenet as example
.. copy-paste from nesthilo

.. code-block:: python
   
    class Cablenet(Network):
       
        def __init__(self):
            super(Cablenet, self).__init__()


.. code-block:: python
   
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


.. code-block:: python

    import brg_rhino as rhino

   
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
            rhino.draw_network(self)


Algorithms
==========

.. network find find_faces
.. network construct dual

.. code-block:: python

    # shortest path
    # when not all edge weights are the same
    # => use Dijkstra algorithm

    import brg

    from brg.datastructures.network import Network
    from brg.datastructures.network.algorithms import network_dijkstra_path

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    weight = dict(((u, v), network.edge_length(u, v)) for u, v in network.edges())
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    start = '21'
    end = '22'

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


.. plot::

    import brg

    from brg.datastructures.network import Network
    from brg.datastructures.network.algorithms import network_dijkstra_path

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    weight = dict(((u, v), network.edge_length(u, v)) for u, v in network.edges())
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    start = '21'
    end = '22'

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


.. code-block:: python

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


.. plot::

    import brg

    from brg.datastructures.network import Network
    from brg.datastructures.network.algorithms import find_network_faces
    from brg.datastructures.network.algorithms import construct_dual_network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    find_network_faces(network, network.leaves())

    dual = construct_dual_network(network)

    dual.plot()
