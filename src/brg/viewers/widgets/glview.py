import sys

try:
    from PySide.QtCore import Qt
    from PySide.QtGui import QApplication
    from PySide.QtOpenGL import QGLWidget

except ImportError:

    class QApplication(object):
        pass

    class QGLWidget(object):
        pass


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from brg.viewers.drawing import xdraw_polygons
from brg.viewers.drawing import xdraw_lines
from brg.viewers.drawing import xdraw_points


# def glDraw ()
# def glInit ()
# def initializeGL ()
# def initializeOverlayGL ()
# def paintGL ()
# def paintOverlayGL ()
# def resizeGL (w, h)
# def resizeOverlayGL (w, h)
# def updateGL ()
# def updateOverlayGL ()


class ScreenWidget(QGLWidget):
    """"""

    def __init__(self, mesh, subdfunc=None):
        QGLWidget.__init__(self)
        self.clear_color = (0.7, 0.7, 0.7, 0.0)
        self.mesh = mesh
        self.subd = None
        self.subdfunc = subdfunc
        self.fcount = len(self.mesh.faces())
        self.k_i = dict((k, i) for i, k in self.mesh.vertices_enum())

    # ==========================================================================
    # inititlisation
    # ==========================================================================

    def initializeGL(self):
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glClearColor(*self.clear_color)
        glCullFace(GL_BACK)
        glShadeModel(GL_SMOOTH)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glPolygonOffset(1.0, 1.0)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glEnable(GL_CULL_FACE)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        self.aim_camera()
        self.focus_camera()

    def init(self):
        pass

    # ==========================================================================
    # camera
    # ==========================================================================

    def aim_camera(self):
        gluLookAt(0, 0, -10, 0, 0, 0, 0, 1, 0)

    def focus_camera(self):
        glPushAttrib(GL_TRANSFORM_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        fov = 60.0
        asp = self.width() / self.height()
        ner = 1.0
        far = 100.0
        gluPerspective(fov, asp, ner, far)
        glPopAttrib()

    # ==========================================================================
    # axes
    # ==========================================================================

    def draw_axes(self):
        x_color = 1.0, 0.0, 0.0
        y_color = 0.0, 1.0, 0.0
        z_color = 0.0, 0.0, 1.0
        glLineWidth(3)
        glBegin(GL_LINES)
        glColor3f(* x_color)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glColor3f(* y_color)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        glColor3f(* z_color)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glEnd()

    # ==========================================================================
    # paint callback
    # ==========================================================================

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushAttrib(GL_POLYGON_BIT)
        self.paint()
        glPopAttrib()
        glutSwapBuffers()

    def paint(self):
        xyz   = [self.mesh.vertex_coordinates(key) for key in self.mesh]
        lines = []
        for u, v in self.mesh.edges_iter():
            lines.append({'start' : xyz[self.k_i[u]],
                          'end'   : xyz[self.k_i[v]],
                          'color' : (0.1, 0.1, 0.1),
                          'width' : 1.})
        points = []
        for key in self.mesh:
            points.append({'pos'   : xyz[self.k_i[key]],
                           'color' : (0.0, 1.0, 0.0),
                           'size'  : 10.0})
        xdraw_lines(lines)
        xdraw_points(points)
        if self.subd:
            k_i   = dict((k, i) for i, k in self.subd.vertices_enum())
            xyz   = [self.subd.vertex_coordinates(key) for key in self.subd]
            faces = [self.subd.face_vertices(fkey, True) for fkey in self.subd.face]
            faces = [[xyz[k_i[key]] for key in vertices] for vertices in faces]
            front = (0.7, 0.7, 0.7, 1.0)
            back  = (0.2, 0.2, 0.2, 1.0)
            poly  = []
            for points in faces:
                poly.append({'points'     : points,
                             'color.front': front,
                             'color.back' : back})
            lines = []
            for u, v in self.subd.edges_iter():
                lines.append({'start': xyz[k_i[u]],
                              'end'  : xyz[k_i[v]],
                              'color': (0.1, 0.1, 0.1),
                              'width': 1.})
            xdraw_polygons(poly)
            xdraw_lines(lines)

    # ==========================================================================
    # resize callback
    # ==========================================================================

    def resizeGl(self, w, h):
        glViewport(0, 0, w, h)
        self.focus_camera()

    # ==========================================================================
    # mouse events
    # ==========================================================================

    def mouseMoveEvent(self, event):
        p = event.pos()
        print('@')
        print(p)

    def mousePressEvent(self, event):
        p = event.pos()
        print('press @')
        print(p)

    def mouseReleaseEvent(self, event):
        p = event.pos()
        print('release @')
        print(p)

    # ==========================================================================
    # keyboard events
    # ==========================================================================

    def keyPressEvent(self, event):
        super(ScreenWidget, self).keyPressEvent(event)
        key = event.key()
        if key == Qt.Key_1:
            self.subd = self.subdfunc(self.mesh, k=1)
        if key == Qt.Key_2:
            self.subd = self.subdfunc(self.mesh, k=2)
        if key == Qt.Key_3:
            self.subd = self.subdfunc(self.mesh, k=3)
        if key == Qt.Key_4:
            self.subd = self.subdfunc(self.mesh, k=4)
        if key == Qt.Key_5:
            self.subd = self.subdfunc(self.mesh, k=5)
        self.updateGL()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from brg.datastructures.mesh.mesh import Mesh
    from brg.datastructures.mesh.algorithms.subdivision import doosabin_subdivision
    from brg.geometry.elements.polyhedron import Polyhedron

    poly = Polyhedron.generate(6)

    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    app = QApplication(sys.argv)

    screen = ScreenWidget(mesh, subdfunc=doosabin_subdivision)
    screen.show()

    sys.exit(app.exec_())
