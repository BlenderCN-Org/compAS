from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Nov 24, 2014'


# rotate around center of scene rather than around center of world
# rotate around axis perpendicular to mouse motion
# don't forget: the camera stays fixed, it is the world that moves

# http://gamedev.stackexchange.com/questions/40741/why-do-we-move-the-world-instead-of-the-camera
# http://stackoverflow.com/questions/1977737/opengl-rotations-around-world-origin-when-they-should-be-around-local-origin

# https://www.opengl.org/archives/resources/faq/technical/viewing.htm


class Camera(object):
    """"""
    def __init__(self, viewer):
        self.viewer = viewer
        self.rx = -30.0  # from y to z => pos
        self.rz = +30.0  # from x to y => pos
        self.dr = +0.5
        self.tx = +0.0
        self.ty = +0.0
        self.tz = -20.0  # move the scene away from the camera
        self.dt = +0.1

    def update(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.tx, self.ty, self.tz)
        glRotatef(self.rx, 1, 0, 0)
        glRotatef(self.rz, 0, 0, 1)

    def zoom_in(self):
        self.tz -= self.tz * self.dt

    def zoom_out(self):
        self.tz += self.tz * self.dt


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
