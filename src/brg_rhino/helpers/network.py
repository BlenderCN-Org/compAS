import ast

import brg_rhino.utilities as rhino

try:
    import Rhino
    from Rhino.Geometry import Point3d
    import rhinoscriptsyntax as rs
except ImportError as e:
    import platform
    if platform.system() == 'Windows':
        raise e


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'draw_network',
    'select_network_vertices',
    'select_network_vertex',
    'select_network_edges',
    'select_network_edge',
    'select_network_faces',
    'select_network_face',
    'get_network_vertices',
    'get_network_edges',
    'get_network_faces',
    'update_network_attributes',
    'update_network_vertex_attributes',
    'update_network_edge_attributes',
    'update_network_face_attributes',
    'display_network_vertex_labels',
    'display_network_edge_labels',
    'display_network_face_labels',
    'move_network',
    'move_network_vertex',
]


# ==============================================================================
# constructors
# ==============================================================================

# ==============================================================================
# draw
# ==============================================================================


def draw_network(network, name=None, layer=None, vertex_color=None, edge_color=None, **kwargs):
    name = name or network.attributes.get('name') or 'Network'
    layer = layer or network.attributes.get('layer')
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


def select_network_faces(network, message='Select network faces.'):
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.textdot)
    if guids:
        prefix = network.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'face' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        keys.append(key)
    return keys


def select_network_face(network, message='Select face.'):
    guid = rs.GetObjects(message, preselect=True, filter=rs.filter.textdot)
    if guid:
        prefix = network.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'face' in name:
            if not prefix or prefix in name:
                key = name[-1]
                return key
    return None


# ==============================================================================
# get
# ==============================================================================


def get_network_vertices(network, where, message='Get network vertices where'):
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


def get_network_edges(network, where, message='Get network edges where'):
    raise NotImplementedError


def get_network_faces(network, where, message='Get network faces where'):
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


