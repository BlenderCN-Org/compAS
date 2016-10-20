# -*- coding: utf-8 -*-

try:
    import System
    import Rhino
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    find_object = sc.doc.Objects.Find
    purge_object = sc.doc.Objects.Purge

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Sep 26, 2014'


__all__ = [
    'set_color',
    'is_line',
    'is_polyline',
    'is_polygon',
    'delete_objects',
    'get_objects',
    'get_object_names',
    'get_object_attributes',
    'get_points',
    'get_point_coordinates',
    'select_curve',
    'select_curves',
    'select_lines',
    'select_polylines',
    'select_polygons',
    'get_lines',
    'get_polylines',
    'get_polygons',
    'get_line_coordinates',
    'get_polyline_coordinates',
    'get_polygon_coordinates',
    'get_surfaces',
    'get_meshes',
    'get_mesh_face_vertices',
    'get_mesh_vertex_coordinates',
    'get_mesh_vertex_colors',
    'set_mesh_vertex_colors',
    'get_mesh_vertices_and_faces',
    'get_mesh_vertex_index',
    'get_mesh_face_index',
    'get_mesh_edge_index',
]


# ==============================================================================
# Objects
# ==============================================================================


def get_object(name=None, color=None, layer=None):
    guids = get_objects(name=name, color=color, layer=layer)
    if guids:
        return guids[0]
    return None


def get_objects(name=None, color=None, layer=None):
    guids = rs.AllObjects()
    if name:
        guids = list(set(guids) & set(rs.ObjectsByName(name)))
    if color:
        guids = list(set(guids) & set(rs.ObjectsByColor(color)))
    if layer:
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
    return guids


def delete_object(guid):
    delete_objects([guid])


def delete_objects(guids):
    for guid in guids:
        if rs.IsObjectHidden(guid):
            rs.ShowObject(guid)
        o = find_object(guid)
        purge_object(o.RuntimeSerialNumber)
    sc.doc.Views.Redraw()


def get_object_names(guids):
    return [rs.ObjectName(guid) for guid in guids]


def get_object_attributes():
    raise NotImplementedError


def set_color(guids, color):
    for guid in guids:
        rs.ObjectColor(guid, color)


# use ast for this
# ast.literal_eval
# @see: https://docs.python.org/2/library/ast.html#ast.literal_eval
def get_object_attributes_from_name(name, separator=';', assignment=':'):
    attr  = {}
    if name:
        name = name.lstrip('{')
        name = name.rstrip('}')
        parts = name.split(separator)
        for part in parts:
            pair = part.split(assignment)
            if len(pair) == 2:
                key, value = pair
                try:
                    attr[eval(key)] = eval(value)
                except:
                    pass
    return attr


# ==============================================================================
# Points
# ==============================================================================


def select_points(message='Select points.'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.point)
    if temp:
        guids = temp
    return guids


def get_points(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.point)
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.point)
    return guids


def get_point_coordinates(guids):
    points = []
    for guid in guids:
        point = rs.PointCoordinates(guid)
        if point:
            points.append(map(float, point))
    return points


# ==============================================================================
# Curves
# ==============================================================================


def is_line(guid):
    return rs.IsCurve(guid) and rs.IsLine(guid) and rs.CurveDegree(guid) == 1 and len(rs.CurvePoints(guid)) == 2


def is_polyline(guid):
    return rs.IsCurve(guid) and rs.IsPolyline(guid) and rs.CurveDegree(guid) == 1 and len(rs.CurvePoints(guid)) > 2


def is_polygon(guid):
    return rs.IsCurve(guid) and rs.IsCurveClosed(guid) and rs.CurveDegree(guid) == 1 and len(rs.CurvePoints(guid)) > 2


def select_curve(message='Select curve.'):
    return rs.GetObject(message, filter=rs.filter.curve)


def select_curves(message='Select curves.'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.curve)
    if temp:
        guids = temp
    return guids


def select_lines(message='Select lines.'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.curve)
    if temp:
        for guid in temp:
            if is_line(guid):
                    guids.append(guid)
    return guids


def select_polylines(message='Select polylines (curves with degree = 1, and multiple segments).'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.curve)
    if temp:
        for guid in temp:
            if is_polyline(guid):
                    guids.append(guid)
    return guids


def select_polygons(message='Select polygons (closed curves with degree = 1)'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.curve)
    if temp:
        for guid in temp:
            if is_polygon(guid):
                guids.append(guid)
    return guids


def get_lines(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_line(guid)]
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_line(guid)]
    return guids


def get_polylines(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_polyline(guid)]
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_polyline(guid)]
    return guids


def get_polygons(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_polygon(guid)]
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.curve)
        guids = [guid for guid in guids if is_polygon(guid)]
    return guids


def get_line_coordinates(guids):
    if isinstance(guids, System.Guid):
        sp = map(float, rs.CurveStartPoint(guids))
        ep = map(float, rs.CurveEndPoint(guids))
        return sp, ep
    lines = []
    for guid in guids:
        sp = map(float, rs.CurveStartPoint(guid))
        ep = map(float, rs.CurveEndPoint(guid))
        lines.append((sp, ep))
    return lines


def get_polyline_coordinates(guids):
    if isinstance(guids, System.Guid):
        points = rs.PolylineVertices(guids)
        coords = []
        if points:
            coords = [map(float, point) for point in points]
        return coords
    polylines = []
    for guid in guids:
        points = rs.PolylineVertices(guid)
        coords = []
        if points:
            coords = [map(float, point) for point in points]
        polylines.append(coords)
    return polylines


def get_polygon_coordinates(guids):
    if isinstance(guids, System.Guid):
        points = rs.CurvePoints(guids)
        coords = []
        if points:
            coords = [list(point) for point in points]
        return coords
    polygons = []
    if guids:
        for guid in guids:
            points = rs.CurvePoints(guid)
            coords = []
            if points:
                coords = map(list, points)
            polygons.append(coords)
    return polygons


