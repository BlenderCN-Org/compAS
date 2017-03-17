import ast

from compas.utilities import geometric_key
from compas.utilities.colors import color_to_colordict

from compas_rhino.geometry.surface import RhinoSurface

import compas_rhino as rhino

try:
    import Rhino
    import scriptcontext as sc
    import rhinoscriptsyntax as rs
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_from_guid',
    'mesh_from_surface',
    'mesh_from_surface_uv',
    'mesh_from_surface_heightfield',
    'draw_mesh',
    'select_mesh_vertices',
    'select_mesh_vertex',
    'select_mesh_edges',
    'select_mesh_edge',
    'select_mesh_faces',
    'select_mesh_face',
    'update_mesh_vertex_attributes',
    'update_mesh_edge_attributes',
    'update_mesh_face_attributes',
    'display_mesh_vertex_labels',
    'display_mesh_edge_labels',
    'display_mesh_face_labels',
]


# ==============================================================================
# constructors
# ==============================================================================


def mesh_from_guid(cls, guid, **kwargs):
    vertices, faces = rhino.get_mesh_vertices_and_faces(guid)
    faces = [face[: -1] if face[-2] == face[-1] else face for face in faces]
    mesh  = cls.from_vertices_and_faces(vertices, faces)
    mesh.attributes.update(kwargs)
    return mesh


def mesh_from_surface(cls, guid, **kwargs):
    gkey_xyz = {}
    faces = []
    obj = sc.doc.Objects.Find(guid)
    if not obj.Geometry.HasBrepForm:
        return
    brep = Rhino.Geometry.Brep.TryConvertBrep(obj.Geometry)
    for loop in brep.Loops:
        curve = loop.To3dCurve()
        segments = curve.Explode()
        face = []
        sp = segments[0].PointAtStart
        ep = segments[0].PointAtEnd
        sp_gkey = geometric_key(sp)
        ep_gkey = geometric_key(ep)
        gkey_xyz[sp_gkey] = sp
        gkey_xyz[ep_gkey] = ep
        face.append(sp_gkey)
        face.append(ep_gkey)
        for segment in segments[1:-1]:
            ep = segment.PointAtEnd
            ep_gkey = geometric_key(ep)
            face.append(ep_gkey)
            gkey_xyz[ep_gkey] = ep
        faces.append(face)
    gkey_index = dict((gkey, index) for index, gkey in enumerate(gkey_xyz))
    vertices = [list(xyz) for gkey, xyz in gkey_xyz.items()]
    faces = [[gkey_index[gkey] for gkey in f] for f in faces]
    mesh = cls.from_vertices_and_faces(vertices, faces)
    mesh.attributes.update(kwargs)
    return mesh


def mesh_from_surface_uv(cls, guid, density=(10, 10), **kwargs):
    raise NotImplementedError


def mesh_from_surface_heightfield(cls, guid, density=(10, 10), **kwargs):
    try:
        u, v = density
    except:
        u, v = density, density
    surface = RhinoSurface(guid)
    mesh = cls()
    mesh.attributes.update(kwargs)
    vertices = surface.heightfield(density=(u, v), over_space=True)
    for x, y, z in vertices:
        mesh.add_vertex(x=x, y=y, z=z)
    for i in range(v - 1):
        for j in range(u - 1):
            face = ((i + 0) * u + j,
                    (i + 0) * u + j + 1,
                    (i + 1) * u + j + 1,
                    (i + 1) * u + j)
            mesh.add_face(face)
    return mesh


# ==============================================================================
# drawing
# ==============================================================================


# change clear to clearlayer
# remove redraw?
# process color spec into color dict

