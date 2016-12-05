"""Specialised plotters for matplotlib."""

from numpy import asarray
from numpy import argmax
from numpy import argmin
from numpy import zeros

from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from brg.datastructures.network.utilities.drawing import draw_points
from brg.datastructures.network.utilities.drawing import draw_lines


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


def draw_points(points, axes=None, alpha=1.0, zorder=1010):
    if not axes:
        axes = plt.gca()
    circles = []
    fcolors = []
    ecolors = []
    lwidths = []
    for point in points:
        xy = point['pos']
        r  = point['radius']
        fc = point.get('facecolor') or '#ffffff'
        ec = point.get('edgecolor') or '#000000'
        lw = point.get('linewidth') or 1.0
        circles.append(Circle(xy, radius=r))
        fcolors.append(fc)
        ecolors.append(ec)
        lwidths.append(lw)
    coll = PatchCollection(circles,
                           linewidths=lwidths,
                           facecolor=fcolors,
                           edgecolor=ecolors,
                           alpha=alpha,
                           zorder=zorder)
    axes.add_collection(coll)


def draw_lines(lines, axes=None, alpha=1.0, zorder=1001):
    if not axes:
        axes = plt.gca()
    fromto = []
    widths = []
    colors = []
    for line in lines:
        sp    = line['start']
        ep    = line['end']
        width = line.get('width') or 1.0
        color = line.get('color') or '#000000'
        fromto.append((sp, ep))
        widths.append(width)
        colors.append(color)
    coll = Line3DCollection(fromto,
                            linewidths=widths,
                            colors=colors,
                            alpha=alpha,
                            zorder=zorder)
    axes.add_collection(coll)


class Axes2(object):
    """"""

    def __init__(self, origin, vectors):
        self.origin = asarray(origin)
        self.vectors = asarray(vectors)

    def plot(self, axes):
        o = self.origin
        xy = self.vectors
        axes.plot(
            [o[0, 0], o[0, 0] + xy[0, 0]],
            [o[0, 1], o[0, 1] + xy[0, 1]],
            'r-'
        )
        axes.plot(
            [o[0, 0], o[0, 0] + xy[1, 0]],
            [o[0, 1], o[0, 1] + xy[1, 1]],
            'g-'
        )


class Cloud2(object):
    pass


class Axes3(object):
    def __init__(self, origin, vectors):
        self.origin = asarray(origin)
        self.vectors = asarray(vectors)

    def plot(self, axes):
        o = self.origin
        xyz = self.vectors
        axes.plot(
            [o[0, 0], o[0, 0] + xyz[0, 0]],
            [o[0, 1], o[0, 1] + xyz[0, 1]],
            [o[0, 2], o[0, 2] + xyz[0, 2]],
            'r-',
            linewidth=3
        )
        axes.plot(
            [o[0, 0], o[0, 0] + xyz[1, 0]],
            [o[0, 1], o[0, 1] + xyz[1, 1]],
            [o[0, 2], o[0, 2] + xyz[1, 2]],
            'g-',
            linewidth=3
        )
        axes.plot(
            [o[0, 0], o[0, 0] + xyz[2, 0]],
            [o[0, 1], o[0, 1] + xyz[2, 1]],
            [o[0, 2], o[0, 2] + xyz[2, 2]],
            'b-',
            linewidth=3
        )


class Bounds3(object):
    """"""
    def __init__(self, points):
        self.points = asarray(points)

    def plot(self, axes):
        xmin, ymin, zmin = argmin(self.points, axis=0)
        xmax, ymax, zmax = argmax(self.points, axis=0)
        xspan = self.points[xmax, 0] - self.points[xmin, 0]
        yspan = self.points[ymax, 1] - self.points[ymin, 1]
        zspan = self.points[zmax, 2] - self.points[zmin, 2]
        span = max(xspan, yspan, zspan)
        axes.plot([self.points[xmin, 0]], [self.points[ymin, 1]], [self.points[zmin, 2]], 'w')
        axes.plot([self.points[xmin, 0] + span], [self.points[ymin, 1] + span], [self.points[zmin, 2] + span], 'w')


class Cloud3(object):
    """"""

    def __init__(self, cloud):
        cloud = asarray(cloud)
        self.cloud = zeros((cloud.shape[0], 3))
        self.cloud[:, :cloud.shape[1]] = cloud

    def plot(self, axes):
        x = self.cloud[:, 0]
        y = self.cloud[:, 1]
        z = self.cloud[:, 2]
        axes.plot(x, y, z, 'o', color=(1.0, 1.0, 1.0))


class Hull3(object):
    """"""
    def __init__(self, hull):
        self.vertices = hull.points
        self.faces = hull.simplices

    def plot(self, axes):
        tri = [[self.vertices[index] for index in face] for face in self.faces]
        tri_coll = Poly3DCollection(tri)
        tri_coll.set_facecolors([(0.0, 1.0, 0.0) for face in self.faces])
        axes.add_collection3d(tri_coll)


class Box3(object):
    """"""
    def __init__(self, corners):
        self.corners = corners
        self.faces = [[0, 1, 2, 3], [4, 7, 6, 5], [1, 5, 6, 2], [0, 4, 5, 1], [0, 3, 7, 4], [2, 6, 7, 3]]

    def plot(self, axes):
        rec = [[self.corners[index] for index in face] for face in self.faces]
        rec_coll = Poly3DCollection(rec)
        rec_coll.set_facecolors([(1.0, 0.0, 0.0) for face in self.faces])
        rec_coll.set_alpha(0.2)
        axes.add_collection3d(rec_coll)


class Network3(object):
    """"""

    def __init__(self, network):
        self.network = network

    def plot(self, axes):
        lines = []
        for u, v in self.network.edges_iter():
            lines.append({
                'start' : self.network.vertex_coordinates(u),
                'end'   : self.network.vertex_coordinates(v),
                'width' : 1.0,
                'color' : '#000000'
            })
        draw_lines(lines, axes)
        points = [self.network.vertex_coordinates(key) for key in self.network if self.network.vertex[key]['is_anchor']]
        Cloud3(points).plot(axes)


class Mesh3(object):
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
