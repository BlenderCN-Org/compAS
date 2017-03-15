"""
.. _compas.files:

********************************************************************************
files
********************************************************************************

.. module:: compas.files


A package for working with different types of files.


CSV
===

.. currentmodule:: compas.files.csv

:mod:`compas.files.csv`

.. autosummary::
    :toctree: generated/

    CSVReader
    CSVWriter    


OBJ
===

.. currentmodule:: compas.files.obj

:mod:`compas.files.obj`

.. autosummary::
    :toctree: generated/

    OBJ
    OBJReader
    OBJParser
    OBJComposer
    OBJWriter

"""

from .csv import CSVReader
from .csv import CSVWriter

from .obj import OBJ
from .obj import OBJReader
from .obj import OBJParser
from .obj import OBJComposer
from .obj import OBJWriter
