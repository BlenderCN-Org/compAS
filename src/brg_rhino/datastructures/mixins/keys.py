# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$


from brg_rhino.datastructures.mixins import Mixin

try:
    import rhinoscriptsyntax as rs

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Jun 19, 2015'


docs = [
    'GetKeys'
]


class GetKeys(Mixin):
    """"""

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