# ==============================================================================
# Surfaces
# ==============================================================================


def get_surface(message='Select a surface.'):
    return rs.GetObject(
        message,
        filter=rs.filter.surface | rs.filter.polysurface
    )


def get_surfaces(message='Select surfaces.'):
    guids = []
    temp = rs.GetObjects(
        message,
        filter=rs.filter.surface | rs.filter.polysurface
    )
    if temp:
        guids = temp
    return guids


# ==============================================================================
# Meshes
# ==============================================================================


def select_mesh(message='Select a mesh.'):
    return rs.GetObject(
        message,
        filter=rs.filter.mesh
    )


def select_meshes(message='Select meshes.'):
    guids = []
    temp = rs.GetObjects(message, filter=rs.filter.mesh)
    if temp:
        guids = temp
    return guids


def get_mesh(layer=None):
    guids = get_meshes(layer=layer)
    if guids:
        return guids[0]


def get_meshes(layer=None):
    if layer:
        rs.EnableRedraw(False)
        visible = rs.LayerVisible(layer, visible=True, force_visible=True)
        guids = rs.ObjectsByType(rs.filter.mesh)
        guids = list(set(guids) & set(rs.ObjectsByLayer(layer)))
        rs.LayerVisible(layer, visible=visible, force_visible=visible)
        rs.EnableRedraw(True)
    else:
        guids = rs.ObjectsByType(rs.filter.mesh)
    return guids


def get_mesh_face_vertices(guid):
    faces = []
    if guid:
        temp = rs.MeshFaceVertices(guid)
        faces = map(list, temp)
    return faces


def get_mesh_vertex_coordinates(guid):
    vertices = []
    if guid:
        vertices = [map(float, vertex) for vertex in rs.MeshVertices(guid)]
    return vertices


def get_mesh_vertex_colors(guid):
    colors = []
    if guid:
        temp = rs.MeshVertexColors(guid)
        if temp:
            colors = map(list, temp)
    return colors


def set_mesh_vertex_colors(guid, colors):
    if not guid:
        return
    return rs.MeshVertexColors(guid, colors)


def get_mesh_vertices_and_faces(guid):
    if not guid:
        return
    vertices = [map(float, vertex) for vertex in rs.MeshVertices(guid)]
    faces = map(list, rs.MeshFaceVertices(guid))
    return vertices, faces


def get_mesh_vertex_index(guid):
    class CustomGetObject(Rhino.Input.Custom.GetObject):
        def CustomGeometryFilter(self, rhino_object, geometry, component_index):
            return guid == rhino_object.Id
    go = CustomGetObject()
    go.SetCommandPrompt('Select a vertex of the mesh.')
    go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshVertex
    go.AcceptNothing(True)
    if go.Get() != Rhino.Input.GetResult.Object:
        return None
    objref = go.Object(0)
    if not objref:
        return None
    tvindex = objref.GeometryComponentIndex.Index
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
    vindex = temp[0]
    go.Dispose()
    return vindex


def get_mesh_face_index(guid):
    class CustomGetObject(Rhino.Input.Custom.GetObject):
        def CustomGeometryFilter(self, rhino_object, geometry, component_index):
            return guid == rhino_object.Id
    go = CustomGetObject()
    go.SetCommandPrompt('Select a face of the mesh.')
    go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshFace
    go.AcceptNothing(True)
    if go.Get() != Rhino.Input.GetResult.Object:
        return None
    objref = go.Object(0)
    if not objref:
        return None
    findex = objref.GeometryComponentIndex.Index
    go.Dispose()
    return findex


def get_mesh_edge_index(guid):
    class CustomGetObject(Rhino.Input.Custom.GetObject):
        def CustomGeometryFilter(self, rhino_object, geometry, component_index):
            return guid == rhino_object.Id
    go = CustomGetObject()
    go.SetCommandPrompt('Select an edge of the mesh.')
    go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
    go.AcceptNothing(True)
    if go.Get() != Rhino.Input.GetResult.Object:
        return None
    objref = go.Object(0)
    if not objref:
        return None
    eindex = objref.GeometryComponentIndex.Index
    go.Dispose()
    return eindex


def get_mesh_vertex_indices(guid):
    tvindices = rs.GetMeshVertices(guid, 'Select mesh vertices.')
    if not tvindices:
        return
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    vindices = []
    for tvindex in tvindices:
        temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
        vindices.append(temp[0])
    return vindices


def get_mesh_face_indices(guid):
    return rs.GetMeshFaces(guid, 'Select mesh faces.')


def get_mesh_vertex_face_indices(guid):
    vindex = get_mesh_vertex_index(guid)
    if vindex is None:
        return
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    findices = mgeo.TopologyVertices.ConnectedFaces(vindex)
    return findices


def get_mesh_face_vertex_indices(guid):
    findex = get_mesh_face_index(guid)
    if findex is None:
        return
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    tvertices = mgeo.Faces.GetTopologicalVertices(findex)
    vindices = []
    for tvertex in tvertices:
        temp = mgeo.TopologyVertices.MeshVertexIndices(tvertex)
        vindices.append(temp[0])
    return vindices


def get_mesh_edge_vertex_indices(guid):
    eindex = get_mesh_edge_index(guid)
    if eindex is None:
        return
    mobj = sc.doc.Objects.Find(guid)
    mgeo = mobj.Geometry
    temp = mgeo.TopologyEdges.GetTopologyVertices(eindex)
    tvindices = temp.I, temp.J
    vindices = []
    for tvindex in tvindices:
        temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
        vindices.append(temp[0])
    return vindices


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
