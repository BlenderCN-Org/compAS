
__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Jul 8, 2015'


__all__ = [
    'MeshError',
]


class MeshError(Exception):
    pass


class MeshKeyError(MeshError):
    pass


class MeshFaceError(MeshError):
    pass
