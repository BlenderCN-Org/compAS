# -*- coding: utf-8 -*-

try:
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
__date__       = 'Jul 18, 2015'


__all__ = [
    'create_layers',
    'clear_layers',
    'delete_layers'
]


def create_layers(layers):
    def recurse(layers, parent=None):
        for name in layers:
            if not name:
                continue
            fullname = name
            if parent:
                fullname = parent + '::' + name
            try:
                attr = layers[name]
            except TypeError:
                attr = {}
            attr = attr or {}
            color   = attr.get('color', (0, 0, 0))
            visible = attr.get('visible', True)
            locked  = attr.get('locked', False)
            if not rs.IsLayer(fullname):
                rs.AddLayer(fullname, color, visible, locked)
            if 'layers' in attr :
                recurse(attr['layers'], fullname)
    rs.EnableRedraw(False)
    recurse(layers)
    rs.EnableRedraw(True)


def clear_layers(layers):
    to_delete = []
    def recurse(layers):
        for layer in layers:
            if not rs.IsLayer(layer):
                continue
            rs.ShowObjects([guid for guid in rs.HiddenObjects() if rs.ObjectLayer(guid) == layer])
            to_delete.extend(rs.ObjectsByLayer(layer))
            if rs.LayerChildCount(layer):
                recurse(rs.LayerChildren(layer))
    rs.EnableRedraw(False)
    recurse(layers)
    for guid in to_delete:
        obj = find_object(guid)
        if not obj:
            continue
        purge_object(obj.RuntimeSerialNumber)
    rs.EnableRedraw(True)


def delete_layers(layers):
    to_delete = []
    def recurse(layers, parent=None):
        for name in layers:
            if not name:
                continue
            fullname = name
            if parent:
                fullname = parent + '::' + name
            try:
                attr = layers[name]
            except TypeError:
                attr = {}
            if 'layers' in attr:
                recurse(attr['layers'], fullname)
            to_delete.append(fullname)
    rs.EnableRedraw(False)
    recurse(layers)
    for layer in to_delete:
        if rs.IsLayer(layer):
            rs.DeleteLayer(layer)
    rs.EnableRedraw(True)


# ==============================================================================
# ==============================================================================

if __name__ == "__main__":

    layers = {
        '1': {'layers': {
            '1.1': {},
            '1.2': {},
            '1.3': {'layers': {
                '1.3.1': {},
            }},
        }},
        '2': {'layers': {
            '2.1': {},
        }},
    }

    create_layers(layers)
