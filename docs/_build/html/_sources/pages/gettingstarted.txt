.. _getting-started:

********************************************************************************
Getting started
********************************************************************************


Dependencies
================================================================================

- Numpy
- Scipy
- Matplotlib
- Shapely
- ...


Download
================================================================================

Get the framework from `bitbucket <http://bitbucket.org>`_.


Installation
================================================================================

A ``pip`` install is in the works


Setup
================================================================================

Environment variables


First steps
================================================================================

Some quick examples...

.. code-block:: python
    :linenos:
    
    import brg
    from brg.datastructures import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))
    mesh.draw()
