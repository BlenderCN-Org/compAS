
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from brg.viewers.viewer import Viewer
from brg.viewers.drawing import xdraw_points
from brg.viewers.drawing import xdraw_lines


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 2, 2014'


class NetworkViewer(Viewer):
    """"""
    def __init__(self, network, width=1280, height=800):
        super(NetworkViewer, self).__init__(width=width, height=height)
        self.network = network
        self.vcount = len(self.network.vertices())

    # --------------------------------------------------------------------------
    # main drawing functionality
    # --------------------------------------------------------------------------

    def display(self):
        points  = []
        r, g, b = self.network.attributes['color.vertex']
        color   = r / 255., g / 255., b / 255.
        for key, attr in self.network.vertices_iter(True):
            points.append({
                'pos'  : (attr['x'], attr['y'], attr['z']),
                'size' : 10.,
                'color': color,
            })
        lines = []
        r, g, b = self.network.attributes['color.edge']
        color   = r / 255., g / 255., b / 255.
        for u, v in self.network.edges_iter():
            lines.append({
                'start': self.network.vertex_coordinates(u),
                'end'  : self.network.vertex_coordinates(v),
                'color': color,
                'width': 1.
            })
        xdraw_points(points)
        xdraw_lines(lines)

    # --------------------------------------------------------------------------
    # keyboard functionality
    # --------------------------------------------------------------------------

    def keypress(self, key, x, y):
        """Assign network functionality to keys.
        """
        pass

    def special(self, key, x, y):
        """Define the meaning of pressing function keys.
        """
        pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg
    from brg.datastructures.network.network import Network

    network = Network.from_obj(brg.get_data('lines.obj'))

    viewer = NetworkViewer(network)
    viewer.setup()
    viewer.show()
