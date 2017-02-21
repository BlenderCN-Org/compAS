"""
.. _compas_rhino.numerical:

********************************************************************************
numerical
********************************************************************************

.. module:: compas_rhino.numerical


Functionality for numerical calculations directly in Rhino, without the need for
external processes. The implementations are basically convenience wrappers
around :mod:`xalglib`, which is the IronPython interface to ``alglib``, a cross-platform
numerical analysis and data processing library.

For more information, see `<www.alglib.net>`_.


linalg
======

.. currentmodule:: compas_rhino.numerical.linalg

:mod:`compas_rhino.numerical.linalg`

.. autosummary::
    :toctree: generated/


matrices
========

.. currentmodule:: compas_rhino.numerical.matrices

:mod:`compas_rhino.numerical.matrices`

.. autosummary::
    :toctree: generated/

    connectivity_matrix
    laplacian_matrix
    edgeweighted_laplacian_matrix

.. autosummary::
    :toctree: generated/

    CitQCi
    CitQCf

"""
