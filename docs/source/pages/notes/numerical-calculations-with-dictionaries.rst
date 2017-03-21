.. _notes_numerical-calculations-with-dictionaries:

********************************************************************************
Numerical calculations with dictionaries
********************************************************************************

.. contents::


NumPy & SciPy
=============

http://www.numpy.org/

https://www.scipy.org/

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

    import compas
    from compas.datastructures.network import Network

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    key_index = dict((k, i) for i, k in network.vertices_enum())

    xyz   = [network.vertex_coordinates(key) for key in network]
    edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]

    network.plotter.vsize = 0.2
    network.plotter.vlabel = key_index
    network.plotter.elabel = {(u, v): '{0}-{1}'.format(key_index[u], key_index[v]) for u, v in network.edges()}

    network.plot()


.. plot::

    import compas
    from compas.datastructures.network import Network

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    key_index = dict((k, i) for i, k in network.vertices_enum())

    xyz   = [network.vertex_coordinates(key) for key in network]
    edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]

    network.plotter.vsize = 0.2
    network.plotter.vlabel = key_index
    network.plotter.elabel = {(u, v): '{0}-{1}'.format(key_index[u], key_index[v]) for u, v in network.edges()}

    network.plot()
