.. _mesh:

********************************************************************************
Mesh
********************************************************************************

* :mod:`compas.datastructures.mesh`
* :class:`compas.datastructures.mesh.Mesh`


The ``Mesh`` is an implementation of a *half-edge* data structure, and is suited
for describing 2-manifold, polygonal geometry. It is *face-oriented*, but provides
support for keeping track of edge attributes.


.. warning::
    
    This page is still under construction.


Meshes and Mesh algorithms
==========================

.. remeshing
.. delaunay

.. code-block:: python

    import compas
    from compas.datastructures.mesh import Mesh
    from compas.datastructures.mesh.algorithms import subdivide_mesh_catmullclark

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))
    subd = mesh.copy()

    subdivide_mesh_catmullclark(subd, k=2)

    subd.plotter.vsize = 0.05
    subd.plotter.vcolor = {key: (255, 0, 0) for key in mesh}

    subd.plot()


.. plot::

    import compas
    from compas.datastructures.mesh import Mesh
    from compas.datastructures.mesh.algorithms import subdivide_mesh_catmullclark

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))
    subd = mesh.copy()

    subdivide_mesh_catmullclark(subd, k=2)

    subd.plotter.vsize = 0.05
    subd.plotter.vcolor = {key: (255, 0, 0) for key in mesh}

    subd.plot()


.. code-block:: python

    # this example requires PyOpenGL and PySide

    from compas.datastructures.mesh import Mesh
    from compas.geometry.elements.polyhedron import Polyhedron
    from compas.datastructures.mesh.viewer import SubdMeshViewer
    from compas.datastructures.mesh.algorithms import subdivide_mesh_doosabin

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

