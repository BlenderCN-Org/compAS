import matplotlib.pyplot as plt

from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection, LineCollection


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Jul 21, 2015'


def draw_points():
    pass


def draw_points_in_matplotlib(points,
                              axes=None,
                              facecolor='#ffffff',
                              edgecolor='#000000',
                              radius=1.0,
                              labels=None):
    """"""
    if not axes:
        ax = plt.gca()
        ax.set_aspect('equal')
    else:
        ax = axes
    p = len(points)
    if isinstance(facecolor, basestring):
        facecolor = [facecolor] * p
    if isinstance(edgecolor, basestring):
        edgecolor = [edgecolor] * p
    if isinstance(radius, (int, float)):
        radius = [radius] * p
    if not labels:
        labels = [None] * p
    circles = []
    for i in range(p):
        point  = points[i]
        circle = Circle(point[0:2], radius=radius[i])
        circles.append(circle)
    collection = PatchCollection(circles,
                                 facecolor=facecolor,
                                 edgecolor=edgecolor,
                                 lw=0.5,
                                 alpha=1.0,
                                 zorder=1000)
    ax.add_collection(collection)

    for i in range(p):
        label = labels[i]
        point = points[i]
        if label:
            color = '#000000'
            ax.text(point[0], point[1],
                    label,
                    fontsize=8,
                    zorder=1001,
                    ha='center',
                    va='center',
                    color=color)
    if not axes:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xmargin(0.05)
        ax.set_ymargin(0.05)
        ax.autoscale()
        plt.show()


def draw_lines():
    pass


def draw_lines_in_matplotlib(lines,
                             axes=None,
                             linewidth=1.0,
                             color='#000000'):
    if not axes:
        ax = plt.gca()
        ax.set_aspect('equal')
    else:
        ax = axes
    l = len(lines)
    if isinstance(linewidth, (int, float)):
        linewidth = [linewidth] * l
    if isinstance(color, basestring):
        color = [color] * l
    for i in range(l):
        line = lines[i]
        lines.append(line)
    collection = LineCollection(lines, linewidths=linewidth, colors=color, zorder=100)
    ax.add_collection(collection)
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