def draw_mesh(mesh,
              layer=None,
              clear_layer=False,
              show_faces=False,
              show_vertices=True,
              show_edges=True,
              vertexcolor=None,
              edgecolor=None,
              facecolor=None):
    """
    Draw a mesh object in Rhino.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        layer (str): Optional. The layer to draw in. Default is ``None``.
        clear_layer (bool): Optional. Clear the drawing layer. Default is ``True``.
        show_faces (bool): Optional. Show the faces. Default is ``True``.
        show_vertices (bool): Optional. Show the vertices. Default is ``True``.
        show_edges (bool): Optional. Show the edges. Default is ``True``.
        vertexcolor (str, tuple, list, dict): Optional. The vertex color specification. Default is ``None``.
        edgecolor (str, tuple, list, dict): Optional. The edge color specification. Default is ``None``.
        facecolor (str, tuple, list, dict): Optional. The face color specification. Default is ``None``.
        redraw (bool): Optional. Redraw instructions. Default is ``True``.

    Note:
        Colors can be specifiedin different ways:

        * str: A hexadecimal color that will be applied to all elements subject to the specification.
        * tuple, list: RGB color that will be applied to all elements subject to the specification.
        * dict: RGB or hex color dict with a specification for some or all of the related elements.

    Important:
        RGB colors should specify color values between 0 and 255.

    """
    # set default options
    vertexcolor = color_to_colordict(vertexcolor,
                                     mesh.vertices(),
                                     default=mesh.attributes['color.vertex'],
                                     colorformat='rgb',
                                     normalize=False)
    edgecolor = color_to_colordict(edgecolor,
                                   mesh.edges(),
                                   default=mesh.attributes['color.edge'],
                                   colorformat='rgb',
                                   normalize=False)
    facecolor = color_to_colordict(facecolor,
                                   mesh.faces(),
                                   default=mesh.attributes['color.face'],
                                   colorformat='rgb',
                                   normalize=False)
    guids = rhino.get_objects(name='{0}.*'.format(mesh.attributes['name']))
    rhino.delete_objects(guids)
    if clear_layer:
        if not layer:
            rhino.clear_current_layer()
        else:
            rhino.clear_layers((layer, ))
    if show_faces:
        key_index = dict((key, index) for index, key in mesh.vertices_enum())
        xyz       = [mesh.vertex_coordinates(key) for key in mesh.vertices_iter()]
        faces     = []
        color     = mesh.attributes['color.face']
        for fkey in mesh.face:
            face = mesh.face_vertices(fkey, ordered=True)
            v = len(face)
            if v < 3:
                print 'Degenerate face: {0} => {1}'.format(fkey, face)
                continue
            if v == 3:
                faces.append([key_index[k] for k in face + [face[-1]]])
            elif v == 4:
                faces.append([key_index[k] for k in face])
            else:
                # a polygonal face
                # => triangulate
                c = len(xyz)
                xyz.append(mesh.face_center(fkey))
                for i in range(-1, len(face) - 1):
                    key = face[i]
                    nbr = face[i + 1]
                    vertices = [c, key_index[key], key_index[nbr], key_index[nbr]]
                    faces.append(vertices)
        rhino.xdraw_mesh(xyz,
                         faces,
                         color,
                         mesh.attributes['name'],
                         layer=layer,
                         clear=False,
                         redraw=False)
    if show_edges:
        lines = []
        color = mesh.attributes['color.edge']
        for u, v in mesh.edges_iter():
            lines.append({
                'start': mesh.vertex_coordinates(u),
                'end'  : mesh.vertex_coordinates(v),
                'name' : '{0}.edge.{1}-{2}'.format(mesh.attributes['name'], u, v),
                'color': edgecolor.get((u, v), color),
            })
        rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=False)
    if show_vertices:
        points = []
        color  = mesh.attributes['color.vertex']
        for key in mesh.vertices_iter():
            points.append({
                'pos'  : mesh.vertex_coordinates(key),
                'name' : '{0}.vertex.{1}'.format(mesh.attributes['name'], key),
                'color': vertexcolor.get(key, color),
            })
        rhino.xdraw_points(points, layer=layer, clear=False, redraw=False)
    rs.Redraw()

# ==============================================================================
# selection
# ==============================================================================


