.. _datastructures:

********************************************************************************
Datastructures
********************************************************************************

.. contents::

.. color.vertex should be the default vertex color if it is defined
.. color.edge should be the default edge color if it is defined
.. remove color.xxx!
.. add references to the docs throughout
.. rename to dijkstra_path
.. add find_faces and dual drawing (combined plot)
.. combine adjacency stuff into plot
.. add intro and mesh equivalence
.. subdivision algorithm for meshes
.. remesh mesh


Create a network
================

.. code-block:: python

    from brg.datastructures.network import Network

    network = Network()

    print network

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # network: 'Network'
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #
    # - default vertex attributes:
    # x = 0.0
    # y = 0.0
    # z = 0.0
    #
    # - default edge attributes:
    # None
    #
    # - number of vertices: 0
    # - number of edges: 0
    #
    # - vertex degree min: 0
    # - vertex degree max: 0
    #


.. code-block:: python

    a = network.add_vertex()
    b = network.add_vertex()
    c = network.add_vertex()
    d = network.add_vertex()
    e = network.add_vertex()

    network.add_edge(a, b)
    network.add_edge(a, c)
    network.add_edge(a, d)
    network.add_edge(a, e)

    print a, b, c, d, e

    # 0 1 2 3 4

    print network.vertex[a]

    # {'y': 0.0, 'x': 0.0, 'z': 0.0}

    print network

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # network: 'Network'
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #
    # - default vertex attributes:
    # x = 0.0
    # y = 0.0
    # z = 0.0
    #
    # - default edge attributes:
    # None
    #
    # - number of vertices: 5
    # - number of edges: 4
    #
    # - vertex degree min: 1
    # - vertex degree max: 4


.. code-block:: python

    network.vertex[b]['x'] = 1.0
    network.vertex[c]['y'] = 1.0
    network.vertex[d]['x'] = -1.0
    network.vertex[e]['y'] = -1.0

    network.plot()


.. plot::

    from brg.datastructures.network import Network

    network = Network()

    a = network.add_vertex()
    b = network.add_vertex()
    c = network.add_vertex()
    d = network.add_vertex()
    e = network.add_vertex()

    network.add_edge(a, b)
    network.add_edge(a, c)
    network.add_edge(a, d)
    network.add_edge(a, e)

    network.vertex[b]['x'] = 1.0
    network.vertex[c]['y'] = 1.0
    network.vertex[d]['x'] = -1.0
    network.vertex[e]['y'] = -1.0

    network.plotter.vsize = 0.05
    network.plot()


.. code-block:: python

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


Constructors
============

