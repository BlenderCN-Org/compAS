import matplotlib.pyplot as plt

from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection, LineCollection


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 17, 2016'


def create_matplotlib_axes(size=(10, 7),
                           xlabel='$x$',
                           ylabel='$y$',
                           zlabel='$z$',
                           fontname='Times New Roman',
                           fontsize=20,
                           grid=True,
                           limits=None,
                           ticklength=20,
                           tickfontsize=15):
    """Initialises plot axes object for matplotlib plotting.

    Note:
        z axes data included for future 3D plot implementation.

    Parameters:
        size (tuple): (horizontal, vertical) size of the figure.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        zlabel (str): Label for the z-axis.
        fontname (str): Fontname of the main labels and text.
        fontsize (int): Fontsize of the main labels and text.
        grid (boolean): Display grid.
        limits (dic): Axis limits and tick spacing.
        ticklength (float): length of the ticks.
        tickfontsize (int): Fontsize of the ticks.

    Returns:
        object: Matplotlib axes.
    """
    if not limits:
        limits = {'xmin': 0, 'dx': 0.1, 'xmax': 1,
                  'ymin': 0, 'dy': 0.1, 'ymax': 1,
                  'zmin': 0, 'dz': 0.1, 'zmax': 1}
    plt.figure(facecolor='white', figsize=size)
    plt.xlabel(xlabel, fontname=fontname, fontsize=fontsize)
    plt.ylabel(ylabel, fontname=fontname, fontsize=fontsize)
    if  grid:
        plt.grid()
    plt.minorticks_on()
    plt.axis([limits['xmin'], limits['xmax'], limits['ymin'], limits['ymax']])
    plt.tick_params(which='major', length=ticklength, labelsize=tickfontsize)
    plt.tick_params(which='minor', length=ticklength*0.33)
    axes = plt.gca()
    return axes


def draw_points():
    raise NotImplementedError


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
    raise NotImplementedError


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
    collection = LineCollection(lines, linewidths=linewidth, colors=color,
                                zorder=100)
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