def update_network_face_attributes(network, fkeys, names=None):
    if not network.dualdata:
        return
    if not names:
        names = sorted(network.dfa.keys())
    values = [network.dualdata.vertex[fkeys[0]][name] for name in names]
    if len(fkeys) > 1:
        for i, name in enumerate(names):
            for fkey in fkeys[1:]:
                if values[i] != network.dualdata.vertex[fkey][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = rhino.update_attributes(names, values)
    if values:
        for i, name in enumerate(names):
            if values[i] != '-':
                for fkey in fkeys:
                    try:
                        network.dualdata.vertex[fkey][name] = eval(values[i])
                    except:
                        network.dualdata.vertex[fkey][name] = values[i]
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
# geometry
# ==============================================================================


def move_network(network):
    color  = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
    origin = dict((key, network.vertex_coordinates(key)) for key in network.vertex)
    vertex = dict((key, network.vertex_coordinates(key)) for key in network.vertex)
    edges  = network.edges()
    start  = rhino.pick_point('Point to move from?')

    if not start:
        return

    def OnDynamicDraw(sender, e):
        current = list(e.CurrentPoint)
        vec = [current[i] - start[i] for i in range(3)]
        for key in vertex:
            vertex[key] = [origin[key][i] + vec[i] for i in range(3)]
        for u, v in iter(edges):
            sp = vertex[u]
            ep = vertex[v]
            sp = Point3d(*sp)
            ep = Point3d(*ep)
            e.Display.DrawDottedLine(sp, ep, color)

    rhino.delete_objects(rhino.get_objects(name='{0}.*'.format(network.attributes['name'])), False)

    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt('Point to move to?')
    gp.DynamicDraw += OnDynamicDraw
    gp.Get()

    if gp.CommandResult() == Rhino.Commands.Result.Success:
        end = list(gp.Point())
        vec = [end[i] - start[i] for i in range(3)]
        for key, attr in network.vertices_iter(True):
            attr['x'] += vec[0]
            attr['y'] += vec[1]
            attr['z'] += vec[2]
    network.draw()


def move_network_vertex(network, key, constraint=None, allow_off=None):
    color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
    nbrs  = [network.vertex_coordinates(nbr) for nbr in network.halfedge[key]]
    nbrs  = [Point3d(*xyz) for xyz in nbrs]

    def OnDynamicDraw(sender, e):
        for ep in nbrs:
            sp = e.CurrentPoint
            e.Display.DrawDottedLine(sp, ep, color)

    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt('Point to move to?')
    gp.DynamicDraw += OnDynamicDraw

    if constraint:
        if allow_off is not None:
            gp.Constrain(constraint, allow_off)
        else:
            gp.Constrain(constraint)

    gp.Get()

    if gp.CommandResult() == Rhino.Commands.Result.Success:
        pos = list(gp.Point())
        network.vertex[key]['x'] = pos[0]
        network.vertex[key]['y'] = pos[1]
        network.vertex[key]['z'] = pos[2]
    network.draw()


# ==============================================================================
# forces
# ==============================================================================


# def display_axial_forces(self,
#                          display=True,
#                          layer=None,
#                          scale=1.0,
#                          color_tension=None,
#                          color_compression=None):
#     tol = rhino.get_tolerance()
#     objects = rhino.get_objects(name='{0}.force:axial.*'.format(self.name))
#     rhino.delete_objects(objects)
#     if not display:
#         return
#     lines = []
#     layer = layer or self.layer
#     color_tension = color_tension or self.color['force:tension']
#     color_compression = color_compression or self.color['force:compression']
#     for u, v, attr in self.edges_iter(True):
#         sp     = self.vertex_coordinates(u)
#         ep     = self.vertex_coordinates(v)
#         force  = attr['f']
#         color  = color_tension if force > 0.0 else color_compression
#         radius = scale * ((force ** 2) ** 0.5 / 3.14159) ** 0.5
#         name   = '{0}.force:axial.{1}-{2}'.format(self.name, u, v)
#         if radius < tol:
#             continue
#         lines.append({
#             'start'  : sp,
#             'end'    : ep,
#             'name'   : name,
#             'color'  : color,
#             'radius' : radius,
#         })
#     rhino.xdraw_cylinders(lines, layer=layer, clear=False, redraw=True)


# def display_reaction_forces(self,
#                             display=True,
#                             layer=None,
#                             scale=1.0,
#                             color=None):
#     tol = rhino.get_tolerance()
#     objects = rhino.get_objects(name='{0}.force:reaction.*'.format(self.name))
#     rhino.delete_objects(objects)
#     if not display:
#         return
#     lines = []
#     layer = layer or self.layer
#     color = color or self.color['force:reaction']
#     for key, attr in self.vertices_iter(True):
#         if not attr['is_support']:
#             continue
#         r     = attr['rx'], attr['ry'], attr['rz']
#         sp    = self.vertex_coordinates(key)
#         ep    = [sp[i] + scale * r[i] for i in range(3)]
#         l     = sum((ep[i] - sp[i]) ** 2 for i in range(3)) ** 0.5
#         arrow = 'start'
#         name  = '{0}.force:reaction.{1}'.format(self.name, key)
#         if l < tol:
#             continue
#         lines.append({
#             'start' : sp,
#             'end'   : ep,
#             'name'  : name,
#             'color' : color,
#             'arrow' : arrow,
#         })
#     rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)


# def display_residual_forces(self,
#                             display=True,
#                             layer=None,
#                             scale=1.0,
#                             color=None):
#     tol = rhino.get_tolerance()
#     objects = rhino.get_objects(name='{0}.force:residual.*'.format(self.name))
#     rhino.delete_objects(objects)
#     if not display:
#         return
#     lines = []
#     layer = layer or self.layer
#     color = color or self.color['force:residual']
#     for key, attr in self.vertices_iter(True):
#         if attr['is_support']:
#             continue
#         r     = attr['rx'], attr['ry'], attr['rz']
#         sp    = self.vertex_coordinates(key)
#         ep    = [sp[i] + scale * r[i] for i in range(3)]
#         l     = sum((ep[i] - sp[i]) ** 2 for i in range(3)) ** 0.5
#         arrow = 'end'
#         name  = '{0}.force:residual.{1}'.format(self.name, key)
#         if l < tol:
#             continue
#         lines.append({'start' : sp,
#                       'end'   : ep,
#                       'name'  : name,
#                       'color' : color,
#                       'arrow' : arrow, })
#     rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)


# def display_selfweight(self,
#                        display=True,
#                        layer=None,
#                        scale=None,
#                        color=None):
#     objects = rhino.get_objects(name='{0}.force:selfweight.*'.format(self.name))
#     rhino.delete_objects(objects)
#     if not display:
#         return
#     lines = []
#     layer = layer or self.layer
#     color = color or self.color['force:selfweight']
#     scale = scale or self.scale['force:selfweight']
#     for key, attr in self.vertices_iter(True):
#         load  = 0, 0, attr['sw']
#         start = self.vertex_coordinates(key)
#         end   = [start[i] + scale * load[i] for i in range(3)]
#         name  = '{0}.force:selfweight.{1}'.format(self.name, key)
#         arrow = 'start'
#         lines.append({'start': start,
#                       'end'  : end,
#                       'name' : name,
#                       'color': color,
#                       'arrow': arrow, })
#     rhino.xdraw_lines(lines, layer=layer, clear=False)


# def display_resultant(self,
#                       keys,
#                       display=True,
#                       layer=None,
#                       scale=None,
#                       color=None):
#     objects = rhino.get_objects(name='{0}.force:resultant.*'.format(self.name))
#     rhino.delete_objects(objects)
#     if not display:
#         return
#     lines = []
#     layer = layer or self.layer
#     color = color or self.color['force:reaction']
#     scale = scale or self.scale['force:reaction']
#     x, y, z = 0, 0, 0
#     rx, ry, rz = 0, 0, 0
#     count = 0
#     for key in keys:
#         attr = self.vertex[key]
#         if not attr['is_anchor'] and not attr['is_fixed']:
#             continue
#         x     += attr['x']
#         y     += attr['y']
#         rx    += attr['rx']
#         ry    += attr['ry']
#         rz    += attr['rz']
#         count += 1
#     x  = x / count
#     y  = y / count
#     z  = z / count
#     start = x, y, z
#     end   = x + scale * rx, y + scale * ry, z + scale * rz
#     name  = '{0}.force:resultant.{1}'.format(self.name, keys)
#     arrow = 'start'
#     lines.append({'start': start,
#                   'end'  : end,
#                   'name' : name,
#                   'color': color,
#                   'arrow': arrow, })
#     rhino.xdraw_lines(lines, layer=layer, clear=False)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
