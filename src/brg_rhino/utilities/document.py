# -*- coding: utf-8 -*-
import os

import System

import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'Apache License, Version 2.0'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Sep 26, 2014'


__all__ = [
    'get_document_name',
    'get_document_filename',
    'get_document_path',
    'get_document_dirname'
]


def get_document_name():
    return rs.DocumentName()


def get_document_filename():
    return os.path.splitext(get_document_name())[0]


def get_document_path():
    return rs.DocumentPath()


def get_document_dirname():
    return os.path.dirname(get_document_path())


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
