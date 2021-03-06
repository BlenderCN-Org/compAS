import os
import compas

from compas.viewers.viewer import Viewer
from compas.viewers.drawing import xdraw_polygons
from compas.viewers.drawing import xdraw_lines
from compas.viewers.drawing import xdraw_points


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
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
        if key == 'c':
            self.screenshot(os.path.join(compas.TEMP, 'screenshot.jpg'))
            return

    def special(self, key, x, y):
        """
        Assign mesh functionality to function keys.
        """
        pass


class SubdMeshViewer(Viewer):
    """Viewer for subdivision meshes.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The *control* mesh object.
        subdfunc (callable): The subdivision algorithm/scheme.
        width (int): Optional. Width of the viewport. Default is ``1440``.
        height (int): Optional. Height of the viewport. Default is ``900``.

    Warning:
        Not properly tested on meshes with a boundary.

    Example:

        .. code-block:: python

            from compas.datastructures.mesh.mesh import Mesh
            from compas.datastructures.mesh.algorithms import subdivide_mesh_doosabin
            from compas.datastructures.mesh.viewer import SubdMeshViewer

            from compas.geometry.elements.polyhedron import Polyhedron

            poly = Polyhedron.generate(6)

            mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

            viewer = SubdMeshViewer(mesh, subdfunc=subdivide_mesh_doosabin, width=600, height=600)

            viewer.axes_on = False
            viewer.grid_on = False

            for i in range(10):
                viewer.camera.zoom_in()

            viewer.setup()
            viewer.show()

    """

    def __init__(self, mesh, subdfunc, width=1440, height=900):
        super(SubdMeshViewer, self).__init__(width=width, height=height)
        self.mesh = mesh
        self.subdfunc = subdfunc
        self.subd = None  # make read-only
        self.fcount = len(self.mesh.faces())  # make protected
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
        if key == '5':
            self.subd = self.subdfunc(self.mesh, k=5)
        if key == 'c':
            self.screenshot(os.path.join(compas.TEMP, 'screenshot.jpg'))

    def subdivide(self, k=1):
        self.subd = self.subdfunc(self.mesh, k=k)


class MultiMeshViewer(Viewer):
    """"""

    def __init__(self, meshes, colors, width=1440, height=900):
        super(MultiMeshViewer, self).__init__(width=width, height=height)
        self.meshes = meshes
        self.colors = colors

    def display(self):
        for i in range(len(self.meshes)):
            mesh = self.meshes[i]
            key_index = mesh.key_index()
            xyz = [mesh.vertex_coordinates(key) for key in mesh.vertex]
            faces = [mesh.face_vertices(fkey, True) for fkey in mesh.face]
            faces = [[xyz[key_index[key]] for key in vertices] for vertices in faces]
            polygons = []
            for points in faces:
                color_front = self.colors[i]
                color_back  = (0.2, 0.2, 0.2, 1.0)
                polygons.append({'points': points,
                                 'color.front': color_front,
                                 'color.back' : color_back})
            lines = []
            for u, v in mesh.edges():
                lines.append({'start': mesh.vertex_coordinates(u),
                              'end'  : mesh.vertex_coordinates(v),
                              'color': (0.1, 0.1, 0.1),
                              'width': 1.})
            xdraw_polygons(polygons)
            xdraw_lines(lines)

    def keypress(self, key, x, y):
        pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures.mesh.mesh import Mesh
    from compas.datastructures.mesh.algorithms import subdivide_mesh_doosabin
    from compas.datastructures.mesh.viewer import SubdMeshViewer

    from compas.geometry.elements.polyhedron import Polyhedron

    poly = Polyhedron.generate(6)

    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    viewer = SubdMeshViewer(mesh, subdfunc=subdivide_mesh_doosabin, width=600, height=600)

    viewer.axes_on = False
    viewer.grid_on = False

    for i in range(10):
        viewer.camera.zoom_in()

    viewer.setup()
    viewer.show()
