.. _getting-started:

********************************************************************************
Getting started
********************************************************************************

.. sectionauthor:: Tom Van Mele <van.mele@arch.ethz.ch>


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


What's in the box
================================================================================

Folder structure etc.


First steps
================================================================================

Some quick examples...

.. code-block:: python
    :linenos:
    
    import brg
    from brg.datastructures import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))
    mesh.draw()