def select_mesh_vertices(mesh, message="Select mesh vertices."):
    """Select vertices of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select mesh vertices."``

    Returns:
        list: The keys of the selected vertices.

    Note:
        Selection is based on naming conventions.
        When a mesh is drawn using the function :func:`draw_mesh`,
        the point objects representing the vertices get assigned a name that
        has the following pattern::

            '{0}.vertex.{1}'.format(mesh.attributes['name'], key)

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as rhino
            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            keys = rhino.select_mesh_vertices(mesh)

            print keys


    See Also:
        * :func:`select_mesh_edges`
        * :func:`select_mesh_faces`

    """
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guids:
        prefix = mesh.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'vertex' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        key = ast.literal_eval(key)
                        keys.append(key)
    return keys


def select_mesh_vertex(mesh, message="Select a mesh vertex"):
    """Select one vertex of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select mesh vertex."``

    Returns:
        * str: The key of the selected vertex.
        * None: If no vertex was selected.

    See Also:
        * :func:`select_mesh_vertices`

    """
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.point | rs.filter.textdot)
    if guid:
        prefix = mesh.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'vertex' in name:
            if not prefix or prefix in name:
                key = name[-1]
                key = ast.literal_eval(key)
                return key
    return None


def select_mesh_edges(mesh, message="Select mesh edges"):
    """Select edges of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select mesh edges."``

    Returns:
        list: The keys of the selected edges. Each key is a *uv* pair.

    Note:
        Selection is based on naming conventions.
        When a mesh is drawn using the function :func:`draw_mesh`,
        the curve objects representing the edges get assigned a name that
        has the following pattern::

            '{0}.edge.{1}-{2}'.format(mesh.attributes['name'], u, v)

    See Also:
        * :func:`select_mesh_vertices`
        * :func:`select_mesh_faces`

    """
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guids:
        prefix = mesh.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'edge' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        u, v = key.split('-')
                        u = ast.literal_eval(u)
                        v = ast.literal_eval(v)
                        keys.append((u, v))
    return keys


