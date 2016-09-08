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

   COM package (brg.com) <brg-com>
   The datastructures (brg.datastructures) <brg-datastructures>


brg_rhino
---------

This is a wrapper for Rhino. Note that the packages of ``brg_rhino`` are written
for IronPython, as this is the Python implementation used by Rhino.

.. toctree::
   :maxdepth: 1

   Conduits (brg_rhino.conduits) <brg_rhino-conduits>
   Datastructure wrappers (brg_rhino.datastructures) <brg_rhino-datastructures>


brg_maya
--------

This is a wrapper for Maya
