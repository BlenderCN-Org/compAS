# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$


from brg_rhino.datastructures.mixins import Mixin
import brg_rhino.utilities as rhino


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Jun 19, 2015'


class DisplayLabels(Mixin):
    """"""

    def display_vertex_labels(self, display=True, layer=None, attr_name=None):
        rhino.delete_objects(rhino.get_objects('{0}.vertex.label*'.format(self.name)))
        if not display:
            return
        labels = []
        layer = layer or self.layer
        color = self.color['vertex']
        for key in self.vertex:
            pos   = self.vertex_coordinates(key)
            name  = '{0}.vertex.label.{1}'.format(self.name, key)
            text  = self.vertex[key].get(attr_name, key)
            labels.append({'pos'  : pos,
                           'text' : text,
                           'name' : name,
                           'color': color, })
        rhino.xdraw_labels(labels, layer=layer, clear=False, redraw=True)

    def display_edge_labels(self, display=True, layer=None, attr_name=None):
        rhino.delete_objects(rhino.get_objects('{0}.edge.label*'.format(self.name)))
        if not display:
            return
        labels = []
        layer = layer or self.layer
        color = self.color['edge']
        for i, (u, v) in self.edges_enum():
            pos   = self.edge_midpoint(u, v)
            name  = '{0}.edge.label.{1}-{2}'.format(self.name, u, v)
            text  = self.edge[u][v].get(attr_name, str(i))
            labels.append({'pos'  : pos,
                           'name' : name,
                           'text' : text,
                           'color': color, })
        rhino.xdraw_labels(labels, layer=layer, clear=False, redraw=True)

    def display_face_labels(self, display=True, layer=None, attr_name=None):
        rhino.delete_objects(rhino.get_objects('{0}.face.label*'.format(self.name)))
        if not display:
            return
        labels = []
        layer = layer or self.layer
        color = self.color['face']
        for fkey in self.face:
            pos   = self.face_center(fkey)
            name  = '{0}.face.label.{1}'.format(self.name, fkey)
            text  = fkey
            labels.append({'pos'  : pos,
                           'name' : name,
                           'text' : text,
                           'color': color, })
        rhino.xdraw_labels(labels, layer=layer, clear=False, redraw=True)
