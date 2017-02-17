from brg.utilities import color_to_colordict

from brg.geometry.planar import centroid_points_2d

from brg.plotters.utilities import assert_axes_dimension
from brg.plotters.utilities import width_to_dict

from brg.plotters.drawing import create_axes_2d

from brg.plotters.drawing import draw_xpoints_2d
from brg.plotters.drawing import draw_xlines_2d
from brg.plotters.drawing import draw_xarrows_2d

from brg.plotters.drawing import draw_points_3d
from brg.plotters.drawing import draw_lines_3d

from brg.plotters.helpers import Bounds

from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
from matplotlib.collections import LineCollection


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'NetworkPlotter2D',
    'NetworkPlotter3D',
]


class NetworkPlotter2D(object):
    """Plotter for 2D networks.

    Parameters:
        network (brg.datastructures.network.Network): The network object.

    Attributes:
        network (brg.datastructures.network.Network):
            A network object.

        vertices_on (bool):
            Display the vertices. Default is ``True``.

        edges_on (bool):
            Display the edges. Default is ``True``.

        vcolor (str, tuple, dict):
            The vertex color specification.
            Default is ``None``.
            Possible values are:

                * str: A HEX color code.
                  When provided, this will be applied to all vertices.
                * tuple: A RGB color code.
                  When provided this will be applied to all vertices.
                * dict: A dictionary of HEX and/or RGB color codes.
                  When provided this will be applied to all vertices included in the dict.

        ecolor (str, tuple, dict):
            The edge color specification.
            Default is ``None``.
            Possible values are:

                * str: A HEX color code.
                  When provided, this will be applied to all edges.
                * tuple: A RGB color code.
                  When provided this will be applied to all edges.
                * dict: A dictionary of HEX and/or RGB color codes.
                  When provided this will be applied to all edges included in the dict.

        fcolor (str, tuple, dict):
            The face color specification.
            Default is ``None``.
            Possible values are:

                * str: A HEX color code.
                  When provided, this will be applied to all faces.
                * tuple: A RGB color code.
                  When provided this will be applied to all faces.
                * dict: A dictionary of HEX and/or RGB color codes.
                  When provided this will be applied to all faces included in the dict.

        vlabel (dict):
            A dictionary of vertex labels.
            Default is ``None``.
            Labels are added to the plot for those vertices included in the dict.

        elabel (dict):
            A dictionary of edge labels.
            Default is ``None``.
            Labels are added to the plot for those edges included in the dict.

        flabel (dict):
            A dictionary of face labels.
            Default is ``None``.
            Labels are added to the plot for those faces included in the dict.

        vsize (float, dict):
            The size of vertices.
            Default is ``None``.
            Possible values are:

                * float: A single size value.
                  When provided, this will be applied to all vertices.
                * dict: A dictionary of size values.
                  When provided, this will be applied to all vertices in the dict.

        ewidth (float, dict):
            The width of the edges.
            Default is ``None``.
            Possible values are:

                * float: A single width value.
                  When provided, this will be applied to all edges.
                * dict: A dictionary of width values.
                  When provided, this will be applied to all edges in the dict.

        points (list):
            A list of additional points to be added to the plot.
            Each point should be defined as a dict of properties.
            The following dict structure is supported:

                * pos: The XY coordinates of the point.
                * text: An optional label. Defaults to ``None``.
                * size: An optional point size. Defaults to ``default_vertex_size``.
                * textcolor: Optional color specification for the label text.
                  Defaults to ``default_text_color``.
                * facecolor: Optional color specification for the fill color of the vertex.
                  Defaults to ``default_face_color``.
                * edgecolor: Optional color specification for the outline color of the vertex.
                  Defaults to ``default_edge_color``.

        lines (list):
            A list of additional lines to be added to the plot.
            Each line should be defined as a dict of properties.
            The following dict structure is supported:

                * start: The XY coordinates of the start point.
                * end: The XY coordinates of the end point.
                * text: An optional label. Defaults to ``None``.
                * width: An optional linewidth. Defaults to ``default_edge_width``.
                * color: Optional color specification. Defaults to ``default_edge_color``.
                * arrow: Optional addition of arrowhead(s).
                  Possible values are ``None``, ``'start'``, ``'end'``, ``'both'``.


    Warning:
        Functionality and parameters related to faces is not properly tested and
        may be buggy.

    Example:

        .. plot::
            :include-source:

            import matplotlib.pyplot as plt

            import brg

            from brg.datastructures.network import Network
            from brg.datastructures.network.plotter import NetworkPlotter2D

            from brg.plotters.drawing import create_axes_2d

            network = Network.from_obj(brg.get_data('lines.obj'))
            plotter = NetworkPlotter2D(network)

            plotter.vsize  = 0.2
            plotter.vcolor = {key: '#ff0000' for key in network.leaves()}
            plotter.vlabel = {key: key for key in network}

            plotter.lines = [{
                'start': network.vertex_coordinates(u, 'xy'),
                'end'  : network.vertex_coordinates(v, 'xy'),
                'color': '#00ff00',
                'width': 4.0,
                'arrow': 'end'
            } for u, v in network.connected_edges(28)]

            axes = create_axes_2d()

            plotter.plot(axes)

            axes.autoscale()

            plt.show()

    """

    def __init__(self, network):
        self.network = network
        self.vertices_on = True
        self.edges_on = True
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
        self.lines  = None
        # defaults
        self.default_text_color = '#000000'
        self.default_vertex_color = '#ffffff'
        self.default_edge_color = '#000000'
        self.default_face_color = '#000000'
        self.default_edge_width = 1.0
        self.default_vertex_size = 0.1

    def plot(self, axes):
        assert_axes_dimension(axes, 2)
        # default values
        vcolor = color_to_colordict(self.vcolor, self.network.vertices(), self.default_vertex_color)
        ecolor = color_to_colordict(self.ecolor, self.network.edges(), self.default_edge_color)
        # fcolor = color_to_colordict(self.fcolor, self.network.faces(), self.default_face_color)
        vlabel = self.vlabel or {}
        elabel = self.elabel or {}
        flabel = self.flabel or {}
        vsize  = self.vsize or self.default_vertex_size
        ewidth = width_to_dict(self.ewidth, self.network.edges(), self.default_edge_width)
        # edges
        if self.edges_on:
            lines  = []
            for u, v in self.network.edges_iter():
                lines.append({
                    'start': self.network.vertex_coordinates(u, 'xy'),
                    'end'  : self.network.vertex_coordinates(v, 'xy'),
                    'text' : None if (u, v) not in elabel else str(elabel[(u, v)]),
                    'color': ecolor[(u, v)],
                    'width': ewidth[(u, v)]
                })
            draw_xlines_2d(lines, axes)
        # vertices
        if self.vertices_on:
            points = []
            for key, attr in self.network.vertices_iter(data=True):
                points.append({
                    'pos'       : (attr['x'], attr['y']),
                    'text'      : None if key not in vlabel else str(vlabel[key]),
                    'radius'    : vsize,
                    'textcolor' : self.default_text_color,
                    'facecolor' : vcolor[key],
                    'edgecolor' : self.default_edge_color,
                })
            draw_xpoints_2d(points, axes)
        # faces
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


