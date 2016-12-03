import sys

from PySide.QtCore import Qt

from PySide.QtGui import QMainWindow
from PySide.QtGui import QApplication

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from brg.viewers.widgets.screen import ScreenWidget


class ViewerApp(QApplication):
    def __init__(self, mesh, subdfunc):
        QApplication.__init__(self, sys.argv)
        self.mesh = mesh
        self.subdfunc = subdfunc
        self.setApplicationName("GL Viewer Test")
        # setup
        self.setup()
        # start the app loop
        self.main.resize(1024, 768)
        self.main.show()

    def setup(self):
        self.setup_mainwindow()

    def start(self):
        sys.exit(self.exec_())

    def setup_mainwindow(self):
        self.main = QMainWindow()
        self.setup_centralwidget()
        self.setup_menubar()
        self.setup_statusbar()

    def setup_centralwidget(self):
        self.screen = screen = ScreenWidget(self.mesh, self.subdfunc)
        screen.setFocusPolicy(Qt.StrongFocus)
        screen.setFocus()
        self.main.setCentralWidget(screen)

    def setup_menubar(self):
        self.menu = menu = self.main.menuBar()
        self.main.setMenuBar(menu)
        self.add_filemenu()

    def add_filemenu(self):
        menu = self.menu.addMenu('&File')
        new_action = menu.addAction('&New')
        new_action.triggered.connect(self.do_newfile)

    def do_newfile(self):
        print('i am doing it!')

    def setup_statusbar(self):
        self.status = self.main.statusBar()
        self.main.setStatusBar(self.status)
        self.status.showMessage('test')


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from brg.datastructures.mesh.mesh import Mesh
    from brg.datastructures.mesh.algorithms.subdivision import doosabin_subdivision
    from brg.geometry.elements.polyhedron import Polyhedron

    poly = Polyhedron.generate(6)

    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    ViewerApp(mesh, subdfunc=doosabin_subdivision).start()
