"""
.. _brg_rhino.geometry:

********************************************************************************
geometry
********************************************************************************

.. module:: brg_rhino.geometry


Object-oriented wrappers for native Rhino geometry.


.. autosummary::
    :toctree: generated/

    RhinoCurve
    RhinoMesh
    RhinoPoint
    RhinoSurface

"""

from .point import RhinoPoint
from .curve import RhinoCurve
from .mesh import RhinoMesh
from .surface import RhinoSurface