class NetworkPlotter3D(object):
    """"""

    def __init__(self, network):
        self.network = network

    def plot(self, axes):
        assert_axes_dimension(axes, 3)
        key_index = self.network.key_index()
        points = [self.network.vertex_coordinates(key) for key in self.network]
        lines = [(points[key_index[u]], points[key_index[v]]) for u, v in self.network.edges_iter()]
        draw_lines_3d(lines, axes, color='#000000', linewidth=1.0)
        draw_points_3d(points, axes, facecolor='#ffffff', edgecolor='#000000')
        bounds = Bounds(points)
        bounds.plot(axes)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg

    from brg.datastructures.network import Network
    from brg.plotters.drawing import create_axes_2d

    import matplotlib.pyplot as plt

    network = Network.from_obj(brg.get_data('lines.obj'))
    plotter = NetworkPlotter2D(network)

    plotter.vsize  = 0.2
    plotter.vcolor = {key: '#ff0000' for key in network.leaves()}
    plotter.vlabel = {key: key for key in network}

    plotter.lines = [{
        'start': network.vertex_coordinates(u, 'xy'),
        'end'  : network.vertex_coordinates(v, 'xy'),
        'color': '#00ff00',
        'width': 4.0,
        'arrow': 'end'
    } for u, v in network.connected_edges(28)]

    axes = create_axes_2d()

    plotter.plot(axes)

    axes.autoscale()

    plt.show()
