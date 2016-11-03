from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from brg.viewers.viewer import Viewer
from brg.viewers.drawing import xdraw_polygons
from brg.viewers.drawing import xdraw_lines
from brg.viewers.drawing import xdraw_points


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


class MeshViewer(Viewer):
    """"""

    def __init__(self, mesh, width=1440, height=900):
        super(MeshViewer, self).__init__(width=width, height=height)
        self.mesh = mesh
        self.fcount = len(self.mesh.faces())

    def display(self):
        key_index = dict((key, index) for index, key in self.mesh.vertices_enum())
        xyz = [self.mesh.vertex_coordinates(key) for key in self.mesh.vertex]
        faces = [self.mesh.face_vertices(fkey, True) for fkey in self.mesh.face]
        faces = [[xyz[key_index[key]] for key in vertices] for vertices in faces]
        polygons = []
        for points in faces:
            color_front = (0.7, 0.7, 0.7, 1.0)
            color_back  = (0.2, 0.2, 0.2, 1.0)
            polygons.append({'points': points,
                             'color.front': color_front,
                             'color.back' : color_back})
        lines = []
        for u, v in self.mesh.edges():
            lines.append({'start': self.mesh.vertex_coordinates(u),
                          'end'  : self.mesh.vertex_coordinates(v),
                          'color': (0.1, 0.1, 0.1),
                          'width': 1.})
        xdraw_polygons(polygons)
        xdraw_lines(lines)

    def keypress(self, key, x, y):
        """
        Assign mesh functionality to keys.

        The following keys have a mesh function assigned to them:
            * u: unify cycle directions
            * f: flip cycle directions
            * s: subdivide using quad subdivision
        """
        if key == 'u':
            self.mesh.unify_cycles()
            return
        if key == 'f':
            self.mesh.flip_cycles()
            return
        if key == 's':
            self.mesh.subdivide('quad')
            return

    def special(self, key, x, y):
        """
        Assign mesh functionality to function keys.
        """
        pass


class SubdMeshViewer(Viewer):
    """"""

    def __init__(self, mesh, subdfunc, width=1440, height=900):
        super(SubdMeshViewer, self).__init__(width=width, height=height)
        self.mesh = mesh
        self.subd = None
        self.subdfunc = subdfunc
        self.fcount = len(self.mesh.faces())
        self.k_i = dict((k, i) for i, k in self.mesh.vertices_enum())

    def display(self):
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
        # the subd mesh
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

    def keypress(self, key, x, y):
        if key == '1':
            self.subd = self.subdfunc(self.mesh, k=1)
        if key == '2':
            self.subd = self.subdfunc(self.mesh, k=2)
        if key == '3':
            self.subd = self.subdfunc(self.mesh, k=3)
        if key == '4':
            self.subd = self.subdfunc(self.mesh, k=4)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from brg.datastructures.mesh.mesh import Mesh
    from brg.datastructures.mesh.algorithms.subdivision import doosabin_subdivision
    from brg.geometry.elements.polyhedron import Polyhedron

    poly = Polyhedron.generate(6)

    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    viewer = SubdMeshViewer(mesh, subdfunc=doosabin_subdivision)

    viewer.axes.x_color = (0.1, 0.1, 0.1)
    viewer.axes.y_color = (0.1, 0.1, 0.1)
    viewer.axes.z_color = (0.1, 0.1, 0.1)

    viewer.setup()
    viewer.show()
