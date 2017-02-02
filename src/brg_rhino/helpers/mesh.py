from brg.utilities.maps import geometric_key
from brg_rhino.geometry.surface import RhinoSurface

import brg_rhino.utilities as rhino

try:
    import Rhino
    import scriptcontext as sc
except ImportError as e:
    import platform
    if platform.system() == 'Windows':
        raise e


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


def draw_mesh(mesh,
              name=None,
              layer=None,
              clear=True,
              redraw=True,
              show_faces=True,
              show_vertices=True,
              show_edges=True,
              vertex_color=None,
              edge_color=None,
              face_color=None):
    """"""
    # set default options
    if not isinstance(vertex_color, dict):
        vertex_color = {}
    if not isinstance(edge_color, dict):
        edge_color = {}
    if not isinstance(face_color, dict):
        face_color = {}
    if name:
        mesh.attributes['name'] = name
    name = mesh.setdefault('name', name)
    if layer:
        mesh.attributes['layer'] = layer
    layer = mesh.setdefault('layer', layer)
    # delete all relevant objects by name
    objects  = rhino.get_objects(name='{0}.mesh'.format(name))
    objects += rhino.get_objects(name='{0}.vertex.*'.format(name))
    objects += rhino.get_objects(name='{0}.edge.*'.format(name))
    rhino.delete_objects(objects)
    # clear the relevant layers
    if clear:
        rhino.clear_layers([layer])
    # draw the requested components
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
                c = len(xyz)
                xyz.append(mesh.face_center(fkey))
                for i in range(-1, len(face) - 1):
                    key = face[i]
                    nbr = face[i + 1]
                    vertices = [c, key_index[key], key_index[nbr], key_index[nbr]]
                    faces.append(vertices)
        rhino.xdraw_mesh(xyz, faces, color, name, layer=layer, clear=False, redraw=False)
    if show_edges:
        lines = []
        color = mesh.attributes['color.edge']
        for u, v in mesh.edges_iter():
            lines.append({
                'start': mesh.vertex_coordinates(u),
                'end'  : mesh.vertex_coordinates(v),
                'name' : '{0}.edge.{1}-{2}'.format(name, u, v),
                'color': edge_color.get((u, v), color),
            })
        rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=False)
    if show_vertices:
        points = []
        color  = mesh.attributes['color.vertex']
        for key in mesh.vertices_iter():
            points.append({
                'pos'  : mesh.vertex_coordinates(key),
                'name' : '{0}.vertex.{1}'.format(name, key),
                'color': vertex_color.get(key, color),
            })
        rhino.xdraw_points(points, layer=layer, clear=False, redraw=False)
    # redraw the views if so requested
    if redraw:
        rs.Redraw()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
