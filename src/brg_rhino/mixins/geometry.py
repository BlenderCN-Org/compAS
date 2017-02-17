from brg_rhino.mixins import Mixin

from brg_rhino.helpers.network import move_network
from brg_rhino.helpers.network import move_network_vertex


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['EditMeshGeometry', 'EditNetworkGeometry', ]


class EditMeshGeometry(Mixin):
    """"""

    pass


class EditNetworkGeometry(Mixin):
    """"""

    move = move_network
    move_vertex = move_network_vertex


# class DisplayGeometry(Mixin):
#     """"""

#     def display_vertex_normals(self, display=True, layer=None, scale=1.0, color=None):
#         rhino.delete_objects(rhino.get_objects(name='{0}.vertex.normal.*'.format(self.attributes['name'])))
#         if not display:
#             return
#         lines = []
#         layer = layer or self.layer
#         color = color or self.color['normal:vertex']
#         for key in self.vertex:
#             nv   = self.vertex_normal(key)
#             sp   = self.vertex_coordinates(key)
#             ep   = [sp[axis] + nv[axis] for axis in range(3)]
#             name = '{0}.vertex.normal.{1}'.format(self.attributes['name'], key)
#             lines.append({
#                 'start' : sp,
#                 'end'   : ep,
#                 'name'  : name,
#                 'color' : color,
#                 'arrow' : 'end',
#             })
#         rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)

#     def display_face_normals(self, display=True, layer=None, scale=1.0, color=None):
#         rhino.delete_objects(rhino.get_objects(name='{0}.face.normal.*'.format(self.attributes['name'])))
#         if not display:
#             return
#         lines = []
#         layer = layer or self.layer
#         color = color or self.color['normal:face']
#         for fkey in self.face:
#             nv   = self.face_normal(fkey)
#             sp   = self.face_center(fkey)
#             ep   = [sp[axis] + nv[axis] for axis in range(3)]
#             name = '{0}.face.normal.{1}'.format(self.attributes['name'], fkey)
#             lines.append({
#                 'start' : sp,
#                 'end'   : ep,
#                 'name'  : name,
#                 'color' : color,
#                 'arrow' : 'end',
#             })
#         rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
