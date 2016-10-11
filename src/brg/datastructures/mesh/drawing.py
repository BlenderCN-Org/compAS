import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from brg.geometry import centroid
from brg.utilities import color_to_colordict


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2015-12-04 08:57:27'


__all__ = ['draw_mesh']


DTC = '#000000'
DVC = '#ffffff'
DEC = '#333333'
DFC = '#eeeeee'


def draw_mesh(mesh,
              show_vertices=False,
              show_faces=True,
              vertex_color=None,
              face_color=None,
              vertex_label=None,
              face_label=None,
              vertex_size=None):
    """Draw the mesh using ``matplotlib``.
    """
    vertex_size = vertex_size or 0.1  # default to min(length(diagonal) / v, length(canvas diagonal) / 20)
    vertex_color = vertex_color or DVC
    face_color = face_color or DFC
    # default color values
    vcolor = color_to_colordict(vertex_color, mesh.vertex, DVC)
    fcolor = color_to_colordict(face_color, mesh.face, DFC)
    # default vertex labels
    if not vertex_label or not isinstance(vertex_label, dict):
        vertex_label = {}
    # default face labels
    if not face_label or not isinstance(face_label, dict):
        face_label = {}
    # figure setup
    plt.figure(figsize=(8.0, 6.0), dpi=100, frameon=True)
    axes = plt.gca()
    axes.set_aspect('equal')
    for spine in axes.spines.itervalues():
        spine.set_linewidth(0.1)
    # faces
    if show_faces:
        polygons = []
        for fkey in mesh.face:
            points = [mesh.vertex_coordinates(vkey, 'xy') for vkey in mesh.face_vertices(fkey, ordered=True)]
            text   = None if fkey not in face_label else face_label[fkey]
            polygons.append({'points'    : points,
                             'text'      : text,
                             'textcolor' : DTC,
                             'facecolor' : fcolor[fkey],
                             'edgecolor' : DEC, })
        draw_polygons(axes, polygons)
    # points
    if show_vertices:
        points = []
        for vkey in mesh.vertex:
            xy   = mesh.vertex_coordinates(vkey, 'xy')
            text = None if vkey not in vertex_label else vertex_label[vkey]
            points.append({'pos'       : xy,
                           'text'      : text,
                           'radius'    : vertex_size,
                           'textcolor' : DTC,
                           'facecolor' : vcolor[vkey],
                           'edgecolor' : DEC, })
        draw_points(axes, points)
    # plot settings
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_xmargin(0.05)
    axes.set_ymargin(0.05)
    axes.autoscale()
    plt.tight_layout()
    plt.show()


def draw_meshes(meshes):
    pass


def draw_points(axes, points):
    """Draw points using ``matplotlib``.

    Parameters:
        points (list): A list of XYZ coordinates per point.

    Returns:
        None
    """
    facecolors = []
    edgecolors = []
    collection = []
    for attr in points:
        pos = attr['pos']
        radius = attr['radius']
        facecolors.append(attr['facecolor'])
        edgecolors.append(attr['edgecolor'])
        textcolor = attr['textcolor']
        text = attr['text']
        point = Circle(pos, radius=radius)
        collection.append(point)
        if text:
            axes.text(pos[0],
                      pos[1] - 0.1 * radius,
                      text,
                      fontsize=8,
                      zorder=13,
                      ha='center',
                      va='center',
                      color=textcolor)
    collection = PatchCollection(collection,
                                 facecolor=facecolors,
                                 edgecolor=edgecolors,
                                 lw=0.25,
                                 alpha=1.0,
                                 zorder=12)
    axes.add_collection(collection)


def draw_lines():
    pass


def draw_polygons(axes, polygons):
    facecolors = []
    edgecolors = []
    collection = []
    for attr in polygons:
        points = attr['points']
        text = attr['text']
        textcolor = attr['textcolor']
        facecolors.append(attr['facecolor'])
        edgecolors.append(attr['edgecolor'])
        polygon = Polygon(points)
        collection.append(polygon)
        if text:
            c = centroid(points)
            axes.text(c[0], c[1], text, fontsize=8, zorder=13, ha='center', va='center', color=textcolor)
    collection = PatchCollection(collection, facecolor=facecolors, edgecolor='#333333', lw=0.25, zorder=10)
    axes.add_collection(collection)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
