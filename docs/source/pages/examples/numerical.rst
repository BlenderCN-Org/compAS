.. _numerical:

********************************************************************************
Numerical
********************************************************************************

.. contents::


NumPy & SciPy
=============

Most (if not all) numerical calculations in the core library are based on NumPy
and SciPy. For all the code snippets on this page, we will assume that both packages
have been imported as seen here:

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
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    key_index = dict((k, i) for i, k in network.vertices_enum())

    xyz   = [network.vertex_coordinates(key) for key in network]
    edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]

    network.plotter.vsize = 0.2
    network.plotter.vlabel = key_index
    network.plotter.elabel = {(u, v): '{0}-{1}'.format(key_index[u], key_index[v]) for u, v in network.edges()}

    network.plot()


.. plot::

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    key_index = dict((k, i) for i, k in network.vertices_enum())

    xyz   = [network.vertex_coordinates(key) for key in network]
    edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]

    network.plotter.vsize = 0.2
    network.plotter.vlabel = key_index
    network.plotter.elabel = {(u, v): '{0}-{1}'.format(key_index[u], key_index[v]) for u, v in network.edges()}

    network.plot()


Matrices
========

The numerical package has several convenience functions for the construction of 
matrices that are commonly used in architectural and structural geometry calculations.


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
    
    from brg.datastructures.network.numerical.matrices import network_adjacency_matrix
    from brg.datastructures.network.numerical.matrices import network_degree_matrix
    from brg.datastructures.network.numerical.matrices import network_connectivity_matrix
    from brg.datastructures.network.numerical.matrices import network_laplacian_matrix

    A = network_adjacency_matrix(network)
    D = network_degree_matrix(network)
    C = network_connectivity_matrix(network)
    L = network_laplacian_matrix(network)


Comparison
----------

.. code-block:: python
    
    L = L / D.diagonal().reshape((-1, 1))

    xyz = np.array(xyz)

    c1 = [network.vertex_neighbourhood_centroid(key) for key in network]
    c1 = np.array(c1)

    c2 = xyz - L.dot(xyz)
    c3 = A.dot(xyz) / D.diagonal().reshape((-1, 1))

    print np.allclose(c1, c2)
    print np.allclose(c1, c3)

    # True
    # True


Linear Algebra
==============

.. code-block:: python

    # compute edge lengths
    
    from brg.numerical.linalg import normrow

    uvw = C.dot(xyz)
    l   = normrow(uvw)

    network.plotter.elabel = {(u, v): '{0:.1f}'.format(l[index, 0]) for index, u, v in network.edges_enum()}
    network.plot()


.. plot::

    import brg
    from numpy import array
    from brg.datastructures.network import Network
    from brg.numerical.linalg import normrow
    from brg.datastructures.network.numerical.matrices import network_connectivity_matrix

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    xyz = array([network.vertex_coordinates(key) for key in network])
    C   = network_connectivity_matrix(network)
    uvw = C.dot(xyz)
    l   = normrow(uvw)

    network.plotter.vsize = 0.1
    network.plotter.elabel = {(u, v): '{0:.1f}'.format(l[index, 0]) for index, u, v in network.edges_enum()}
    network.plot()


.. code-block:: python

    # centroidal smoothing
    # i.e. laplacian smoothing with *umbrella* weights

    fixed = [key_index[key] for key in network.leaves()]
    free = list(set(range(len(network))) - set(fixed))

    for k in range(10):
        xyz[free] -= 0.1 * L.dot(xyz)[free]

    for key, attr in network.vertices_iter(True):
        index = key_index[key]

        attr['x'] = xyz[index, 0]
        attr['y'] = xyz[index, 1]
        attr['z'] = xyz[index, 2]

    network.plotter.vcolor = {key: (255, 0, 0) for key in network.leaves()}
    network.plot()


.. plot::

    import brg
    from numpy import array
    from brg.datastructures.network import Network
    from brg.datastructures.network.numerical.matrices import network_laplacian_matrix

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    key_index = {key: index for index, key in network.vertices_enum()}

    L     = network_laplacian_matrix(network)
    xyz   = array([network.vertex_coordinates(key) for key in network])
    fixed = [key_index[key] for key in network.leaves()]
    free  = list(set(range(len(network))) - set(fixed))

    for k in range(10):
        xyz[free] -= 0.1 * L.dot(xyz)[free]

    for key, attr in network.vertices_iter(True):
        index = key_index[key]

        attr['x'] = xyz[index, 0]
        attr['y'] = xyz[index, 1]
        attr['z'] = xyz[index, 2]

    network.plotter.vcolor = {key: (255, 0, 0) for key in network.leaves()}
    network.plot()


Other stuff
===========

.. bounding boxes
.. principal components
.. contours

