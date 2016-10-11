from brg.datastructures import Mesh
from brg.utilities.maps import geometric_key

from brg_rhino.datastructures.mixins.attributes import EditAttributes
from brg_rhino.datastructures.mixins.geometry import EditGeometry
from brg_rhino.datastructures.mixins.geometry import DisplayGeometry
from brg_rhino.datastructures.mixins.keys import GetKeys
from brg_rhino.datastructures.mixins.labels import DisplayLabels

from brg_rhino.geometry.surface import Surface

import brg_rhino.utilities as rhino

try:
    import rhinoscriptsyntax as rs

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e


@rhino.add_gui_helpers((
    EditAttributes,
    EditGeometry,
    DisplayGeometry,
    GetKeys,
    DisplayLabels
))
class RhinoMesh(Mesh):

    def __init__(self, **kwargs):
        super(RhinoMesh, self).__init__(**kwargs)
        self.attributes.update({
            'layer'               : None,
            'color.normal:vertex' : (0, 255, 0),
            'color.normal:face'   : (0, 255, 0),
        })

    # --------------------------------------------------------------------------
    # descriptors
    #
    # NOTE: some descriptors are inherited from the base Mixin class
    # --------------------------------------------------------------------------

    @property
    def layer(self):
        """:obj:`str` : The layer of the mesh.

        Any value of appropriate type assigned to this property will be stored in
        the instance's attribute dict.
        """
        return self.attributes.get('layer', None)

    @layer.setter
    def layer(self, value):
        self.attributes['layer'] = value

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_guid(cls, guid, **kwargs):
        vertices, faces = rhino.get_mesh_vertices_and_faces(guid)
        faces = [face[: -1] if face[-2] == face[-1] else face for face in faces]
        mesh  = cls.from_vertices_and_faces(vertices, faces)
        mesh.attributes.update(kwargs)
        return mesh

    @classmethod
    def from_surface(cls, guid, density=(10, 10), **kwargs):
        surface = Surface(guid)
        try:
            u, v = density
        except:
            u, v = density, density
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

    # add parameter for maximum deviation from original geometry
    # split faces accordingly
    # for example, measure distance between potentail split point
    # and the corresponding curved surface
    @classmethod
    def from_polysurface(cls, guid, **kwargs):
        vertices = {}
        faces    = []
        gkey_key = {}
        count    = 0
        surfaces = rs.ExplodePolysurfaces(guid, False)
        for surface in surfaces:
            curves = rs.DuplicateEdgeCurves(surface)
            halfedges = []
            for curve in curves:
                sp = rs.CurveStartPoint(curve)
                ep = rs.CurveEndPoint(curve)
                sp_gkey = geometric_key(sp)
                ep_gkey = geometric_key(ep)
                if sp_gkey not in gkey_key:
                    gkey_key[sp_gkey] = str(count)
                    count += 1
                if ep_gkey not in gkey_key:
                    gkey_key[ep_gkey] = str(count)
                    count += 1
                u = gkey_key[sp_gkey]
                v = gkey_key[ep_gkey]
                vertices[u] = map(float, sp)
                vertices[v] = map(float, ep)
                halfedges.append([u, v])
            rs.DeleteObjects(curves)
            face = []
            start, end = halfedges[0]
            face.append(start)
            face.append(end)
            found = set()
            for i in range(1, len(halfedges)):
                for j in range(1, len(halfedges)):
                    if j in found:
                        continue
                    u, v = halfedges[j]
                    if u == end:
                        face.append(u)
                        start, end = u, v
                        found.add(j)
                        break
                    if v == end:
                        face.append(v)
                        halfedges[j] = v, u
                        start, end = v, u
                        found.add(j)
                        break
            faces.append(face)
        rs.DeleteObjects(surfaces)
        key_index = dict((key, index) for index, key in enumerate(vertices))
        vertices  = [xyz for key, xyz in vertices.items()]
        faces     = [[key_index[key] for key in face] for face in faces]
        mesh      = cls.from_vertices_and_faces(vertices, faces)
        mesh.attributes.update(kwargs)
        return mesh

    # --------------------------------------------------------------------------
    # drawing
    # --------------------------------------------------------------------------

    def draw(self,
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
        self.name  = name or self.name
        self.layer = layer or self.layer
        # delete all relevant objects by name
        objects  = rhino.get_objects(name='{0}.mesh'.format(self.name))
        objects += rhino.get_objects(name='{0}.vertex.*'.format(self.name))
        objects += rhino.get_objects(name='{0}.edge.*'.format(self.name))
        rhino.delete_objects(objects)
        # draw the requested components
        if show_faces:
            key_index = dict((key, index) for index, key in self.vertices_enum())
            xyz       = [self.vertex_coordinates(key) for key in self.vertices_iter()]
            faces     = []
            color     = self.color['face']
            for fkey in self.face:
                face = self.face_vertices(fkey, ordered=True)
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
                    xyz.append(self.face_center(fkey))
                    for i in range(-1, len(face) - 1):
                        key = face[i]
                        nbr = face[i + 1]
                        vertices = [c, key_index[key], key_index[nbr], key_index[nbr]]
                        faces.append(vertices)
            rhino.xdraw_mesh(xyz,
                             faces,
                             color,
                             self.name,
                             layer=self.layer,
                             clear=clear,
                             redraw=(True if redraw and not (show_edges or show_vertices) else False))
        if show_edges:
            lines = []
            color = self.color['edge']
            for u, v in self.edges_iter():
                lines.append({
                    'start': self.vertex_coordinates(u),
                    'end'  : self.vertex_coordinates(v),
                    'name' : '{0}.edge.{1}-{2}'.format(self.name, u, v),
                    'color': edge_color.get((u, v), color),
                })
            rhino.xdraw_lines(lines,
                              layer=self.layer,
                              clear=(True if clear and not show_faces else False),
                              redraw=(True if redraw and not show_vertices else False))
        if show_vertices:
            points = []
            color  = self.color['vertex']
            for key in self.vertices_iter():
                points.append({
                    'pos'  : self.vertex_coordinates(key),
                    'name' : '{0}.vertex.{1}'.format(self.name, key),
                    'color': vertex_color.get(key, color),
                })
            rhino.xdraw_points(points,
                               layer=self.layer,
                               clear=(True if clear and not (show_faces or show_edges) else False),
                               redraw=redraw)
