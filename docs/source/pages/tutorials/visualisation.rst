.. _tutorials-visualisation:

********************************************************************************
Visualisation
********************************************************************************

.. plotters => simple 2D/3D viewing
.. viewers => (very) simple interaction
.. modellers? => advanced modelling capabilities


.. contents::


Plotters
========

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


Viewers
=======

.. code-block:: python

    


Rhinoceros 3D
=============


Grasshopper
===========


Blender
=======

