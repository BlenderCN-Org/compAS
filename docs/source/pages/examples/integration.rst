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
    
    import brg
    from brg.datastructures.network import Network

    import brg_rhino as rhino

    network = Network.from_obj(brg.get_data('lines.obj'))

    rhino.draw_network(network)


.. code-block:: python

    # modify geometry


.. code-block:: python

    # update attributes


.. code-block:: python

    # display labels/normals/selfweight/forces