.. code-block:: python
    
    vertices = [[0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [-1.0, 0.0, 0.0],
                [0.0, -1.0, 0.0]]

    edges = [(0, 1), (0, 2), (0, 3), (0, 4)]

    network = Network.from_vertices_and_edges(vertices, edges)


.. code-block:: python

    # network = Network.from_obj('...')

    path = brg.get_data('grid_irregular.obj')

    network = Network.from_obj(path)

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


Topology
========

.. code-block:: python

    # adjacency

    for key in network:
        print network.neighbours(key)

    # 24 ['0', '31', '27', '12']
    # 25 ['3']
    # 26 ['20']
    # 27 ['1', '24', '3', '19']
    # 20 ['8', '26', '17', '18']
    # 21 ['15']
    # 22 ['17']
    # 23 ['2']
    # 28 ['14']
    # 29 ['9', '8', '30', '14', '18']
    # 1 ['27']
    # 0 ['24', '10', '7', '19']
    # 3 ['19', '25', '27', '9', '15']
    # 2 ['18', '23', '30', '6']
    # 5 ['30']
    # 4 ['17']
    # 7 ['0', '13', '17', '8']
    # 6 ['2']
    # 9 ['19', '3', '29', '14']
    # 8 ['19', '18', '20', '29', '7']
    # 11 ['15']
    # 10 ['0']
    # 13 ['7']
    # 12 ['24']
    # 15 ['11', '3', '21', '14']
    # 14 ['9', '15', '30', '28', '29']
    # 17 ['20', '4', '22', '7']
    # 16 ['18']
    # 19 ['9', '0', '3', '27', '8']
    # 18 ['8', '2', '20', '29', '16']
    # 31 ['24']
    # 30 ['2', '5', '29', '14']


.. code-block:: python

    # adjacency

    vlabel = {key: key for key in network.neighbours('0')}
    vlabel['0'] = '0'

    vcolor = {key: (255, 0, 0) for key in vlabel}
    vcolor['0'] = (0, 255, 0)

    network.plotter.vsize = 0.2
    network.plotter.vlabel = vlabel
    network.plotter.vcolor = vcolor
    network.plot()


.. plot::

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    vlabel = {key: key for key in network.neighbours('0')}
    vlabel['0'] = '0'

    vcolor = {key: (255, 0, 0) for key in vlabel}
    vcolor['0'] = (0, 255, 0)

    network.plotter.vsize = 0.2
    network.plotter.vlabel = vlabel
    network.plotter.vcolor = vcolor
    network.plot()    


.. code-block:: python

    # degree

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

    # setting attributes

    network.vertex[a] = {'x': 0.0, 'y': -2.0}
    network.set_vertex_attributes(a, {'x': 0.0, 'y': -2.0})

    network.vertex[a]['x'] = -5.0
    network.set_vertex_attribute(a, 'x', -5.0)

    network.vertex[a]['is_fixed'] = False
    network.set_vertex_attribute(a, 'is_fixed', False)

    for key in network:
        network[key]['is_fixed'] = False

    network.set_vertices_attribute('is_fixed', False)

    for key in network:
        network[key]['x'] = 0.0
        network[key]['y'] = 0.0
        network[key]['z'] = 0.0
        network[key]['is_fixed'] = False

    network.set_vertices_attributes({'x': 0.0, 'y': 0.0, 'z': 0.0, 'is_fixed': False})

    network.set_dva({'x': 0.0, 'y': 0.0, 'z': 0.0, 'is_fixed': False})


.. code-block:: python

    # getting attributes

    print network.vertex[a]
    print network.get_vertex_attributes(a)

    print network.vertex[a]['x']
    print network.get_vertex_attribute(a, 'x')
    print network.get_vertex_attribute(a, 'x', 10.0)


Geometry
========

See geometry examples?


Customisation
=============

.. give cablenet as example
.. copy-paste from nesthilo

.. code-block:: python
   
    class CustomNetwork(Network):
       
        def __init__(self):
            super(CustomNetwork, self).__init__()
            self.dva.update({
                'is_fixed': False,
                'cx': None,
                'cy': None
            })


.. seealso::
    
    :mod:`brg_ags.diagrams`


Export
======

.. code-block:: python
   
    # data

    network = Network.from_obj('lines.obj')

    # do stuff

    data = network.to_data()
    data = network.to_json()
    data = network.to_csv()

    other = Network.from_data(data)


Algorithms (Extras)
===================

.. network: paths
.. mesh: subdivision
.. network & mesh: smoothing

.. code-block:: python

    import brg

    from brg.datastructures.network import Network
    from brg.datastructures.network.algorithms import network_shortest_path_dijkstra

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    weight = dict(((u, v), network.edge_length(u, v)) for u, v in network.edges())
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    start = '21'
    end = '22'

    path = network_shortest_path_dijkstra(network.adjacency, weight, start, end)

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
    from brg.datastructures.network.algorithms import network_shortest_path_dijkstra

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    weight = dict(((u, v), network.edge_length(u, v)) for u, v in network.edges())
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    start = '21'
    end = '22'

    path = network_shortest_path_dijkstra(network.adjacency, weight, start, end)

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

