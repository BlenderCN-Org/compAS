"""
.. _brg.files:

********************************************************************************
files
********************************************************************************

.. module:: brg.files

:mod:`brg.files`

A package for working with different types of files.


CSV
===

.. currentmodule:: brg.files.csv

:mod:`brg.files.csv`

.. rubric:: Classes

.. autosummary::
    :toctree: generated/

    CSVReader
    CSVWriter    


OBJ
===

.. currentmodule:: brg.files.obj

:mod:`brg.files.obj`

.. rubric:: Classes

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