def select_mesh_edge(mesh, message="Select a mesh edge"):
    """Select one edge of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select mesh edges."``

    Returns:
        tuple: The key of the selected edge.
        None: If no edge was selected.

    See Also:
        * :func:`select_mesh_edges`

    """
    guid = rs.GetObject(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
    if guid:
        prefix = mesh.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'edge' in name:
            if not prefix or prefix in name:
                key = name[-1]
                u, v = key.split('-')
                u = ast.literal_eval(u)
                v = ast.literal_eval(v)
                return u, v
    return None


def select_mesh_faces(mesh, message='Select mesh faces.'):
    """Select faces of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select mesh edges."``

    Returns:
        list: The keys of the selected faces.

    Note:
        Selection of faces is based on naming conventions.
        When a mesh is drawn using the function :func:`draw_mesh`,
        the curve objects representing the edges get assigned a name that
        has the following pattern::

            '{0}.edge.{1}-{2}'.format(mesh.attributes['name'], u, v)

    Example:

        .. code-block:: python
            :emphasize-lines: 14

            import compas
            import compas_rhino as rhino

            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            find_mesh_faces(mesh, mesh.leaves())

            rhino.draw_mesh(mesh)
            rhino.display_mesh_face_labels(mesh)

            fkeys = rhino.select_mesh_faces(mesh)

            print fkeys


    See Also:
        * :func:`select_mesh_vertices`
        * :func:`select_mesh_edges`

    """
    keys = []
    guids = rs.GetObjects(message, preselect=True, filter=rs.filter.textdot)
    if guids:
        prefix = mesh.attributes['name']
        seen = set()
        for guid in guids:
            name = rs.ObjectName(guid).split('.')
            if 'face' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    if not seen.add(key):
                        key = ast.literal_eval(key)
                        keys.append(key)
    return keys


def select_mesh_face(mesh, message='Select face.'):
    """Select one face of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        message (str): Optional. The message to display to the user.
            Default is ``"Select mesh edges."``

    Returns:
        tuple: The key of the selected face.
        None: If no face was selected.

    See Also:
        * :func:`select_mesh_faces`

    """
    guid = rs.GetObjects(message, preselect=True, filter=rs.filter.textdot)
    if guid:
        prefix = mesh.attributes['name']
        name = rs.ObjectName(guid).split('.')
        if 'face' in name:
            if not prefix or prefix in name:
                key = name[-1]
                key = ast.literal_eval(key)
                return key
    return None


# ==============================================================================
# attributes
# ==============================================================================


def update_mesh_attributes(mesh):
    """Update the attributes of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.

    Returns:
        bool: ``True`` if the update was successful, and ``False`` otherwise.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino
            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            if compas_rhino.update_mesh_attributes(mesh):
                print 'mesh attributes updated'
            else:
                print 'mesh attributres not updated'


    See Also:
        * :func:`update_mesh_vertex_attributes`
        * :func:`update_mesh_edge_attributes`
        * :func:`update_mesh_face_attributes`

    """
    names  = sorted(mesh.attributes.keys())
    values = [str(mesh.attributes[name]) for name in names]
    values = rhino.update_named_values(names, values)
    if values:
        for i, name in enumerate(names):
            value = values[i]
            try:
                mesh.attributes[name] = ast.literal_eval(value)
            except:
                mesh.attributes[name] = value
        return True
    return False


def update_mesh_vertex_attributes(mesh, keys, names=None):
    """Update the attributes of the vertices of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        keys (tuple, list): The keys of the vertices to update.
        names (tuple, list): Optional. The names of the atrtibutes to update.
            Defaults to ``None``. If ``None``, all attributes are included in the
            update.

    Returns:
        bool: ``True`` if the update was successful, and ``False`` otherwise.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino

            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            keys = mesh.vertices()

            if compas_rhino.update_mesh_vertex_attributes(mesh, keys):
                print 'mesh vertex attributes updated'
            else:
                print 'mesh vertex attributes not updated'


    See Also:
        * :func:`update_mesh_attributes`
        * :func:`update_mesh_edge_attributes`
        * :func:`update_mesh_face_attributes`

    """
    if not names:
        names = mesh.default_vertex_attributes.keys()
    names = sorted(names)
    values = [mesh.vertex[keys[0]][name] for name in names]
    if len(keys) > 1:
        for i, name in enumerate(names):
            for key in keys[1:]:
                if values[i] != mesh.vertex[key][name]:
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
                        mesh.vertex[key][name] = ast.literal_eval(value)
                    except:
                        mesh.vertex[key][name] = value
        return True
    return False


def update_mesh_edge_attributes(mesh, keys, names=None):
    """Update the attributes of the edges of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        keys (tuple, list): The keys of the edges to update. Note that the keys
            should be pairs of vertex keys.
        names (tuple, list): Optional. The names of the atrtibutes to update.
            Defaults to ``None``. If ``None``, all attributes are included in the
            update.

    Returns:
        bool: ``True`` if the update was successful, and ``False`` otherwise.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino

            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            keys = mesh.edges()

            if compas_rhino.update_mesh_edge_attributes(mesh, keys):
                print 'mesh edge attributes updated'
            else:
                print 'mesh edge attributes not updated'


    See Also:
        * :func:`update_mesh_attributes`
        * :func:`update_mesh_vertex_attributes`
        * :func:`update_mesh_face_attributes`

    """
    if not names:
        names = mesh.default_edge_attributes.keys()
    names = sorted(names)
    u, v = keys[0]
    values = [mesh.edge[u][v][name] for name in names]
    if len(keys) > 1:
        for i, name in enumerate(names):
            for u, v in keys[1:]:
                if values[i] != mesh.edge[u][v][name]:
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
                        mesh.edge[u][v][name] = ast.literal_eval(value)
                    except:
                        mesh.edge[u][v][name] = value
        return True
    return False


def update_mesh_face_attributes(mesh, fkeys, names=None):
    """Update the attributes of the faces of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        keys (tuple, list): The keys of the faces to update.
        names (tuple, list): Optional. The names of the atrtibutes to update.
            Defaults to ``None``. If ``None``, all attributes are included in the
            update.

    Returns:
        bool: ``True`` if the update was successful, and ``False`` otherwise.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino

            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            keys = mesh.faces()

            if compas_rhino.update_mesh_face_attributes(mesh, keys):
                print 'mesh face attributes updated'
            else:
                print 'mesh face attributes not updated'


    See Also:
        * :func:`update_mesh_attributes`
        * :func:`update_mesh_vertex_attributes`
        * :func:`update_mesh_edge_attributes`

    """
    if not mesh.dualdata:
        return
    if not names:
        names = sorted(mesh.default_face_attributes.keys())
    values = [mesh.dualdata.vertex[fkeys[0]][name] for name in names]
    if len(fkeys) > 1:
        for i, name in enumerate(names):
            for fkey in fkeys[1:]:
                if values[i] != mesh.dualdata.vertex[fkey][name]:
                    values[i] = '-'
                    break
    values = map(str, values)
    values = rhino.update_attributes(names, values)
    if values:
        for i, name in enumerate(names):
            if values[i] != '-':
                for fkey in fkeys:
                    try:
                        mesh.dualdata.vertex[fkey][name] = eval(values[i])
                    except:
                        mesh.dualdata.vertex[fkey][name] = values[i]
        return True
    return False


# ==============================================================================
# labels
# ==============================================================================


def display_mesh_vertex_labels(mesh, attr_name=None, layer=None, color=None, formatter=None):
    """Display labels for the vertices of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        attr_name (str): Optional. The name of the attribute value to display in the label.
            Default is ``None``. If ``None``, the key of the vertex is displayed.
        layer (str): Optional. The layer to draw in. Default is ``None``.
        color (str, tuple, list, dict): Optional. The color specification. Default is ``None``.
            The following values are supported:

                * str: A HEX color. For example, ``'#ff0000'``.
                * tuple, list: RGB color. For example, ``(255, 0, 0)``.
                * dict: A dictionary of RGB and/or HEX colors.

            If ``None``, the default vertex color of the mesh will be used.
        formatter (callable): Optional. A formatting function. Default is ``None``.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino

            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            compas_rhino.display_mesh_vertex_labels(mesh)


        .. code-block:: python

            import compas
            import compas_rhino

            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            def formatter(value):
                return '{0:.3f}'.format(value)

            compas_rhino.display_mesh_vertex_labels(mesh, attr_name='x' formatter=formatter)


    See Also:
        * :func:`display_mesh_edge_labels`
        * :func:`display_mesh_face_labels`

    """
    if not attr_name:
        attr_name = 'key'

    colordict = color_to_colordict(color,
                                   mesh.vertices(),
                                   default=mesh.attributes['color.vertex'],
                                   colorformat='rgb',
                                   normalize=False)
    if formatter:
        if not callable(formatter):
            raise Exception('The provided formatter is not callable.')
    else:
        formatter = str

    labels = []

    for index, key, attr in mesh.vertices_enum(True):
        if 'key' == attr_name:
            value = key
        elif 'index' == attr_name:
            value = index
        else:
            value = attr[attr_name]

        labels.append({'pos'  : mesh.vertex_coordinates(key),
                       'text' : formatter(value),
                       'name' : '{0}.vertex.label.{1}'.format(mesh.attriutes['name'], key),
                       'color': colordict[key], })

    rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=False,
        redraw=True
    )


