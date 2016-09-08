.. _reference:

********************************************************************************
Reference Guide
********************************************************************************

The Block Research Group (BRG) framework is a set of Python packages for
computational architectural grometry, structural design, and fabrication.
There is a main package (``brg``) that defines the base functionality of the
framework, and several wrapper packages (``brg_rhino``, ``brg_maya``, ...) that
provide wrappers for different CAD environments.


brg
---

This is the main package. It defines all base functionality of the framework, and
the main datastructures.

.. toctree::
   :maxdepth: 1

   brg-com
   brg-datastructures
   brg-files
   brg-geometry
   brg-numerical
   brg-physics
   brg-utilities
   brg-viewers
   brg-web


brg_rhino
---------

This is a wrapper for Rhino. Note that the packages of ``brg_rhino`` are written
for IronPython, as this is the Python implementation used by Rhino.

.. toctree::
   :maxdepth: 1

   brg_rhino-conduits
   brg_rhino-datastructures
   brg_rhino-forms
   brg_rhino-geometry
   brg_rhino-ui
   brg_rhino-utilities


brg_maya
--------

This is a wrapper for Maya
