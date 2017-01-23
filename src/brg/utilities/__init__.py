"""
.. _brg.utilities:

********************************************************************************
utilities
********************************************************************************

.. module:: brg.utilities

:mod:`brg.utilities`


_datetime
=========

.. currentmodule:: brg.utilities._datetime

:mod:`brg.utilities._datetime`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    timestamp


colors
======

.. currentmodule:: brg.utilities.colors

:mod:`brg.utilities.colors`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    i_to_rgb
    i_to_red
    i_to_green
    i_to_blue
    i_to_white
    i_to_black
    rgb_to_hex
    color_to_colordict
    color_to_rgb


maps
====

.. currentmodule:: brg.utilities.maps

:mod:`brg.utilities.maps`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    geometric_key
    geometric_key2


mixing
======

.. currentmodule:: brg.utilities.mixing

:mod:`brg.utilities.mixing`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    mix_in_functions
    mix_in_class_attributes


names
=====

.. currentmodule:: brg.utilities.names

:mod:`brg.utilities.names`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    random_name


profiling
=========

.. currentmodule:: brg.utilities.profiling

:mod:`brg.utilities.profiling`

.. rubric:: Functions

.. autosummary::
    :toctree: generated/

    print_profile


scripts
=======

.. currentmodule:: brg.utilities.scripts

:mod:`brg.utilities.scripts`

.. rubric:: Classes

.. autosummary::
    :toctree: generated/

    ScriptServer


xfunc
=====

.. currentmodule:: brg.utilities.xfunc

:mod:`brg.utilities.xfunc`

.. rubric:: Classes

.. autosummary::
    :toctree: generated/
    
    XFunc


xfuncio
=======

.. currentmodule:: brg.utilities.xfuncio

:mod:`brg.utilities.xfuncio`

.. rubric:: Classes

.. autosummary::
    :toctree: generated/
    
    XFuncIO


"""

from ._datetime import *
from .colors import *
from .maps import *
from .mixing import *
from .names import *
# from .profiling import *
from .scripts import *
from .xfunc import *
from .xfuncio import *
