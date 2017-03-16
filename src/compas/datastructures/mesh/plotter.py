from compas.utilities import color_to_colordict

from compas.plotters.utilities import width_to_dict
from compas.plotters.utilities import assert_axes_dimension

from compas.plotters.drawing import create_axes_2d
from compas.plotters.drawing import draw_xpoints_2d
from compas.plotters.drawing import draw_xlines_2d
from compas.plotters.drawing import draw_xarrows_2d
from compas.plotters.drawing import draw_xpolygons_2d


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
        self.edges_on = False
        self.vcolor = None
        self.ecolor = None
        self.fcolor = None
        self.vlabel = None
        self.elabel = None
        self.flabel = None
        self.vsize  = None
        self.ewidth = None
        # additional
        self.points = None
        self.lines = None
        # defaults
        self.default_text_color = '#000000'
        self.default_vertex_color = '#ffffff'
        self.default_face_color = '#eeeeee'
        self.default_edge_color = '#333333'
        self.default_edge_width = 1.0
        self.default_vertex_size = 0.1

    def plot(self, axes):
        assert_axes_dimension(axes, 2)
        # default values
        vcolor = color_to_colordict(self.vcolor, self.mesh.vertices(), self.default_vertex_color)
        ecolor = color_to_colordict(self.ecolor, self.mesh.edges(), self.default_edge_color)
        fcolor = color_to_colordict(self.fcolor, self.mesh.faces(), self.default_face_color)
        vlabel = self.vlabel or {}
        elabel = self.elabel or {}
        flabel = self.flabel or {}
        vsize  = self.vsize or self.default_vertex_size
        ewidth = width_to_dict(self.ewidth, self.mesh.edges(), self.default_edge_width)
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
        # edges
        if self.edges_on:
            lines  = []
            for u, v in self.mesh.edges_iter():
                lines.append({
                    'start': self.mesh.vertex_coordinates(u, 'xy'),
                    'end'  : self.mesh.vertex_coordinates(v, 'xy'),
                    'text' : None if (u, v) not in elabel else str(elabel[(u, v)]),
                    'color': ecolor[(u, v)],
                    'width': ewidth[(u, v)]
                })
            draw_xlines_2d(lines, axes)
        # points
        if self.points:
            points = []
            for point in self.points:
                points.append({
                    'pos'       : point['pos'],
                    'text'      : point.get('text', ''),
                    'radius'    : point.get('size', vsize),
                    'textcolor' : point.get('textcolor', self.default_text_color),
                    'facecolor' : point.get('facecolor', self.default_vertex_color),
                    'edgecolor' : point.get('edgecolor', self.default_edge_color),
                })
            draw_xpoints_2d(points, axes)
        # lines
        if self.lines:
            lines = []
            arrows = []
            for line in self.lines:
                if line.get('arrow', None):
                    arrows.append({
                        'start': line['start'],
                        'end'  : line['end'],
                        'color': line.get('color', self.default_edge_color),
                        'width': line.get('width', self.default_edge_width),
                        'arrow': line.get('arrow', 'end')
                    })
                else:
                    lines.append({
                        'start': line['start'],
                        'end'  : line['end'],
                        'color': line.get('color', self.default_edge_color),
                        'width': line.get('width', self.default_edge_width),
                    })
            if lines:
                draw_xlines_2d(lines, axes)
            if arrows:
                draw_xarrows_2d(arrows, axes)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures.mesh import Mesh

    import matplotlib.pyplot as plt

    axes = create_axes_2d()

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    plotter = MeshPlotter2D(mesh)

    plotter.points = [{
        'pos': mesh.face_centroid(fkey),
        'text': fkey
    } for fkey in mesh.face]

    plotter.plot(axes)

    axes.autoscale()

    plt.show()
