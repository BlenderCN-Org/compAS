# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$


from brg_rhino.datastructures.mixins import Mixin
import brg_rhino.utilities as rhino


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Jun 19, 2015'


__all__ = [
    'EditAttributes',
]


# class DisplayAttributes(Mixin):
#     """"""

#     def show_vertex_attributes(self, keys, name):


class EditAttributes(Mixin):
    """"""

    def edit_vertex_attributes(self, keys, names=None):
        if not names:
            names = sorted(self.default_vertex_attributes.keys())
        values = [self.vertex[keys[0]][name] for name in names]
        if len(keys) > 1:
            for i, name in enumerate(names):
                for key in keys[1:]:
                    if values[i] != self.vertex[key][name]:
                        values[i] = '-'
                        break
        values = map(str, values)
        values = rhino.update_attributes(names, values)
        if values:
            for i, name in enumerate(names):
                if values[i] != '-':
                    for key in keys:
                        try:
                            self.vertex[key][name] = eval(values[i])
                        except:
                            self.vertex[key][name] = values[i]
            return True
        return False

    def edit_edge_attributes(self, keys, names=None):
        if not names:
            names = sorted(self.defaut_edge_attributes.keys())
        u, v = keys[0]
        values = [self.edge[u][v][name] for name in names]
        if len(keys) > 1:
            for i, name in enumerate(names):
                for u, v in keys[1:]:
                    if values[i] != self.edge[u][v][name]:
                        values[i] = '-'
                        break
        values = map(str, values)
        values = rhino.update_attributes(names, values)
        if values:
            for i, name in enumerate(names):
                if values[i] != '-':
                    for u, v in keys:
                        try:
                            self.edge[u][v][name] = eval(values[i])
                        except:
                            self.edge[u][v][name] = values[i]
            return True
        return False

    def edit_face_attributes(self, fkeys, names=None):
        if not self.dual:
            return
        if not names:
            names = sorted(self.defaut_face_attributes.keys())
        values = [self.dual.vertex[fkeys[0]][name] for name in names]
        if len(fkeys) > 1:
            for i, name in enumerate(names):
                for fkey in fkeys[1:]:
                    if values[i] != self.dual.vertex[fkey][name]:
                        values[i] = '-'
                        break
        values = map(str, values)
        values = rhino.update_attributes(names, values)
        if values:
            for i, name in enumerate(names):
                if values[i] != '-':
                    for fkey in fkeys:
                        try:
                            self.dual.vertex[fkey][name] = eval(values[i])
                        except:
                            self.dual.vertex[fkey][name] = values[i]
            return True
        return False
