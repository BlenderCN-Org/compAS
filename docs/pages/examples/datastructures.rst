.. _datastructures:

********************************************************************************
Datastructures
********************************************************************************


.. contents::


Create a network
================

.. code-block:: python

   # create a network
   # add vertices and edges

   from brg.datastructures.network import Network

   network = Network()

   a = network.add_vertex()
   b = network.add_vertex('5', x=1.0, y=0.0, z=0.0)
   c = network.add_vertex('1', x=0.0, y=1.0, z=0.0)
   d = network.add_vertex(attr_dict={'x': -1.0, 'y': 0.0, 'z':0.0})
   e = network.add_vertex('e', x=0.0, y=-1.0)

   print a, b, c, d, e

   network.add_edge(a, b)
   network.add_edge(a, c)
   network.add_edge(a, d)
   network.add_edge(a, e)

   print network


Topology
========

.. code-block:: python

   # adjacency

   for key in network.vertices_iter():
       print key, network.neighbours(key)

   for key in network.vertices_iter():
       print key, network.neighbours_in(key)

   for key in network.vertices_iter():
       print key, network.neighbours_out(key)

   # degree

   for key in network.vertices_iter():
       print key, network.degree(key)

   for key in network.vertices_iter():
       print key, network.degree_in(key)

   for key in network.vertices_iter():
       print key, network.degree_out(key)

   print network.leaves()

   # traversal

   ...


Attributes
==========

.. code-block:: python

   # network attributes
   print network.attributes

   network.attributes['name'] = 'Example'

   # vertex attributes
   
   print network.vertex[a]
   # print network.get_vertex_attributes(a)
   
   print network.vertex[a]['x']
   # print network.get_vertex_attribute(a, 'x')
   # print network.get_vertex_attribute(a, 'x', 10.0)

   for key, attr in network.vertices_iter(True):
       attr['is_fixed'] = True

   # network.set_vertices_attribute('is_fixed', True)

   network.vertex[a]['is_fixed'] = False

   # network.set_vertex_attribute(a, 'is_fixed', False)

   # edge attributes
   print network.edge[a][b]

   network.set_vertices_attribute('is_fixed', False)
   network.set_edges_attribute('weight', 0.0)

   for key, attr in network.vertices_iter(True):
       print key, attr

   for u, v, attr in network.edges_iter(True):
       print u, v, attr


Geometry
========

.. code-block:: python

   # vertices

   for key, attr in network.vertices_iter(True):
      x = attr['x']
      y = attr['y']
      z = attr['z']
      print key, x, y, z

   for key in network.vertex:
      print key, network.vertex_coordinates(key)

   key_xyz = dict((key, network.vertex_coordinates(key)) for key in network)
   # key_xyz = network.key_xyz

   xyz = network.xyz

   # edges

   for u, v in network.edges_iter():
      print network.edge_length(u, v)


Constructors
============

.. code-block:: python

   # constructor functions

   # Network.from_vertices_and_edges()
   # Network.from_lines()
   # Network.from_...()

   network = Network.from_obj('lines.obj')

   network.set_dva({'is_fixed': False, 'cx': None, 'cy': None})
   network.set_dea({'f': 0.0, 'l': 0.0, 'q': 0.0})


Customisation
=============

.. code-block:: python
   
   # custom networks

   class CustomNetwork(Network):
       
       def __init__(self):
           super(CustomNetwork, self).__init__()


.. code-block:: python
   
   # data

   n = Network.from_obj('lines.obj')

   # do stuff

   data = n.to_data()

   m = Network.from_data(data)


Applications
============

...
