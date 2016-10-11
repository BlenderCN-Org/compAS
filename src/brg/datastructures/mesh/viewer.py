"""A viewer specifically geared towards meshes.

.. TODO: center the scene around the bbox of the object
.. TODO: assign functionality to arrow keys
.. TODO: create modes
.. TODO: use spacebar to start/stop

"""

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from brg.viewers.viewer import Viewer
from brg.viewers.drawing import xdraw_polygons
from brg.viewers.drawing import xdraw_lines


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 2, 2014'


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


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg
    from brg.datastructures.mesh.mesh import Mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    viewer = MeshViewer(mesh)
    viewer.setup()
    viewer.show()
