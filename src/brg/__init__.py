"""
.. _brg:

********************************************************************************
brg
********************************************************************************

.. module:: brg


This is the main package of the core framework. It defines the base functionality
used by all other packages and can be used entirely standalone.


.. rubric:: Submodules

.. toctree::
    :maxdepth: 1

    brg.com
    brg.datastructures
    brg.files
    brg.geometry
    brg.numerical
    brg.physics
    brg.plotters
    brg.utilities
    brg.viewers
    brg.web
    brg.xlibs

"""

import os


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs3'))


def _find_resource(filename):
    filename = filename.strip('/')
    return os.path.abspath(os.path.join(DATA, filename))


def get_data(filename):
    return _find_resource(filename)


def get_license():
    with open(os.path.join(HOME, 'LICENSE')) as fp:
        return fp.read()


def get_requirements(rtype='list'):
    pass


__all__ = []
