from compas.utilities import geometric_key
from compas.utilities.colors import color_to_colordict

from compas_rhino.geometry.surface import RhinoSurface

import compas_rhino as rhino

try:
    import Rhino
    import scriptcontext as sc
    import rhinoscriptsyntax as rs
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_from_guid',
    'mesh_from_surface',
    'mesh_from_surface_uv',
    'mesh_from_surface_heightfield',
    'draw_mesh',
]


# ==============================================================================
# constructors
# ==============================================================================


def mesh_from_guid(cls, guid, **kwargs):
    vertices, faces = rhino.get_mesh_vertices_and_faces(guid)
    faces = [face[: -1] if face[-2] == face[-1] else face for face in faces]
    mesh  = cls.from_vertices_and_faces(vertices, faces)
    mesh.attributes.update(kwargs)
    return mesh


def mesh_from_surface(cls, guid, **kwargs):
    gkey_xyz = {}
    faces = []
    obj = sc.doc.Objects.Find(guid)
    if not obj.Geometry.HasBrepForm:
        return
    brep = Rhino.Geometry.Brep.TryConvertBrep(obj.Geometry)
    for loop in brep.Loops:
        curve = loop.To3dCurve()
        segments = curve.Explode()
        face = []
        sp = segments[0].PointAtStart
        ep = segments[0].PointAtEnd
        sp_gkey = geometric_key(sp)
        ep_gkey = geometric_key(ep)
        gkey_xyz[sp_gkey] = sp
        gkey_xyz[ep_gkey] = ep
        face.append(sp_gkey)
        face.append(ep_gkey)
        for segment in segments[1:-1]:
            ep = segment.PointAtEnd
            ep_gkey = geometric_key(ep)
            face.append(ep_gkey)
            gkey_xyz[ep_gkey] = ep
        faces.append(face)
    gkey_index = dict((gkey, index) for index, gkey in enumerate(gkey_xyz))
    vertices = [list(xyz) for gkey, xyz in gkey_xyz.items()]
    faces = [[gkey_index[gkey] for gkey in f] for f in faces]
    mesh = cls.from_vertices_and_faces(vertices, faces)
    mesh.attributes.update(kwargs)
    return mesh


def mesh_from_surface_uv(cls, guid, density=(10, 10), **kwargs):
    raise NotImplementedError


def mesh_from_surface_heightfield(cls, guid, density=(10, 10), **kwargs):
    try:
        u, v = density
    except:
        u, v = density, density
    surface = RhinoSurface(guid)
    mesh = cls()
    mesh.attributes.update(kwargs)
    vertices = surface.heightfield(density=(u, v), over_space=True)
    for x, y, z in vertices:
        mesh.add_vertex(x=x, y=y, z=z)
    for i in range(v - 1):
        for j in range(u - 1):
            face = ((i + 0) * u + j,
                    (i + 0) * u + j + 1,
                    (i + 1) * u + j + 1,
                    (i + 1) * u + j)
            mesh.add_face(face)
    return mesh


# ==============================================================================
# drawing
# ==============================================================================


# change clear to clearlayer
# remove redraw?
# process color spec into color dict

