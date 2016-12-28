"""Rhino-specific utilities for network datastructures."""


from brg_rhino.utilities.drawing import xdraw_labels


try:
    import rhinoscriptsyntax as rs
except ImportError as e:
    import platform
    if platform.system() == 'Windows':
        raise e


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


# ==============================================================================
# draw
# ==============================================================================


def draw(network, **kwargs):
    raise NotImplementedError


# ==============================================================================
# select
# ==============================================================================


def select_vertices(network, message="Select network vertices"):
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guids:
        prefix = network.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'vertex' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        keys.append(key)
    return keys


def select_vertex(network, message="Select a network vertex"):
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guid:
        prefix = network.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'vertex' in name:
            if not prefix or prefix in name:
                return name[-1]
    return None


def select_edges(network, message="Select network edges"):
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guids:
        prefix = network.attributes['name']
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


def select_edge(network, message="Select a network edge"):
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guid:
        prefix = network.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'edge' in name:
            if not prefix or prefix in name:
                key = name[-1]
                return tuple(key.split('-'))
    return None


# ==============================================================================
# get
# ==============================================================================


def get_vertices(network, where):
    """Get netwerk vertices for which a certain condition is ``True``.

    Parameters:
        network (brg.datastructures.network.network.Network) :
            A network data structure.
        where (dict) : A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.

    Returns:
        list :
            A list of vertex keys that satisfy the conditions.

    Examples:
        >>> keys = get_vertices(network, where={'x': 0.0})

    """
    raise NotImplementedError


def get_vertex(network, where):
    raise NotImplementedError


def get_edges(network, where):
    raise NotImplementedError


def get_edge(network, where):
    raise NotImplementedError


# ==============================================================================
# attributes
# ==============================================================================


def update_attributes(network):
    raise NotImplementedError


def update_vertex_attributes(network, key):
    raise NotImplementedError


def update_edge_attributes(network, key):
    raise NotImplementedError


# ==============================================================================
# labels
# ==============================================================================


def display_vertex_labels(network, attr_name=None, **kwargs):
    attr_name = attr_name or 'key'
    color = network.attributes.get('color.vertex', (0, 0, 0))
    name = network.attributes.get('name', 'Network')
    float_precision = kwargs.get('float_precision', '1')
    layer = kwargs.get('layer', network.attributes.get('layer'))
    clear = kwargs.get('clear', False)
    redraw = kwargs.get('redraw', True)
    labels = []
    for index, key, attr in network.vertices_enum(True):
        if attr_name == 'key':
            text = key
        elif attr_name == 'index':
            text = str(index)
        else:
            value = attr[attr_name]
            if isinstance(value, float):
                text = '{0:.{1}f}'.format(value, float_precision)
            else:
                text = str(value)
        labels.append({
            'pos': network.vertex_coordinates(key),
            'text': text,
            'name': '{0}.vertex.label.{1}'.format(name, key),
            'color': color
        })
    xdraw_labels(
        labels,
        layer=layer,
        clear=clear,
        redraw=redraw
    )


def display_edge_labels(network, attr_name, **kwargs):
    attr_name = attr_name or 'key'
    color = network.attributes.get('color.edge', (0, 0, 0))
    name = network.attributes.get('name', 'Network')
    float_precision = kwargs.get('float_precision', '1')
    layer = kwargs.get('layer', network.attributes.get('layer'))
    clear = kwargs.get('clear', False)
    redraw = kwargs.get('redraw', True)
    labels = []
    for index, (u, v), attr in network.edges_enum(True):
        if attr_name == 'key':
            text = '{0}-{1}'.format(u, v)
        elif attr_name == 'index':
            text = str(index)
        else:
            value = attr[attr_name]
            if isinstance(value, float):
                text = '{0:.{1}f}'.format(value, float_precision)
            else:
                text = str(value)
        labels.append({
            'pos': network.edge_midpoint(u, v),
            'text': text,
            'name': '{0}.edge.label.{1}-{2}'.format(name, u, v),
            'color': color
        })
    xdraw_labels(
        labels,
        layer=layer,
        clear=clear,
        redraw=redraw
    )


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
