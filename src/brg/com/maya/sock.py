""""""

import socket


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__date__       = '2016-08-29 13:31:36'


__all__ = [
    'MayaSockError',
    'MayaSock',
]


class MayaSockError(Exception):
    pass


# see: http://download.autodesk.com/us/maya/2011help/CommandsPython/commandPort.html
# see: http://stackoverflow.com/questions/6485059/sending-multiline-commands-to-maya-through-python-socket
# see: https://docs.python.org/3/howto/sockets.html
class MayaSock(object):
    """"""

    def __init__(self):
        pass