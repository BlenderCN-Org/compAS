.. _api:

********************************************************************************
API Reference
********************************************************************************

The Block Research Group (BRG) framework is a set of Python packages for
computational architectural geometry, structural design, and fabrication.

The framework consists of a core that can be extended with special-purpose
packages targeting specific areas in ...


.. rubric:: Core

The core framework consists of a main package (:mod:`brg`) that defines the base
functionality of the framework, and several wrapper
(:mod:`brg_rhino`, :mod:`brg_gh`, :mod:`brg_blender`, ...) that integrate the
framework with different CAD environments.


.. toctree::
	:maxdepth: 1

	reference/brg
	reference/brg_rhino
	reference/brg_gh
	reference/brg_blender


.. rubric:: Special packages

Currently, the following add-ons are publicly available:

.. toctree::
	:maxdepth: 1

	brg_ags
	brg_fea
	brg_tna
