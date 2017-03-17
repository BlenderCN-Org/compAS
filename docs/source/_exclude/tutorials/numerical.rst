.. _numerical:

********************************************************************************
Numerical
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


Matrices
========

The numerical package has several convenience functions for the construction of 
matrices that are commonly used in architectural and structural geometry calculations.


Adjacency matrix
----------------

.. code-block:: python

    from compas.numerical.matrices import adjacency_matrix

    adjacency = [[key_index[nbr] for nbr in network.neighbours(key)] for key in network]

    A = adjacency_matrix(adjacency)


Degree matrix
-------------

.. code-block:: python

    from compas.numerical.matrices import degree_matrix

    adjacency = [[key_index[nbr] for nbr in network.neighbours(key)] for key in network]

    D = degree_matrix(adjacency)


Connectivity matrix
-------------------

.. code-block:: python

    from compas.numerical.matrices import connectivity_matrix

    edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]

    C = connectivity_matrix(edges)


Laplacian matrix
----------------

.. code-block:: python

    from compas.numerical.matrices import laplacian_matrix

    edges = [(key_index[u], key_index[v]) for u, v in network.edges_iter()]

    L = laplacian_matrix(edges)


Datastructure-specific implementations
--------------------------------------

.. code-block:: python
    
    from compas.datastructures.network.numerical.matrices import network_adjacency_matrix
    from compas.datastructures.network.numerical.matrices import network_degree_matrix
    from compas.datastructures.network.numerical.matrices import network_connectivity_matrix
    from compas.datastructures.network.numerical.matrices import network_laplacian_matrix

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
    
    from compas.numerical.linalg import normrow

    uvw = C.dot(xyz)
    l   = normrow(uvw)

    network.plotter.elabel = {(u, v): '{0:.1f}'.format(l[index, 0]) for index, u, v in network.edges_enum()}
    network.plot()


.. plot::

    import compas
    from numpy import array
    from compas.datastructures.network import Network
    from compas.numerical.linalg import normrow
    from compas.datastructures.network.numerical.matrices import network_connectivity_matrix

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

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

    import compas
    from numpy import array
    from compas.datastructures.network import Network
    from compas.datastructures.network.numerical.matrices import network_laplacian_matrix
    from compas.datastructures.network.numerical.matrices import network_degree_matrix

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    key_index = {key: index for index, key in network.vertices_enum()}

    L = network_laplacian_matrix(network)
    D = network_degree_matrix(network)

    L = L / D.diagonal().reshape((-1, 1))

    xyz = array([network.vertex_coordinates(key) for key in network])

    fixed = [key_index[key] for key in network.leaves()]
    free = list(set(range(len(network))) - set(fixed))

    for k in range(10):
        xyz[free] -= L.dot(xyz)[free]

    for key, attr in network.vertices_iter(True):
        index = key_index[key]

        attr['x'] = xyz[index, 0]
        attr['y'] = xyz[index, 1]
        attr['z'] = xyz[index, 2]

    network.plotter.vcolor = {key: (255, 0, 0) for key in network.leaves()}
    network.plot()


.. plot::

    import compas
    from numpy import array
    from compas.datastructures.network import Network
    from compas.datastructures.network.numerical.matrices import network_laplacian_matrix
    from compas.datastructures.network.numerical.matrices import network_degree_matrix

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    key_index = {key: index for index, key in network.vertices_enum()}

    L = network_laplacian_matrix(network)
    D = network_degree_matrix(network)

    L = L / D.diagonal().reshape((-1, 1))

    xyz = array([network.vertex_coordinates(key) for key in network])

    fixed = [key_index[key] for key in network.leaves()]
    free = list(set(range(len(network))) - set(fixed))

    for k in range(10):
        xyz[free] -= L.dot(xyz)[free]

    for key, attr in network.vertices_iter(True):
        index = key_index[key]

        attr['x'] = xyz[index, 0]
        attr['y'] = xyz[index, 1]
        attr['z'] = xyz[index, 2]

    network.plotter.vcolor = {key: (255, 0, 0) for key in network.leaves()}
    network.plot()


Other stuff
===========

Object-aligned bounding box
---------------------------

.. code-block:: python

    # generate randomly oriented clusters of points

    from numpy.random import randint
    from numpy.random import rand

    from compas.numerical.xforms import rotation_matrix

    clouds = []

    for i in range(8):
        a = randint(1, high=8) * 10 * 3.14159 / 180
        d = [1, 1, 1]

        cloud = rand(100, 3)

        if i in (1, 2, 5, 6):
            cloud[:, 0] *= - 10.0
            cloud[:, 0] -= 3.0
            d[0] = -1
        else:
            cloud[:, 0] *= 10.0
            cloud[:, 0] += 3.0

        if i in (2, 3, 6, 7):
            cloud[:, 1] *= - 3.0
            cloud[:, 1] -= 3.0
            d[1] = -1
        else:
            cloud[:, 1] *= 3.0
            cloud[:, 1] += 3.0

        if i in (4, 5, 6, 7):
            cloud[:, 2] *= - 6.0
            cloud[:, 2] -= 3.0
            d[2] = -1
        else:
            cloud[:, 2] *= 6.0
            cloud[:, 2] += 3.0

        R = rotation_matrix(a, d)
        cloud[:] = cloud.dot(R)

        clouds.append(cloud.tolist())