def draw_mesh(mesh,
              layer=None,
              clear_layer=False,
              show_faces=False,
              show_vertices=True,
              show_edges=True,
              vertexcolor=None,
              edgecolor=None,
              facecolor=None):
    """
    Draw a mesh object in Rhino.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        layer (str): Optional. The layer to draw in. Default is ``None``.
        clear_layer (bool): Optional. Clear the drawing layer. Default is ``True``.
        show_faces (bool): Optional. Show the faces. Default is ``True``.
        show_vertices (bool): Optional. Show the vertices. Default is ``True``.
        show_edges (bool): Optional. Show the edges. Default is ``True``.
        vertexcolor (str, tuple, list, dict): Optional. The vertex color specification. Default is ``None``.
        edgecolor (str, tuple, list, dict): Optional. The edge color specification. Default is ``None``.
        facecolor (str, tuple, list, dict): Optional. The face color specification. Default is ``None``.
        redraw (bool): Optional. Redraw instructions. Default is ``True``.

    Note:
        Colors can be specifiedin different ways:

        * str: A hexadecimal color that will be applied to all elements subject to the specification.
        * tuple, list: RGB color that will be applied to all elements subject to the specification.
        * dict: RGB or hex color dict with a specification for some or all of the related elements.

    Important:
        RGB colors should specify color values between 0 and 255.

    """
    # set default options
    vertexcolor = color_to_colordict(vertexcolor,
                                     mesh.vertices(),
                                     default=mesh.attributes['color.vertex'],
                                     colorformat='rgb',
                                     normalize=False)
    edgecolor = color_to_colordict(edgecolor,
                                   mesh.edges(),
                                   default=mesh.attributes['color.edge'],
                                   colorformat='rgb',
                                   normalize=False)
    facecolor = color_to_colordict(facecolor,
                                   mesh.faces(),
                                   default=mesh.attributes['color.face'],
                                   colorformat='rgb',
                                   normalize=False)
    guids = rhino.get_objects(name='{0}.*'.format(mesh.attributes['name']))
    rhino.delete_objects(guids)
    if clear_layer:
        if not layer:
            rhino.clear_current_layer()
        else:
            rhino.clear_layers((layer, ))
    if show_faces:
        key_index = dict((key, index) for index, key in mesh.vertices_enum())
        xyz       = [mesh.vertex_coordinates(key) for key in mesh.vertices_iter()]
        faces     = []
        color     = mesh.attributes['color.face']
        for fkey in mesh.face:
            face = mesh.face_vertices(fkey, ordered=True)
            v = len(face)
            if v < 3:
                print 'Degenerate face: {0} => {1}'.format(fkey, face)
                continue
            if v == 3:
                faces.append([key_index[k] for k in face + [face[-1]]])
            elif v == 4:
                faces.append([key_index[k] for k in face])
            else:
                # a polygonal face
                # => triangulate
                c = len(xyz)
                xyz.append(mesh.face_center(fkey))
                for i in range(-1, len(face) - 1):
                    key = face[i]
                    nbr = face[i + 1]
                    vertices = [c, key_index[key], key_index[nbr], key_index[nbr]]
                    faces.append(vertices)
        rhino.xdraw_mesh(xyz,
                         faces,
                         color,
                         mesh.attributes['name'],
                         layer=layer,
                         clear=False,
                         redraw=False)
    if show_edges:
        lines = []
        color = mesh.attributes['color.edge']
        for u, v in mesh.edges_iter():
            lines.append({
                'start': mesh.vertex_coordinates(u),
                'end'  : mesh.vertex_coordinates(v),
                'name' : '{0}.edge.{1}-{2}'.format(mesh.attributes['name'], u, v),
                'color': edgecolor.get((u, v), color),
            })
        rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=False)
    if show_vertices:
        points = []
        color  = mesh.attributes['color.vertex']
        for key in mesh.vertices_iter():
            points.append({
                'pos'  : mesh.vertex_coordinates(key),
                'name' : '{0}.vertex.{1}'.format(mesh.attributes['name'], key),
                'color': vertexcolor.get(key, color),
            })
        rhino.xdraw_points(points, layer=layer, clear=False, redraw=False)
    rs.Redraw()

# ==============================================================================
# selection
# ==============================================================================

# ==============================================================================
# attributes
# ==============================================================================

# ==============================================================================
# labels
# ==============================================================================

# ==============================================================================
# geometry
# ==============================================================================


def display_mesh_vertex_normals(mesh,
                                display=True,
                                layer=None,
                                scale=1.0,
                                color=(0, 0, 255)):
    guids = rhino.get_objects(name='{0}.vertex.normal.*'.format(mesh.attributes['name']))
    rhino.delete_objects(guids)
    if not display:
        return
    lines = []
    for key in mesh.vertex:
        nv   = mesh.vertex_normal(key)
        sp   = mesh.vertex_coordinates(key)
        ep   = [sp[axis] + nv[axis] for axis in range(3)]
        name = '{0}.vertex.normal.{1}'.format(mesh.attributes['name'], key)
        lines.append({
            'start' : sp,
            'end'   : ep,
            'name'  : name,
            'color' : color,
            'arrow' : 'end',
        })
    rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)


def display_mesh_face_normals(mesh,
                              display=True,
                              layer=None,
                              scale=1.0,
                              color=(0, 0, 255)):
    guids = rhino.get_objects(name='{0}.face.normal.*'.format(mesh.attributes['name']))
    rhino.delete_objects(guids)
    if not display:
        return
    lines = []
    for fkey in mesh.face:
        nv   = mesh.face_normal(fkey)
        sp   = mesh.face_center(fkey)
        ep   = [sp[axis] + nv[axis] for axis in range(3)]
        name = '{0}.face.normal.{1}'.format(mesh.attributes['name'], fkey)
        lines.append({
            'start' : sp,
            'end'   : ep,
            'name'  : name,
            'color' : color,
            'arrow' : 'end',
        })
    rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)


# ==============================================================================
# forces
# ==============================================================================


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
