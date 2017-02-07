.. _the-numerical-package:

********************************************************************************
The Numerical Package
********************************************************************************

.. contents::


NumPy & SciPy
=============

.. code-block:: python

	import numpy as np
	import scipy as sp


Working with indexed data
=========================

The datastructures use dictionaries to keep track of the relationship between
vertices, edges, and faces, and to manage their attributes. Dictionaries map
named keys to values, but the key-value pairs have no specific order, and
whatever ordering they have may change whenever pairs are added or removed.

Numerical calculations with (for example) NumPy and SciPy are based on indexed
arrays of data. The data has a specific order and is accessed as such.

There is a simple and robust mechanism to bridge the difference between these 
two data formats, using key-index maps.


.. code-block:: python
	
	import brg
	from brg.datastructures.network.network import Network
	from brg.numerical.matrices import connectivity_matrix

	network = Network.from_obj(brg.get_data('lines.obj'))


.. code-block:: python
	
	key_index = dict((k, i) for i, k in network.vertices_enum())

	xyz = [network.vertex_coordinates(key) for key in network]

	edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]

	for i, j in edges:
		print xyz[i]
		print xyz[j]


Matrices
========

The numerical package has several convenience functions for the construction of 
matrices that are commonly used in calculations related to ...


Adjacency matrix
----------------

.. code-block:: python
	
	from brg.numerical.matrices import adjacency_matrix

	adjacency = [[key_index[nbr] for nbr in network.neighbours(key)] for key in network]

	A = adjacency_matrix(adjacency)


Degree matrix
-------------

.. code-block:: python
	
	from brg.numerical.matrices import degree_matrix

	adjacency = [[key_index[nbr] for nbr in network.neighbours(key)] for key in network]

	D = degree_matrix(adjacency)


Connectivity matrix
-------------------

.. code-block:: python
	
	from brg.numerical.matrices import connectivity_matrix

	edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]

	C = connectivity_matrix(edges)


Laplacian matrix
----------------

.. code-block:: python
	
	from brg.numerical.matrices import laplacian_matrix

	edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]

	L = laplacian_matrix(edges)


Datastructure-specific implementations
--------------------------------------

.. code-block:: python
	
	from brg.datastructures.network.numerical.matrices import adjacency_matrix
	from brg.datastructures.network.numerical.matrices import degree_matrix
	from brg.datastructures.network.numerical.matrices import connectivity_matrix
	from brg.datastructures.network.numerical.matrices import laplacian_matrix

	A = adjacency_matrix(network)
	D = degree_matrix(network)
	C = connectivity_matrix(network)
	L = laplacian_matrix(network)


Examples
--------

.. code-block:: python

	from brg.geometry.functions import centroid

	xyz = np.array(xyz)

    centroids1 = [centroid([network.vertex_coordinates(nbr) for nbr in network.neighbours(key)])
                  for key in network.vertices_iter()]

    centroids1 = np.array(centroids1)

    centroids2 = xyz - L.dot(xyz)
    centroids3 = A.dot(xyz) / D.diagonal().reshape((-1, 1))

    print np.allclose(centroids1, centroids2)
    print np.allclose(centroids1, centroids3)


Linear Algebra
==============

.. code-block:: python

	# compute the length 
	
	from brg.numerical.linalg import normrow

	uvw = C.dot(xyz)

	l = normrow(uvw)

