.. _datastructures:

********************************************************************************
Datastructures
********************************************************************************

.. contents::

.. remove color.xxx!
.. add references to the docs throughout
.. rename to dijkstra_path
.. add find_faces and dual drawing (combined plot)
.. combine adjacency stuff into plot
.. add mesh equivalence
.. subdivision algorithm for meshes
.. remesh mesh
.. cycle through vertices and edges


Mesh, Network, VolMesh
======================

There are three types of data structures in the core library. 

The ``Mesh`` (:class:`brg.datastructures.mesh.Mesh`) is an implementation of a
*half-edge* data structure, and is suited for describing 2-manifold, polygonal
geometry. It is *face-oriented*, but provides support for keeping track of
edge attributes.

The ``Network`` (:class:`brg.datastructures.network.Network`) is an edge graph.
It is suited for describing general networks of connected nodes or vertices,
both planar and non-planar. It is *edge-oriented*, but provides support for face
topology if the network is planar.

The ``VolMesh`` (:class:`brg.datastructures.volmesh.VolMesh`) is an implementation
of a *half-plane* data structure. It is suited for describing cellular meshes,
i.e. 3-manifold, polygonal geometry.

These three types of data structures have very similar interfaces. They differ
mainly in the types of algorithms they provide and are compatible with. This
document focusses on networks, because they are the most general. However, an
introduction to the available data structures base don the ``Mesh`` or ``VolMesh``
would be very similar. Some of the similarities and differences are discussed
at the bottom of the page.


Create a network
================

.. code-block:: python

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

    print network.vertex[a]

    # {'y': 0.0, 'x': 0.0, 'z': 0.0}


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

    for key in sorted(network.vertices(), key=int):
        print network.neighbours(key)

    # 0 ['24', '10', '7', '19']
    # 1 ['27']
    # 2 ['18', '23', '30', '6']
    # 3 ['19', '25', '27', '9', '15']
    # 4 ['17']
    # 5 ['30']
    # 6 ['2']
    # 7 ['0', '13', '17', '8']
    # 8 ['19', '18', '20', '29', '7']
    # 9 ['19', '3', '29', '14']
    # 10 ['0']
    # 11 ['15']
    # 12 ['24']
    # 13 ['7']
    # 14 ['9', '15', '30', '28', '29']
    # 15 ['11', '3', '21', '14']
    # 16 ['18']
    # 17 ['20', '4', '22', '7']
    # 18 ['8', '2', '20', '29', '16']
    # 19 ['9', '0', '3', '27', '8']
    # 20 ['8', '26', '17', '18']
    # 21 ['15']
    # 22 ['17']
    # 23 ['2']
    # 24 ['0', '31', '27', '12']
    # 25 ['3']
    # 26 ['20']
    # 27 ['1', '24', '3', '19']
    # 28 ['14']
    # 29 ['9', '8', '30', '14', '18']
    # 30 ['2', '5', '29', '14']
    # 31 ['24']


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


.. Export
.. ======

.. .. code-block:: python
   
..     # data

..     network = Network.from_obj('lines.obj')

..     # do stuff

..     data = network.to_data()
..     data = network.to_json()
..     data = network.to_csv()

..     other = Network.from_data(data)


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


Meshes and Mesh algorithms
==========================

.. remeshing
.. delaunay

.. code-block:: python

    import brg
    from brg.datastructures.mesh import Mesh
    from brg.datastructures.mesh.algorithms import subdivide_mesh_catmullclark

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))
    subd = mesh.copy()

    subdivide_mesh_catmullclark(subd, k=2)

    subd.plotter.vsize = 0.05
    subd.plotter.vcolor = {key: (255, 0, 0) for key in mesh}

    subd.plot()


.. plot::

    import brg
    from brg.datastructures.mesh import Mesh
    from brg.datastructures.mesh.algorithms import subdivide_mesh_catmullclark

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))
    subd = mesh.copy()

    subdivide_mesh_catmullclark(subd, k=2)

    subd.plotter.vsize = 0.05
    subd.plotter.vcolor = {key: (255, 0, 0) for key in mesh}

    subd.plot()


.. code-block:: python

    # this example requires PyOpenGL and PySide

    from brg.datastructures.mesh import Mesh
    from brg.geometry.elements.polyhedron import Polyhedron
    from brg.datastructures.mesh.viewer import SubdMeshViewer
    from brg.datastructures.mesh.algorithms import subdivide_mesh_doosabin

    cube = Polyhedron.generate(6)

    mesh = Mesh.from_vertices_and_faces(cube.vertices, cube.faces)

    viewer = SubdMeshViewer(mesh, subdfunc=subdivide_mesh_doosabin, width=600, height=600)

    viewer.axes.x_color = (0.1, 0.1, 0.1)
    viewer.axes.y_color = (0.1, 0.1, 0.1)
    viewer.axes.z_color = (0.1, 0.1, 0.1)

    viewer.axes_on = False
    viewer.grid_on = False

    viewer.setup()
    viewer.show()

