.. _integration:

********************************************************************************
Integration
********************************************************************************

.. drawing
.. update geometry
.. conduits
.. external script
.. 


Rhino
=====

.. code-block:: python

    # simple drawing
    
    import compas
    from compas.datastructures.network import Network

    import compas_rhino as rhino

    network = Network.from_obj(compas.get_data('lines.obj'))

    rhino.draw_network(network)


.. code-block:: python

    # modify geometry


.. code-block:: python

    # update attributes


.. code-block:: python

    # display labels/normals/selfweight/forces
