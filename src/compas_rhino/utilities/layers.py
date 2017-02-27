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
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'create_layers',
    'clear_layers',
    'clear_current_layer',
    'delete_layers',
]


def create_layers(layers):
    """Create layers in Rhino.

    Parameters:
        layers (dict): Structured layer information. The keys of the dictionary
            are layer names. The values are dictionaries themselves with the
            following (optional) items:

                - color => RGB tuple
                - visible => True / False
                - locked => True / False
                - layers => a dictionary of child layers with the same structure as described

    Examples:

        .. code-block:: python

            layers = {
                'Main': {
                    'layers': {
                        'Sub1': {'color': (255, 0, 0)},
                        'Sub2': {},
                        'Sub3': {'visible': False, 'layers': {
                            'Sub31': {},
                            'Sub32': {},
                            ...
                        }}
                    }
                }
            }

            create_layers(layers)

    """

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


def clear_layers(layers, clear_children=True):
    """Clear all objects from the given layers.

    Parameters:
        layers (list): A list of layer names.
        clear_children (bool): Optional. The children of the layers in the list
            will also be cleared if ``True``. Default is ``True``.

    Note:
        This function is typically used in combination with :func:`.create_layers`.
        The latter requires a layer structure, for example in the form of a dict,
        rather than a list of layer names. All layers in the structured layer dict
        can be cleared by simply taking the keys of the dict, while setting the
        flag for clearing the child layers to ``True``.

    Examples:
        >>> layers = {'Main': {'layers': {'Sub1': {}, 'Sub2': {'layers': {'SubSub1': {}}}}}}
        >>> create_layers(layers)
        >>> clear_layers(layers)

    """
    to_delete = []

    def recurse(layers):
        for layer in layers:
            if not layer:
                continue

            if not rs.IsLayer(layer):
                continue

            rs.ShowObjects([guid for guid in rs.HiddenObjects() if rs.ObjectLayer(guid) == layer])
            to_delete.extend(rs.ObjectsByLayer(layer))

            if clear_children:
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


def clear_current_layer():
    layer = rs.CurrentLayer()
    clear_layers((layer, ))


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
