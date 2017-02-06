from brg.utilities import color_to_colordict

from brg.geometry.planar import centroid_points_2d

from brg.plotters.utilities import assert_axes_dimension
from brg.plotters.utilities import width_to_dict

from brg.plotters.drawing import create_axes_2d

from brg.plotters.drawing import draw_xpoints_2d
from brg.plotters.drawing import draw_xlines_2d

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


# plot specific vertices, edges, faces
# specify text color, per label
# width per edge
# arrow per edge
# plot paths (defaults for start/end, ...)
# alternative plot functions
# add conversion functions to base class definition
# defaults for everything


class NetworkPlotter2D(object):
    """"""

    def __init__(self, network):
        self.network = network
        self.vertices_on = True
        self.edges_on = True
        self.vcolor = None
        self.ecolor = None
        self.fcolor = None
        self.vlabel = None
        self.elabel = None
        self.ewidth = None
        self.flabel = None
        self.vsize = None
        # defaults
        self.default_text_color = '#000000'
        self.default_vertex_color = '#ffffff'
        self.default_edge_color = '#000000'
        self.default_face_color = '#000000'
        self.default_edge_width = 1.0

    def plot(self, axes):
        assert_axes_dimension(axes, 2)
        # default values
        vcolor = color_to_colordict(self.vcolor, self.network.vertices(), self.default_vertex_color)
        ecolor = color_to_colordict(self.ecolor, self.network.edges(), self.default_edge_color)
        fcolor = color_to_colordict(self.fcolor, self.network.faces(), self.default_face_color)
        vlabel = self.vlabel or {}
        elabel = self.elabel or {}
        flabel = self.flabel or {}
        vsize  = self.vsize or 0.1
        ewidth = width_to_dict(self.ewidth, self.network.edges(), self.default_edge_width)
        # edges
        if self.edges_on:
            lines  = []
            colors = []
            linewidths = []
            for u, v in self.network.edges_iter():
                x  = self.network.vertex[u]['x'], self.network.vertex[v]['x']
                y  = self.network.vertex[u]['y'], self.network.vertex[v]['y']
                mp = 0.5 * (x[0] + x[1]), 0.5 * (y[0] + y[1])
                line = (x[0], y[0]), (x[1], y[1])
                lines.append(line)
                colors.append(ecolor[(u, v)])
                linewidths.append(ewidth[(u, v)])
                if (u, v) in elabel:
                    text = elabel[(u, v)]
                    axes.text(
                        mp[0],
                        mp[1],
                        text,
                        fontsize=8,
                        zorder=13,
                        ha='center',
                        va='center',
                        color=self.default_text_color,
                        backgroundcolor='#ffffff'
                    )
            coll = LineCollection(lines, linewidths=linewidths, colors=colors, zorder=10, alpha=1.0)
            axes.add_collection(coll)
        # vertices
        if self.vertices_on:
            circles    = []
            facecolors = []
            edgecolors = []
            for key, attr in self.network.vertices_iter(data=True):
                xy = attr['x'], attr['y']
                circle = Circle(xy, radius=vsize)
                circles.append(circle)
                facecolors.append(vcolor[key])
                edgecolors.append(self.default_edge_color)
                if key in vlabel:
                    text = vlabel[key]
                    axes.text(
                        xy[0],
                        xy[1],
                        text,
                        fontsize=8,
                        zorder=13,
                        ha='center',
                        va='center',
                        color=self.default_text_color
                    )
            # make a collection
            # add collection to axes
            coll = PatchCollection(circles, facecolor=facecolors, edgecolor=edgecolors, lw=0.5, alpha=1.0, zorder=12)
            axes.add_collection(coll)
        # faces
        for fkey, vertices in self.network.face.items():
            if fkey in flabel:
                c = centroid_points_2d([[self.network.vertex[key][_] for _ in 'xy'] for key in set(vertices)])
                axes.text(
                    c[0],
                    c[1],
                    fkey,
                    fontsize=8,
                    zorder=13,
                    ha='center',
                    va='center',
                    color=self.default_text_color
                )


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

    axes = create_axes_2d()

    network = Network.from_obj(brg.get_data('lines.obj'))

    plotter = NetworkPlotter2D(network)
    plotter.plot(axes)

    axes.autoscale()

    plt.show()
