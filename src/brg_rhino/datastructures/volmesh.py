from brg.datastructures import VolMesh
from brg.utilities.maps import geometric_key

import brg_rhino.utilities as rhino

try:
    import Rhino
    import scriptcontext as sc

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e


class RhinoVolMesh(VolMesh):

    def __init__(self):
        super(RhinoVolMesh, self).__init__()
        self.attributes.update({
            'layer' : None,
        })

    # --------------------------------------------------------------------------
    # descriptors
    #
    # NOTE: some descriptors could be inherited from the base Mixin class
    # --------------------------------------------------------------------------

    @property
    def layer(self):
        return self.attributes['layer']

    @layer.setter
    def layer(self, layer):
        self.attributes['layer'] = layer

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_polysurfaces(cls, guids):
        gkey_xyz = dict() 
        cells = []
        for guid in guids:
            cell = []
            obj = sc.doc.Objects.Find(guid)
            if not obj.Geometry.HasBrepForm:
                continue
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
                cell.append(face)
            cells.append(cell)
        gkey_index = dict((gkey, index) for index, gkey in enumerate(gkey_xyz))
        vertices = [list(xyz) for gkey, xyz in gkey_xyz.items()]
        cells = [[[gkey_index[gkey] for gkey in face] for face in cell] for cell in cells]
        return cls.from_vertices_and_cells(vertices, cells)

    @classmethod
    def from_wireframe(cls, edges):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # drawing
    # --------------------------------------------------------------------------

    def draw(self,
             name=None,
             layer=None,
             clear=True,
             redraw=True,
             show_faces=True,  # rename to display_faces?
             show_vertices=True,  # rename to display_vertices?
             show_edges=True,  # rename to display_edges?
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
            faces = []
            color = self.color['face']
            for vertices in self.faces():
                points = [self.vertex_coordinates(vkey) for vkey in vertices + [vertices[0]]]
                faces.append({
                    'points' : points,
                    'name'   : '',
                    'color'  : color,
                })
            rhino.xdraw_faces(faces,
                              layer=self.layer,
                              clear=clear,
                              redraw=(True if redraw and not (show_vertices or show_edges) else False))
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

    # --------------------------------------------------------------------------
    # attributes
    # --------------------------------------------------------------------------

    # def edit_vertex_attributes(self, keys=None, names=None):
    #     if not keys:
    #         keys = self.vertices()
    #     if not names:
    #         names = sorted(self.default_vertex_attributes.keys())

