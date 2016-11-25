from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 24, 2014'


class Mouse(object):
    """"""
    def __init__(self, viewer):
        self.viewer  = viewer
        self.buttons = [False, False, False, False, False]
        self.x       = 0.0
        self.y       = 0.0
        self.x_last  = 0.0
        self.y_last  = 0.0


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
