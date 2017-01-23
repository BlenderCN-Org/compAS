from brg_rhino.mixins import Mixin
import brg_rhino.utilities as rhino


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['EditAttributes', ]


def edit_vertex_attributes(datastructure, keys, names=None):
    if not names:
        names = sorted(datastructure.dva.keys())
    values = [datastructure.vertex[keys[0]][name] for name in names]
    if len(keys) > 1:
        for i, name in enumerate(names):
            for key in keys[1:]:
                if values[i] != datastructure.vertex[key][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = rhino.update_attributes(names, values)
    if values:
        for i, name in enumerate(names):
            if values[i] != '-':
                for key in keys:
                    try:
                        datastructure.vertex[key][name] = eval(values[i])
                    except:
                        datastructure.vertex[key][name] = values[i]
        return True
    return False


def edit_edge_attributes(datastructure, keys, names=None):
    if not names:
        names = sorted(datastructure.dea.keys())
    u, v = keys[0]
    values = [datastructure.edge[u][v][name] for name in names]
    if len(keys) > 1:
        for i, name in enumerate(names):
            for u, v in keys[1:]:
                if values[i] != datastructure.edge[u][v][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = rhino.update_attributes(names, values)
    if values:
        for i, name in enumerate(names):
            if values[i] != '-':
                for u, v in keys:
                    try:
                        datastructure.edge[u][v][name] = eval(values[i])
                    except:
                        datastructure.edge[u][v][name] = values[i]
        return True
    return False


def edit_face_attributes(datastructure, fkeys, names=None):
    if not datastructure.dualdata:
        return
    if not names:
        names = sorted(datastructure.dfa.keys())
    values = [datastructure.dualdata.vertex[fkeys[0]][name] for name in names]
    if len(fkeys) > 1:
        for i, name in enumerate(names):
            for fkey in fkeys[1:]:
                if values[i] != datastructure.dualdata.vertex[fkey][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = rhino.update_attributes(names, values)
    if values:
        for i, name in enumerate(names):
            if values[i] != '-':
                for fkey in fkeys:
                    try:
                        datastructure.dualdata.vertex[fkey][name] = eval(values[i])
                    except:
                        datastructure.dualdata.vertex[fkey][name] = values[i]
        return True
    return False


class EditAttributes(Mixin):
    """"""

    edit_vertex_attributes = edit_vertex_attributes
    edit_edge_attributes = edit_edge_attributes
    edit_face_attributes = edit_face_attributes


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    mixin = EditAttributes()

    print mixin.edit_vertex_attributes.im_self
    print mixin.edit_vertex_attributes.im_class
