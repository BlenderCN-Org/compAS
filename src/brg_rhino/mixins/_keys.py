from brg_rhino.mixins import Mixin

try:
    import rhinoscriptsyntax as rs

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['SelectComponents', ]


def select_vertices(self, message='Select vertices.'):
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guids:
        prefix = self.name
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'vertex' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        keys.append(key)
    return keys


def select_vertex(self, message='Select vertex.'):
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guid:
        prefix = self.name
        name = rs.ObjectName(guid).split('.')
        if 'vertex' in name:
            if not prefix or prefix in name:
                return name[-1]
    return None


def select_edges(self, message='Select edges.'):
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guids:
        prefix = self.name
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'edge' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        uv = tuple(key.split('-'))
                        keys.append(uv)
    return keys


def select_edge(self, message='Select an edge.'):
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guid:
        prefix = self.name
        name = rs.ObjectName(guid).split('.')
        if 'edge' in name:
            if not prefix or prefix in name:
                key = name[-1]
                return tuple(key.split('-'))
    return None


def select_faces(self, message='Select faces.'):
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.textdot)
    if guids:
        prefix = self.name
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'face' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        keys.append(key)
    return keys


def select_face(self, message='Select face.'):
    guid = rs.GetObjects(message, preselect=True, filter=rs.filter.textdot)
    if guid:
        prefix = self.name
        name = rs.ObjectName(guid).split('.')
        if 'face' in name:
            if not prefix or prefix in name:
                key = name[-1]
                return key
    return None


class SelectComponents(Mixin):
    """"""
    select_vertex   = select_vertex
    select_vertices = select_vertices
    select_edge     = select_edge
    select_edges    = select_edges
    select_face     = select_face
    select_faces    = select_faces


def get_vertex_keys(self, message='Select vertices.'):
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guids:
        prefix = self.name
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'vertex' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        keys.append(key)
    return keys


def get_vertex_key(self, message='Select vertex.'):
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guid:
        prefix = self.name
        name = rs.ObjectName(guid).split('.')
        if 'vertex' in name:
            if not prefix or prefix in name:
                return name[-1]
    return None


def get_edge_keys(self, message='Select edges.'):
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guids:
        prefix = self.name
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'edge' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        uv = tuple(key.split('-'))
                        keys.append(uv)
    return keys


def get_edge_key(self, message='Select an edge.'):
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guid:
        prefix = self.name
        name = rs.ObjectName(guid).split('.')
        if 'edge' in name:
            if not prefix or prefix in name:
                key = name[-1]
                return tuple(key.split('-'))
    return None


def get_face_keys(self, message='Select faces.'):
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.textdot)
    if guids:
        prefix = self.name
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'face' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        keys.append(key)
    return keys


def get_face_key(self, message='Select face.'):
    guid = rs.GetObjects(message, preselect=True, filter=rs.filter.textdot)
    if guid:
        prefix = self.name
        name = rs.ObjectName(guid).split('.')
        if 'face' in name:
            if not prefix or prefix in name:
                key = name[-1]
                return key
    return None


class GetKeys(Mixin):
    """"""
    get_vertex_key  = get_vertex_key
    get_vertex_keys = get_vertex_keys
    get_edge_key    = get_edge_key
    get_edge_keys   = get_edge_keys
    get_face_key    = get_face_key
    get_face_keys   = get_face_keys


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
