from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', 'Shajay Bhooshan']
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 2, 2014'


# ==============================================================================
# draw
# ==============================================================================

def draw_points(xyz, color=None, size=1):
    color = color if color else (0.0, 0.0, 0.0)
    glColor3f(*color)
    glPointSize(size)
    glBegin(GL_POINTS)
    for x, y, z in iter(xyz):
        glVertex3f(x, y, z)
    glEnd()


def draw_lines(uv, xyz, color=None, linewidth=1):
    color = color if color else (0.0, 0.0, 0.0)
    glColor3f(*color)
    glLineWidth(linewidth)
    glBegin(GL_LINES)
    for u, v in iter(uv):
        glVertex3f(*xyz[u])
        glVertex3f(*xyz[v])
    glEnd()


def draw_faces(faces, color=None):
    color = color if color else (1.0, 0.0, 0.0, 0.5)
    glColor4f(*color)
    for face in faces:
        glBegin(GL_POLYGON)
        for xyz in face:
            glVertex3f(*xyz)
        glEnd()


def draw_sphere(r=1.):
    slices = 17
    stacks = 17
    glColor4f(0.8, 0.8, 0.8, 0.5)
    glLineWidth(0.1)
    glutWireSphere(r, slices, stacks)


# ==============================================================================
# xdraw
# ==============================================================================


def xdraw_points(points):
    for attr in points:
        pos   = attr['pos']
        color = attr['color']
        size  = attr['size']
        glColor3f(*color)
        glPointSize(size)
        glBegin(GL_POINTS)
        glVertex3f(*pos)
        glEnd()
        pass


def xdraw_lines(lines):
    for attr in lines:
        start = attr['start']
        end   = attr['end']
        color = attr['color']
        width = attr['width']
        glColor3f(*color)
        glLineWidth(width)
        glBegin(GL_LINES)
        glVertex3f(*start)
        glVertex3f(*end)
        glEnd()


def xdraw_polygons(polygons):
    for attr in polygons:
        points      = attr['points']
        color_front = attr['color.front']
        color_back  = attr['color.back']
        # front faces
        glColor4f(*color_front)
        glBegin(GL_POLYGON)
        for xyz in points:
            glVertex3f(*xyz)
        glEnd()
        # back faces
        glColor4f(*color_back)
        glBegin(GL_POLYGON)
        for xyz in points[::-1]:
            glVertex3f(*xyz)
        glEnd()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
