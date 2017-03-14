from compas.utilities import color_to_colordict

from compas.plotters.utilities import assert_axes_dimension
from compas.plotters.utilities import width_to_dict

from compas.plotters.drawing import create_axes_2d

from compas.plotters.drawing import draw_xpoints_2d
from compas.plotters.drawing import draw_xlines_2d
from compas.plotters.drawing import draw_xarrows_2d
from compas.plotters.drawing import draw_xpolygons_2d

from compas.plotters.drawing import draw_points_3d
from compas.plotters.drawing import draw_lines_3d

from compas.plotters.helpers import Bounds


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
        network (compas.datastructures.network.Network): The network object.

    Attributes:
        network (compas.datastructures.network.Network):
            A network object.

        vertices_on (bool):
            Display the vertices. Default is ``True``.

        edges_on (bool):
            Display the edges. Default is ``True``.

        vertexcolor (str, tuple, dict):
            The vertex color specification.
            Default is ``None``.
            Possible values are:

                * str: A HEX color code.
                  When provided, this will be applied to all vertices.
                * tuple: A RGB color code.
                  When provided this will be applied to all vertices.
                * dict: A dictionary of HEX and/or RGB color codes.
                  When provided this will be applied to all vertices included in the dict.

        edgecolor (str, tuple, dict):
            The edge color specification.
            Default is ``None``.
            Possible values are:

                * str: A HEX color code.
                  When provided, this will be applied to all edges.
                * tuple: A RGB color code.
                  When provided this will be applied to all edges.
                * dict: A dictionary of HEX and/or RGB color codes.
                  When provided this will be applied to all edges included in the dict.

        facecolor (str, tuple, dict):
            The face color specification.
            Default is ``None``.
            Possible values are:

                * str: A HEX color code.
                  When provided, this will be applied to all faces.
                * tuple: A RGB color code.
                  When provided this will be applied to all faces.
                * dict: A dictionary of HEX and/or RGB color codes.
                  When provided this will be applied to all faces included in the dict.

        vertexlabel (dict):
            A dictionary of vertex labels.
            Default is ``None``.
            Labels are added to the plot for those vertices included in the dict.

        edgelabel (dict):
            A dictionary of edge labels.
            Default is ``None``.
            Labels are added to the plot for those edges included in the dict.

        facelabel (dict):
            A dictionary of face labels.
            Default is ``None``.
            Labels are added to the plot for those faces included in the dict.

        vertexsize (float, dict):
            The size of vertices.
            Default is ``None``.
            Possible values are:

                * float: A single size value.
                  When provided, this will be applied to all vertices.
                * dict: A dictionary of size values.
                  When provided, this will be applied to all vertices in the dict.

        edgewidth (float, dict):
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
                * size: An optional point size. Defaults to ``default_vertexsize``.
                * textcolor: Optional color specification for the label text.
                  Defaults to ``default_textcolor``.
                * facecolor: Optional color specification for the fill color of the vertex.
                  Defaults to ``default_facecolor``.
                * edgecolor: Optional color specification for the outline color of the vertex.
                  Defaults to ``default_edgecolor``.

        lines (list):
            A list of additional lines to be added to the plot.
            Each line should be defined as a dict of properties.
            The following dict structure is supported:

                * start: The XY coordinates of the start point.
                * end: The XY coordinates of the end point.
                * text: An optional label. Defaults to ``None``.
                * width: An optional linedgewidth. Defaults to ``default_edgewidth``.
                * color: Optional color specification. Defaults to ``default_edgecolor``.
                * arrow: Optional addition of arrowhead(s).
                  Possible values are ``None``, ``'start'``, ``'end'``, ``'both'``.


    Warning:
        Functionality and parameters related to faces is not properly tested and
        may be buggy.

    Example:

        .. plot::
            :include-source:

            import matplotlib.pyplot as plt

            import compas

            from compas.datastructures.network import Network
            from compas.datastructures.network.plotter import NetworkPlotter2D

            from compas.plotters.drawing import create_axes_2d

            network = Network.from_obj(compas.get_data('lines.obj'))
            plotter = NetworkPlotter2D(network)

            plotter.vertexsize  = 0.2
            plotter.vertexcolor = {key: '#ff0000' for key in network.leaves()}
            plotter.vertexlabel = {key: key for key in network}

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
        self.edges_on    = True
        self.faces_on    = False
        self.vertexcolor = None
        self.edgecolor = None
        self.facecolor = None
        self.vertexlabel = None
        self.edgelabel = None
        self.facelabel = None
        self.vertexsize  = None
        self.edgewidth = None
        self.textcolor = None
        # additional
        self.points = None
        self.lines  = None
        # defaults
        self.default_textcolor = '#000000'
        self.default_vertexcolor = '#ffffff'
        self.default_edgecolor = '#000000'
        self.default_facecolor = '#000000'
        self.default_edgewidth = 1.0
        self.default_vertexsize = 0.1
        self.default_pointcolor = '#ffffff'
        self.default_linecolor = '#000000'
        self.default_linewidth = 1.0
        self.default_pointsize = 0.1

    def plot(self, axes):
        assert_axes_dimension(axes, 2)
        # default values
        vertexcolor = color_to_colordict(self.vertexcolor, self.network.vertices_iter(), self.default_vertexcolor)
        edgecolor = color_to_colordict(self.edgecolor, self.network.edges_iter(), self.default_edgecolor)
        facecolor = color_to_colordict(self.facecolor, self.network.faces_iter(), self.default_facecolor)
        textcolor = color_to_colordict(self.textcolor, self.network.vertices_iter(), self.default_textcolor)
        vertexsize  = self.vertexsize or self.default_vertexsize  # this should be a dict
        edgewidth = width_to_dict(self.edgewidth, self.network.edges_iter(), self.default_edgewidth)
        vertexlabel = self.vertexlabel or {}
        edgelabel = self.edgelabel or {}
        facelabel = self.facelabel or {}
        # edges
        if self.edges_on:
            lines  = []
            for u, v in self.network.edges_iter():
                lines.append({
                    'start': self.network.vertex_coordinates(u, 'xy'),
                    'end'  : self.network.vertex_coordinates(v, 'xy'),
                    'text' : None if (u, v) not in edgelabel else str(edgelabel[(u, v)]),
                    'color': edgecolor[(u, v)],
                    'width': edgewidth[(u, v)]
                })
            draw_xlines_2d(lines, axes)
        # vertices
        if self.vertices_on:
            points = []
            for key, attr in self.network.vertices_iter(data=True):
                points.append({
                    'pos'       : (attr['x'], attr['y']),
                    'text'      : None if key not in vertexlabel else str(vertexlabel[key]),
                    'radius'    : vertexsize,
                    'textcolor' : textcolor[key],
                    'facecolor' : vertexcolor[key],
                    'edgecolor' : self.default_edgecolor,
                })
            draw_xpoints_2d(points, axes)
        # faces
        if self.faces_on:
            if self.network.face:
                polygons = []
                for fkey in self.network.face:
                    vertices = self.network.face_vertices(fkey)
                    if vertices[0] == vertices[-1]:
                        points = [self.network.vertex_coordinates(key, 'xy') for key in vertices[:-1]]
                    else:
                        points = [self.network.vertex_coordinates(key, 'xy') for key in vertices]
                    polygons.append({
                        'points'   : points,
                        'text'     : None if fkey not in facelabel else str(facelabel[fkey]),
                        'facecolor': facecolor[fkey],
                        'edgecolor': facecolor[fkey],
                        'textcolor': self.default_textcolor
                    })
                draw_xpolygons_2d(polygons, axes)
        # points
        if self.points:
            points = []
            for point in self.points:
                points.append({
                    'pos'       : point['pos'],
                    'text'      : point.get('text', ''),
                    'radius'    : point.get('size', self.default_pointsize),
                    'textcolor' : point.get('textcolor', self.default_textcolor),
                    'facecolor' : point.get('facecolor', self.default_pointcolor),
                    'edgecolor' : point.get('edgecolor', self.default_linecolor),
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
                        'color': line.get('color', self.default_linecolor),
                        'width': line.get('width', self.default_linewidth),
                        'arrow': line.get('arrow', 'end')
                    })
                else:
                    lines.append({
                        'start': line['start'],
                        'end'  : line['end'],
                        'color': line.get('color', self.default_linecolor),
                        'width': line.get('width', self.default_linewidth),
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
        draw_lines_3d(lines, axes, color='#000000', linedgewidth=1.0)
        draw_points_3d(points, axes, facecolor='#ffffff', edgecolor='#000000')
        bounds = Bounds(points)
        bounds.plot(axes)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures.network import Network
    from compas.plotters.drawing import create_axes_2d

    import matplotlib.pyplot as plt

    network = Network.from_obj(compas.get_data('lines.obj'))
    plotter = NetworkPlotter2D(network)

    plotter.vertexsize  = 0.2
    plotter.vertexcolor = {key: '#ff0000' for key in network.leaves()}
    plotter.vertexlabel = {key: key for key in network}

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