.. code-block:: python

    # compute object-aligned bounding boxes

    import matplotlib.pyplot as plt

    from compas.plotters.helpers import Bounds
    from compas.plotters.helpers import Cloud3D
    from compas.plotters.helpers import Box

    from compas.plotters.drawing import create_axes_3d

    axes = create_axes_3d()

    bounds = Bounds([point for points in clouds for point in points])
    bounds.plot(axes)

    for cloud in clouds:
        bbox = bounding_box_3d(cloud)

        Cloud3D(cloud).plot(axes)
        Box(bbox[1]).plot(axes)

    plt.show()


.. plot::
    
    from numpy.random import randint
    from numpy.random import rand

    import matplotlib.pyplot as plt

    from compas.plotters.helpers import Bounds
    from compas.plotters.helpers import Cloud3D
    from compas.plotters.helpers import Box

    from compas.numerical.xforms import rotation_matrix

    from compas.plotters.drawing import create_axes_3d

    from compas.numerical.spatial import bounding_box_3d

    clouds = []

    for i in range(8):
        a = randint(1, high=8) * 10 * 3.14159 / 180
        d = [1, 1, 1]

        cloud = rand(100, 3)

        if i in (1, 2, 5, 6):
            cloud[:, 0] *= - 10.0
            cloud[:, 0] -= 3.0
            d[0] = -1
        else:
            cloud[:, 0] *= 10.0
            cloud[:, 0] += 3.0

        if i in (2, 3, 6, 7):
            cloud[:, 1] *= - 3.0
            cloud[:, 1] -= 3.0
            d[1] = -1
        else:
            cloud[:, 1] *= 3.0
            cloud[:, 1] += 3.0

        if i in (4, 5, 6, 7):
            cloud[:, 2] *= - 6.0
            cloud[:, 2] -= 3.0
            d[2] = -1
        else:
            cloud[:, 2] *= 6.0
            cloud[:, 2] += 3.0

        R = rotation_matrix(a, d)
        cloud[:] = cloud.dot(R)

        clouds.append(cloud.tolist())

    axes = create_axes_3d()

    bounds = Bounds([point for points in clouds for point in points])
    bounds.plot(axes)

    for cloud in clouds:
        bbox = bounding_box_3d(cloud)

        Cloud3D(cloud).plot(axes)
        Box(bbox[1]).plot(axes)

    plt.show()


Principal component analysis
----------------------------

.. code-block:: python

    # generate data for principal component analysis

    from numpy import random

    from compas.numerical.xforms import rotation_matrix

    data = random.rand(300, 3)
    data[:, 0] *= 10.0
    data[:, 1] *= 1.0
    data[:, 2] *= 4.0

    a = 3.14159 * 30.0 / 180
    Ry = rotation_matrix(a, [0, 1.0, 0.0])

    a = -3.14159 * 45.0 / 180
    Rz = rotation_matrix(a, [0, 0, 1.0])

    data[:] = data.dot(Ry).dot(Rz)


.. code-block:: python

    # compute principal components

    import matplotlib.pyplot as plt

    from compas.plotters.helpers import Axes3D
    from compas.plotters.helpers import Cloud3D
    from compas.plotters.helpers import Bounds
    from compas.plotters.drawing import create_axes_3d

    average, vectors, values = principal_components(data)

    axes = create_axes_3d()

    Bounds(data).plot(axes)
    Cloud3D(data).plot(axes)
    Axes3D(average, vectors).plot(axes)

    plt.show()


.. plot::

    from numpy import random

    import matplotlib.pyplot as plt

    from compas.numerical.xforms import rotation_matrix

    from compas.plotters.helpers import Axes3D
    from compas.plotters.helpers import Cloud3D
    from compas.plotters.helpers import Bounds
    from compas.plotters.drawing import create_axes_3d

    from compas.numerical.statistics import principal_components

    data = random.rand(300, 3)
    data[:, 0] *= 10.0
    data[:, 1] *= 1.0
    data[:, 2] *= 4.0

    a = 3.14159 * 30.0 / 180
    Ry = rotation_matrix(a, [0, 1.0, 0.0])

    a = -3.14159 * 45.0 / 180
    Rz = rotation_matrix(a, [0, 0, 1.0])

    data[:] = data.dot(Ry).dot(Rz)

    average, vectors, values = principal_components(data)

    axes = create_axes_3d()

    Bounds(data).plot(axes)
    Cloud3D(data).plot(axes)
    Axes3D(average, vectors).plot(axes)

    plt.show()


Contours
--------

.. code-block:: python

    # plot the isolines of a distance field
    # the distance field is defined by the distance of every vertex
    # from the 2D centroid of the mesh

    import compas

    from compas.datastructures.mesh import Mesh

    from compas.geometry import centroid_points
    from compas.geometry import distance_point_point

    from compas.datastructures.mesh.numerical import plot_mesh_isolines

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    points = [mesh.vertex_coordinates(key) for key in mesh]
    centroid = centroid_points(points)

    for key, attr in mesh.vertices_iter(True):
        xyz = mesh.vertex_coordinates(key)
        attr['d'] = distance_point_point(xyz, centroid)

    plot_mesh_isolines(mesh, 'd')


.. plot::

    import compas

    from compas.datastructures.mesh import Mesh

    from compas.geometry import centroid_points
    from compas.geometry import distance_point_point

    from compas.datastructures.mesh.numerical import plot_mesh_isolines

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    points = [mesh.vertex_coordinates(key) for key in mesh]
    centroid = centroid_points(points)

    for key, attr in mesh.vertices_iter(True):
        xyz = mesh.vertex_coordinates(key)
        attr['d'] = distance_point_point(xyz, centroid)

    plot_mesh_isolines(mesh, 'd')
