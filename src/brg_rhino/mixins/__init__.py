"""
.. _brg_rhino.mixins:

********************************************************************************
mixins
********************************************************************************

.. module:: brg_rhino.mixins


Mixins make it easier to add functionality to custom implementations of
datastructure classes.

.. seealso::

    :mod:`brg_rhino.helpers`


.. autosummary::
    :toctree: generated/

    UpdateMeshAttributes
    UpdateNetworkAttributes
    MeshConstructors
    NetworkConstructors
    MeshDrawing
    NetworkDrawing
    DisplayMeshForces
    DisplayNetworkForces
    EditMeshGeometry
    EditNetworkGeometry
    DisplayMeshLabels
    DisplayNetworkLabels
    MeshSelect
    NetworkSelect

"""


class Mixin(object):
    """"""
    pass


from .attributes import *
from .constructors import *
from .drawing import *
from .forces import *
from .geometry import *
from .labels import *
from .selection import *
