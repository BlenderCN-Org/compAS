"""Basic two-dimensional drawing functionality for networks based on Matplotlib."""


import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection, LineCollection

from brg.geometry import centroid
from brg.utilities import color_to_colordict


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BRG - ETH Zurich'
__license__    = 'MIT'
__email__      = '<vanmelet@ethz.ch>'


DEFAULT_TEXT_COLOR   = '#000000'
DEFAULT_VERTEX_COLOR = '#ffffff'
DEFAULT_EDGE_COLOR   = '#333333'
DEFAULT_FACE_COLOR   = '#eeeeee'

DEFAULT_EDGE_WIDTH   = 1.0


# ==============================================================================
# helpers
# ==============================================================================


def width_to_dict(width, dictkeys, defval=None):
    width = width or defval
    if isinstance(width, (int, float)):
        return dict((key, width) for key in dictkeys)
    if isinstance(width, dict):
        for k, w in width.items():
            if isinstance(w, (int, float)):
                width[k] = w
        return dict((key, width.get(key, defval)) for key in dictkeys)
    raise Exception('This is not a valid width format: {0}'.format(type(width)))


# ==============================================================================
# draw funcs
# ==============================================================================


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
    coll = LineCollection(fromto,
                          linewidths=widths,
                          colors=colors,
                          alpha=alpha,
                          zorder=zorder)
    axes.add_collection(coll)


def draw_arrows(lines, axes=None, alpha=1.0, zorder=1000):
    if not axes:
        axes = plt.gca()
    arrowprops = {
        'arrowstyle'      : '-|>,head_length=0.4,head_width=0.2',
        'connectionstyle' : 'arc3,rad=0.0',
        'linewidth'       : 1.0,
        'color'           : '#000000',
        'shrinkB'         : 5,
    }
    for line in lines:
        sp    = line['start']
        ep    = line['end']
        color = line.get('color', '#000000')
        width = line.get('width', 1.0)
        arrowprops['color'] = color
        arrowprops['linewidth'] = width
        axes.annotate('', xy=ep, xytext=sp, arrowprops=arrowprops)


def draw_labels(labels, axes=None, zorder=1020, alpha=1.0, pad=0.0):
    if not axes:
        axes = plt.gca()
    for label in labels:
        x, y     = label['pos']
        text     = label['text']
        fontsize = label['fontsize']
        color    = label.get('color') or '#ffffff'
        tcolor   = label.get('textcolor') or '#000000'
        t = axes.text(x, y, text,
                      fontsize=fontsize,
                      zorder=zorder,
                      ha='center',
                      va='center',
                      color=tcolor)
        t.set_bbox(dict(color=color, edgecolor=color, alpha=alpha, pad=pad))


# ==============================================================================
# composite
# ==============================================================================


def draw_network(network,
                 draw_vertices=True,
                 draw_edges=True,
                 vcolor=None,
                 ecolor=None,
                 fcolor=None,
                 vlabel=None,
                 elabel=None,
                 ewidth=None,
                 flabel=None,
                 vsize=None,
                 axes=None):
    """"""
    # default values
    vcolor = color_to_colordict(vcolor, network.vertices(), DEFAULT_VERTEX_COLOR)
    ecolor = color_to_colordict(ecolor, network.edges(), DEFAULT_EDGE_COLOR)
    fcolor = color_to_colordict(fcolor, network.faces(), DEFAULT_FACE_COLOR)
    vlabel = vlabel or {}
    elabel = elabel or {}
    flabel = flabel or {}
    vsize  = vsize or 0.1
    ewidth = width_to_dict(ewidth, network.edges(), DEFAULT_EDGE_WIDTH)
    # figure setup
    if not axes:
        ax = plt.gca()
        ax.set_aspect('equal')
    else:
        ax = axes
    # edges
    if draw_edges:
        lines  = []
        colors = []
        linewidths = []
        for u, v in network.edges_iter():
            x  = network.vertex[u]['x'], network.vertex[v]['x']
            y  = network.vertex[u]['y'], network.vertex[v]['y']
            mp = 0.5 * (x[0] + x[1]), 0.5 * (y[0] + y[1])
            line = (x[0], y[0]), (x[1], y[1])
            lines.append(line)
            colors.append(ecolor[(u, v)])
            linewidths.append(ewidth[(u, v)])
            if (u, v) in elabel:
                text = elabel[(u, v)]
                ax.text(mp[0], mp[1], text,
                        fontsize=8,
                        zorder=13,
                        ha='center',
                        va='center',
                        color=DEFAULT_TEXT_COLOR,
                        backgroundcolor='#ffffff')
        # make a collection
        # add collection to axes
        collection = LineCollection(lines, linewidths=linewidths, colors=colors, zorder=10, alpha=1.0)
        ax.add_collection(collection)
    # vertices
    if draw_vertices:
        circles    = []
        facecolors = []
        edgecolors = []
        for key, attr in network.vertices_iter(data=True):
            xy = attr['x'], attr['y']
            circle = Circle(xy, radius=vsize)
            circles.append(circle)
            facecolors.append(vcolor[key])
            edgecolors.append(DEFAULT_EDGE_COLOR)
            if key in vlabel:
                text = vlabel[key]
                ax.text(xy[0], xy[1], text, fontsize=8, zorder=13, ha='center', va='center', color=DEFAULT_TEXT_COLOR)
        # make a collection
        # add collection to axes
        collection = PatchCollection(circles, facecolor=facecolors, edgecolor=edgecolors, lw=0.5, alpha=1.0, zorder=12)
        ax.add_collection(collection)
    # faces
    for fkey, vertices in network.face.items():
        if fkey in flabel:
            c = centroid([[network.vertex[key][_] for _ in 'xy'] for key in set(vertices)])
            ax.text(c[0], c[1], fkey, fontsize=8, zorder=13, ha='center', va='center', color=DEFAULT_TEXT_COLOR)
    # finalise figure setup
    # show figure
    if not axes:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xmargin(0.05)
        ax.set_ymargin(0.05)
        ax.autoscale()
        plt.show()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
