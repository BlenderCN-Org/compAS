from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 24, 2014'


class Grid(object):
    """"""
    def __init__(self):
        self.xlim = -10, 10
        self.ylim = -10, 10
        self.linewidth = 1
        self.color = (0, 0, 0)
        self.dotted = True

    def draw(self):
        glColor3f(*self.color)
        glLineWidth(self.linewidth)
        if self.dotted:
            glEnable(GL_LINE_STIPPLE)
            glLineStipple(1, 0xAAAA)
        glBegin(GL_LINES)
        for i in xrange(self.xlim[0], self.xlim[1] + 1):
            glVertex3f(i, self.ylim[0], 0)
            glVertex3f(i, self.ylim[1], 0)
        for i in xrange(self.ylim[0], self.ylim[1] + 1):
            glVertex3f(self.xlim[0], i, 0)
            glVertex3f(self.xlim[1], i, 0)
        glEnd()
        if self.dotted:
            glDisable(GL_LINE_STIPPLE)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
