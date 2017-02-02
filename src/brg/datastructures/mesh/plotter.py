from brg.utilities import color_to_colordict

from brg.plotters.utilities import assert_axes_dimension

from brg.plotters.drawing import create_axes_2d
from brg.plotters.drawing import draw_xpoints_2d
from brg.plotters.drawing import draw_xpolygons_2d


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'MeshPlotter2D',
]


class MeshPlotter2D(object):
    """"""

    def __init__(self, mesh):
        self.mesh = mesh
        self.vertices_on = True
        self.faces_on = True
        self.vcolor = None
        self.fcolor = None
        self.vlabel = None
        self.flabel = None
        self.vsize = None
        # defaults
        self.default_text_color = '#000000'
        self.default_vertex_color = '#ffffff'
        self.default_face_color = '#eeeeee'
        self.default_edge_color = '#333333'

    def plot(self, axes):
        assert_axes_dimension(axes, 2)
        # default values
        vcolor = color_to_colordict(self.vcolor, self.mesh.vertices(), self.default_vertex_color)
        fcolor = color_to_colordict(self.fcolor, self.mesh.faces(), self.default_face_color)
        vlabel = self.vlabel or {}
        flabel = self.flabel or {}
        vsize  = self.vsize or 0.15
        # vertices
        if self.vertices_on:
            points = []
            for key in self.mesh:
                xy   = self.mesh.vertex_coordinates(key, 'xy')
                text = None if key not in vlabel else vlabel[key]
                points.append({
                    'pos'       : xy,
                    'text'      : text,
                    'radius'    : vsize,
                    'textcolor' : self.default_text_color,
                    'facecolor' : vcolor[key],
                    'edgecolor' : self.default_edge_color,
                })
            draw_xpoints_2d(points, axes)
        # faces
        if self.faces_on:
            polygons = []
            for fkey in self.mesh.face:
                points = [self.mesh.vertex_coordinates(key, 'xy') for key in self.mesh.face_vertices(fkey, ordered=True)]
                text   = None if fkey not in flabel else flabel[fkey]
                polygons.append({
                    'points'    : points,
                    'text'      : text,
                    'textcolor' : self.default_text_color,
                    'facecolor' : fcolor[fkey],
                    'edgecolor' : self.default_edge_color,
                })
            draw_xpolygons_2d(polygons, axes)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg
    from brg.datastructures.mesh import Mesh

    import matplotlib.pyplot as plt

    axes = create_axes_2d()

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    plotter = MeshPlotter2D(mesh)
    plotter.plot(axes)

    axes.autoscale()

    plt.show()
