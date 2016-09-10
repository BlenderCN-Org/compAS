# -*- coding: utf-8 -*-

import Rhino
import rhinoscriptsyntax as rs


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'Apache License, Version 2.0'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '29.09.2014'


class MeshError(Exception):
    pass


class Mesh(object):
    """"""

    def __init__(self, guid):
        self.guid = guid

    # def get_vertices(self):
    #     return [map(float, vertex) for vertex in rs.MeshVertices(self.guid)]

    def get_coordinates(self):
        return [map(float, vertex) for vertex in rs.MeshVertices(self.guid)]

    def get_faces(self):
        return map(list, rs.MeshFaceVertices(self.guid))

    def get_face_vertices(self):
        return map(list, rs.MeshFaceVertices(self.guid))

    def get_vertex_colors(self):
        return map(list, rs.MeshVertexColors(self.guid))

    def set_vertex_colors(self, colors):
        return rs.MeshVertexColors(self.guid, colors)

    def get_vertices_and_faces(self):
        vertices = [map(float, vertex) for vertex in rs.MeshVertices(self.guid)]
        faces = map(list, rs.MeshFaceVertices(self.guid))
        return vertices, faces

    def get_vertex_index(self):
        guid = self.guid
        class CustomGetObject(Rhino.Input.Custom.GetObject):
            def CustomGeometryFilter(self, rhino_object, geometry, component_index):
                # return True if selection is on current mesh object (guid)
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
        mesh    = sc.doc.Objects.Find(guid)
        temp    = mesh.Geometry.TopologyVertices.MeshVertexIndices(tvindex)
        vindex  = temp[0]
        go.Dispose()
        return vindex

    def get_face_index(self):
        guid = self.guid
        class CustomGetObject(Rhino.Input.Custom.GetObject):
            def CustomGeometryFilter(self, rhino_object, geometry, component_index):
                # return True if selecion is on current mesh object (guid)
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

    # def get_edge_index(guid):
    #     class CustomGetObject(Rhino.Input.Custom.GetObject):
    #         def CustomGeometryFilter(self, rhino_object, geometry, component_index):
    #             return guid == rhino_object.Id
    #     go = CustomGetObject()
    #     go.SetCommandPrompt('Select an edge of the mesh.')
    #     go.GeometryFilter = Rhino.DocObjects.ObjectType.MeshEdge
    #     go.AcceptNothing(True)
    #     if go.Get() != Rhino.Input.GetResult.Object:
    #         return None
    #     objref = go.Object(0)
    #     if not objref:
    #         return None
    #     eindex = objref.GeometryComponentIndex.Index
    #     go.Dispose()
    #     return eindex
    #
    # def get_vertex_indices(guid):
    #     tvindices = rs.GetMeshVertices(guid, 'Select mesh vertices.')
    #     if not tvindices:
    #         return
    #     mobj = sc.doc.Objects.Find(guid)
    #     mgeo = mobj.Geometry
    #     vindices = []
    #     for tvindex in tvindices:
    #         temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
    #         vindices.append(temp[0])
    #     return vindices
    #
    # def get_face_indices(guid):
    #     return rs.GetMeshFaces(guid, 'Select mesh faces.')
    #
    # def get_vertex_face_indices(guid):
    #     vindex = get_mesh_vertex_index(guid)
    #     if vindex is None:
    #         return
    #     mobj = sc.doc.Objects.Find(guid)
    #     mgeo = mobj.Geometry
    #     findices = mgeo.TopologyVertices.ConnectedFaces(vindex)
    #     return findices
    #
    # def get_face_vertex_indices(guid):
    #     findex = get_mesh_face_index(guid)
    #     if findex is None:
    #         return
    #     mobj = sc.doc.Objects.Find(guid)
    #     mgeo = mobj.Geometry
    #     tvertices = mgeo.Faces.GetTopologicalVertices(findex)
    #     vindices = []
    #     for tvertex in tvertices:
    #         temp = mgeo.TopologyVertices.MeshVertexIndices(tvertex)
    #         vindices.append(temp[0])
    #     return vindices
    #
    # def get_edge_vertex_indices(guid):
    #     eindex = get_mesh_edge_index(guid)
    #     if eindex is None:
    #         return
    #     mobj = sc.doc.Objects.Find(guid)
    #     mgeo = mobj.Geometry
    #     temp = mgeo.TopologyEdges.GetTopologyVertices(eindex)
    #     tvindices = temp.I, temp.J
    #     vindices = []
    #     for tvindex in tvindices:
    #         temp = mgeo.TopologyVertices.MeshVertexIndices(tvindex)
    #         vindices.append(temp[0])
    #     return vindices


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
