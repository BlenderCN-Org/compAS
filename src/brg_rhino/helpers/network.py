import ast

import brg_rhino.utilities as rhino

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


__all__ = []


# ==============================================================================
# constructors
# ==============================================================================


# ==============================================================================
# draw
# ==============================================================================


def draw_network(network, name=None, layer=None, vertex_color=None, edge_color=None, **kwargs):
    name = name or network.attributes['name']
    layer = layer or network.attributes['layer']
    # vertex color
    vcolor = dict((key, network.attributes['color.vertex']) for key in network)
    if isinstance(vertex_color, dict):
        vcolor.update(vertex_color)
    elif isinstance(vertex_color, basestring):
        pass
    elif isinstance(vertex_color, (tuple, list)):
        vcolor = dict((key, vertex_color) for key in network)
    else:
        pass
    # edge color
    ecolor = dict(((u, v), network.attributes['color.edge']) for u, v in network.edges_iter())
    if isinstance(edge_color, dict):
        ecolor.update(edge_color)
    elif isinstance(edge_color, basestring):
        pass
    elif isinstance(edge_color, (tuple, list)):
        ecolor = dict(((u, v), edge_color) for u, v in network.edges_iter())
    else:
        pass
    # points
    points = []
    for key, attr in network.vertices_iter(True):
        points.append({
            'pos': network.vertex_coordinates(key),
            'name': '{0}.vertex.{1}'.format(name, key),
            'color': vcolor[key]
        })
    # lines
    lines = []
    for u, v, attr in network.edges_iter(True):
        lines.append({
            'start': network.vertex_coordinates(u),
            'end': network.vertex_coordinates(v),
            'name': '{0}.edge.{1}-{2}'.format(name, u, v),
            'color': ecolor[(u, v)]
        })
    # drawing
    rhino.xdraw_points(
        points,
        layer=layer,
        clear=True,
        redraw=False
    )
    rhino.xdraw_lines(
        lines,
        layer=layer,
        clear=False,
        redraw=True
    )


# ==============================================================================
# select
# ==============================================================================


def select_network_vertices(network, message="Select network vertices"):
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


def select_network_vertex(network, message="Select a network vertex"):
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guid:
        prefix = network.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'vertex' in name:
            if not prefix or prefix in name:
                return name[-1]
    return None


def select_network_edges(network, message="Select network edges"):
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


def select_network_edge(network, message="Select a network edge"):
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


def get_network_vertices(network, where):
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


def get_network_vertex(network, where):
    raise NotImplementedError


def get_network_edges(network, where):
    raise NotImplementedError


def get_network_edge(network, where):
    raise NotImplementedError


# ==============================================================================
# attributes
# ==============================================================================


def update_network_attributes(network):
    names  = sorted(network.attributes.keys())
    values = [str(network.attributes[name]) for name in names]
    values = rhino.update_named_values(names, values)
    if values:
        for i, name in enumerate(names):
            value = values[i]
            try:
                network.attributes[name] = ast.literal_eval(value)
            except:
                network.attributes[name] = value
        return True
    return False


def update_network_vertex_attributes(network, keys, names=None):
    if not names:
        names = network.dva.keys()
    names = sorted(names)
    values = [network.vertex[keys[0]][name] for name in names]
    if len(keys) > 1:
        for i, name in enumerate(names):
            for key in keys[1:]:
                if values[i] != network.vertex[key][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = rhino.update_named_values(names, values)
    if values:
        for i, name in enumerate(names):
            value = values[i]
            if value != '-':
                for key in keys:
                    try:
                        network.vertex[key][name] = ast.literal_eval(value)
                    except:
                        network.vertex[key][name] = value
        return True
    return False


def update_network_edge_attributes(network, keys, names=None):
    if not names:
        names = network.dea.keys()
    names = sorted(names)
    u, v = keys[0]
    values = [network.edge[u][v][name] for name in names]
    if len(keys) > 1:
        for i, name in enumerate(names):
            for u, v in keys[1:]:
                if values[i] != network.edge[u][v][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = rhino.update_named_values(names, values)
    if values:
        for i, name in enumerate(names):
            value = values[i]
            if value != '-':
                for u, v in keys:
                    try:
                        network.edge[u][v][name] = ast.literal_eval(value)
                    except:
                        network.edge[u][v][name] = value
        return True
    return False


# ==============================================================================
# labels
# ==============================================================================


def display_network_vertex_labels(network, attr_name=None, **kwargs):
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
    rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=clear,
        redraw=redraw
    )


def display_network_edge_labels(network, attr_name, **kwargs):
    attr_name = attr_name or 'key'
    color = network.attributes.get('color.edge', (0, 0, 0))
    name = network.attributes.get('name', 'Network')
    float_precision = kwargs.get('float_precision', '1')
    layer = kwargs.get('layer', network.attributes.get('layer'))
    clear = kwargs.get('clear', False)
    redraw = kwargs.get('redraw', True)
    labels = []
    for index, u, v, attr in network.edges_enum(True):
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
    rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=clear,
        redraw=redraw
    )


def display_network_face_labels(network, attr_name, **kwargs):
    attr_name = attr_name or 'key'
    color = network.attributes.get('color.face', (0, 0, 0))
    name = network.attributes.get('name', 'Network')
    float_precision = kwargs.get('float_precision', '1')
    layer = kwargs.get('layer', network.attributes.get('layer'))
    clear = kwargs.get('clear', False)
    redraw = kwargs.get('redraw', True)
    labels = []
    for index, fkey in network.faces_enum():
        if attr_name == 'key':
            text = '{0}'.format(fkey)
        elif attr_name == 'index':
            text = str(index)
        else:
            raise NotImplementedError
        labels.append({
            'pos': network.face_centroid(fkey),
            'text': text,
            'name': '{0}.face.label.{1}'.format(name, fkey),
            'color': color
        })
    rhino.xdraw_labels(
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