def display_mesh_edge_labels(mesh, attr_name=None, layer=None, color=None, formatter=None):
    """Display labels for the edges of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        attr_name (str): Optional. The name of the attribute value to display in the label.
            Default is ``None``. If ``None``, the key of the edge is displayed.
        layer (str): Optional. The layer to draw in. Default is ``None``.
        color (str, tuple, list, dict): Optional. The color specification. Default is ``None``.
            The following values are supported:

                * str: A HEX color. For example, ``'#ff0000'``.
                * tuple, list: RGB color. For example, ``(255, 0, 0)``.
                * dict: A dictionary of RGB and/or HEX colors.

            If ``None``, the default edge color of the mesh will be used.
        formatter (callable): Optional. A formatting function. Default is ``None``.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino

            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            compas_rhino.display_mesh_edge_labels(mesh)


    See Also:
        * :func:`display_mesh_vertex_labels`
        * :func:`display_mesh_face_labels`

    """
    if not attr_name:
        attr_name = 'key'

    colordict = color_to_colordict(color,
                                   mesh.edges(),
                                   default=mesh.attributes['color.edge'],
                                   colorformat='rgb',
                                   normalize=False)
    if formatter:
        if not callable(formatter):
            raise Exception('The provided formatter is not callable.')
    else:
        formatter = str

    labels = []

    for index, u, v, attr in mesh.edges_enum(True):

        if attr_name == 'key':
            value = '{0}-{1}'.format(u, v)
        elif attr_name == 'index':
            value = index
        else:
            value = attr[attr_name]

        labels.append({'pos'  : mesh.edge_midpoint(u, v),
                       'text' : formatter(value),
                       'name' : '{0}.edge.label.{1}-{2}'.format(mesh.attributes['name'], u, v),
                       'color': colordict[(u, v)], })

    rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=False,
        redraw=True
    )


