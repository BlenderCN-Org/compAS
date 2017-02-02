.. _api:

********************************************************************************
API Reference
********************************************************************************

The Block Research Group (BRG) framework is a set of Python packages for
computational architectural geometry, structural design, and fabrication.
There is a main package (``brg``) that defines the base functionality of the
framework, and several wrapper packages (``brg_rhino``, ``brg_maya``, ...) that
provide wrappers for different CAD environments.


brg
---

This is the main package. It defines all base functionality of the framework, and
the main datastructures.

.. toctree::
   :maxdepth: 1

   api/brg-com
   api/brg-datastructures
   api/brg-files
   api/brg-geometry
   api/brg-numerical
   api/brg-physics
   api/brg-utilities
   api/brg-viewers


brg_rhino
---------

This is a wrapper for Rhino. Note that the packages of ``brg_rhino`` are written
for IronPython, as this is the Python implementation used by Rhino.

.. toctree::
   :maxdepth: 1



brg_gh
------

This is a wrapper for Grasshopper.

.. toctree::
   :maxdepth: 1



brg_blender
-----------

This is a wrapper for Blender.

.. toctree::
   :maxdepth: 1



brg_maya
--------

This is a wrapper for Maya.

.. toctree::
   :maxdepth: 1



brg_web
-------

This is a wrapper for the browser.

.. toctree::
   :maxdepth: 1