def display_mesh_face_labels(mesh, attr_name=None, layer=None, color=None, formatter=None):
    """Display labels for the faces of a mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        attr_name (str): Optional. The name of the attribute value to display in the label.
            Default is ``None``. If ``None``, the key of the face is displayed.
        layer (str): Optional. The layer to draw in. Default is ``None``.
        color (str, tuple, list, dict): Optional. The color specification. Default is ``None``.
            The following values are supported:

                * str: A HEX color. For example, ``'#ff0000'``.
                * tuple, list: RGB color. For example, ``(255, 0, 0)``.
                * dict: A dictionary of RGB and/or HEX colors.

            If ``None``, the default face color of the mesh will be used.
        formatter (callable): Optional. A formatting function. Default is ``None``.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino

            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            compas_rhino.display_mesh_face_labels(mesh)


    See Also:
        * :func:`display_mesh_vertex_labels`
        * :func:`display_mesh_edge_labels`

    """
    if not attr_name:
        attr_name = 'key'

    colordict = color_to_colordict(color,
                                   mesh.faces(),
                                   default=mesh.attributes['color.face'],
                                   colorformat='rgb',
                                   normalize=False)

    if formatter:
        if not callable(formatter):
            raise Exception('The provided formatter is not callable.')
    else:
        formatter = str

    labels = []

    for index, fkey in mesh.faces_enum():
        if attr_name == 'key':
            value = fkey
        elif attr_name == 'index':
            value = index
        else:
            value = mesh.facedata[fkey][attr_name]

        labels.append({
            'pos'  : mesh.face_centroid(fkey),
            'text' : formatter(value),
            'name' : '{0}.face.label.{1}'.format(mesh.attributes['name'], fkey),
            'color': colordict[fkey]
        })

    rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=False,
        redraw=True
    )


# ==============================================================================
# geometry
# ==============================================================================


def display_mesh_vertex_normals(mesh,
                                display=True,
                                layer=None,
                                scale=1.0,
                                color=(0, 0, 255)):
    guids = rhino.get_objects(name='{0}.vertex.normal.*'.format(mesh.attributes['name']))
    rhino.delete_objects(guids)
    if not display:
        return
    lines = []
    for key in mesh.vertex:
        nv   = mesh.vertex_normal(key)
        sp   = mesh.vertex_coordinates(key)
        ep   = [sp[axis] + nv[axis] for axis in range(3)]
        name = '{0}.vertex.normal.{1}'.format(mesh.attributes['name'], key)
        lines.append({
            'start' : sp,
            'end'   : ep,
            'name'  : name,
            'color' : color,
            'arrow' : 'end',
        })
    rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)


def display_mesh_face_normals(mesh,
                              display=True,
                              layer=None,
                              scale=1.0,
                              color=(0, 0, 255)):
    guids = rhino.get_objects(name='{0}.face.normal.*'.format(mesh.attributes['name']))
    rhino.delete_objects(guids)
    if not display:
        return
    lines = []
    for fkey in mesh.face:
        nv   = mesh.face_normal(fkey)
        sp   = mesh.face_center(fkey)
        ep   = [sp[axis] + nv[axis] for axis in range(3)]
        name = '{0}.face.normal.{1}'.format(mesh.attributes['name'], fkey)
        lines.append({
            'start' : sp,
            'end'   : ep,
            'name'  : name,
            'color' : color,
            'arrow' : 'end',
        })
    rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)


# ==============================================================================
# forces
# ==============================================================================


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
