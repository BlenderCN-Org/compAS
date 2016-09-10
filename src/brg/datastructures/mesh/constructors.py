import os
import json

from brg.files.obj import OBJ
from brg.utilities.maps import geometric_key


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2015-12-03 13:38:15'


__all__ = [
    'mesh_from_vertices_and_faces',
    'mesh_from_obj',
    'mesh_from_data',
    'mesh_from_boundary',
    'mesh_from_points',
]


def mesh_from_vertices_and_faces(cls, vertices, faces):
    mesh = cls()
    for x, y, z in vertices:
        mesh.add_vertex(x=x, y=y, z=z)
    for face in faces:
        mesh.add_face(face)
    return mesh


# def mesh_from_multiple(cls, meshes):
#     vertices = []
#     faces = []
#     gkey_index = {}
#     index = 0
#     for mesh in meshes:
#         for key in mesh.vertex:
#             xyz = mesh.vertex_coordinates(key)
#             gkey = geometric_key(xyz, '3f')
#             if gkey not in gkey_index:
#                 gkey_index[gkey] = index
#                 vertices.append(xyz)
#                 index += 1
#         for fkey in mesh.face:
#             faces.append([])
#             for key in mesh.face_vertices(fkey, True):
#                 xyz = mesh.vertex_coordinates(key)
#                 gkey = geometric_key(xyz, '3f')
#                 faces[-1].append(gkey_index[gkey])
#     mesh = cls.from_vertices_and_faces(vertices, faces)
#     return mesh


def mesh_from_obj(cls, filepath, **kwargs):
    """Initialise a mesh from the data described in an obj file.

    Parameters:
        filepath (str): The path to the obj file.

    Returns:
        ABCMesh: Mesh of type cls.
    """
    mesh = cls()
    mesh.attributes.update(kwargs)
    obj = OBJ(filepath)
    vertices = obj.parser.vertices
    faces = obj.parser.faces
    for x, y, z in vertices:
        mesh.add_vertex(x=x, y=y, z=z)
    for face in faces:
        mesh.add_face(face)
    return mesh


def mesh_from_dxf(cls, filepath):
    raise NotImplementedError


def mesh_from_stl(cls, filepath):
    raise NotImplementedError


def mesh_from_json(cls, filepath, **kwargs):
    data = None
    with open(filepath, 'rb') as fp:
        data = json.load(fp)
    mesh = cls.from_data(data)
    return mesh


def mesh_from_data(cls, data):
    """Construct a mesh from actual mesh data.

    This function should be used in combination with the data obtained from
    `mesh.data`.

    Parameters:
        data (dict): The data dictionary.

    Returns:
        Mesh: A Mesh of type cls.
    """
    mesh = cls()
    mesh.data = data
    return mesh


# differentiate between delaunay of boundary and delaunay in boundary
# use nurbs curves?
# differentiate between config and **kwargs
def mesh_from_boundary(cls,
                       boundary,
                       holes=None,
                       spacing=1.0,
                       do_smooth=False,
                       **kwargs):
    from brg.utilities.scriptserver import ScriptServer
    scriptdir = os.path.join(os.path.dirname(__file__), '_scripts')
    server = ScriptServer(scriptdir)
    config = {
        'do_smooth': do_smooth,
        'dva': cls.default_vertex_attributes,
        'dea': cls.default_edge_attributes,
        'dfa': cls.default_face_attributes
    }
    config.update(kwargs)
    res = server.mesh_from_boundary(
        boundary=boundary,
        holes=holes,
        spacing=spacing,
        config=config,
    )
    mesh = cls.from_data(res['data'])
    return mesh


# differentiate between config and **kwargs
def mesh_from_points(cls,
                     points,
                     do_smooth=False,
                     **kwargs):
    from brg.utilities.scriptserver import ScriptServer
    scriptdir = os.path.join(os.path.dirname(__file__), '_scripts')
    server = ScriptServer(scriptdir)
    config = {
        'do_smooth': do_smooth,
        'dva': cls.default_vertex_attributes,
        'dea': cls.default_edge_attributes,
        'dfa': cls.default_face_attributes
    }
    config.update(kwargs)
    res = server.mesh_from_points(
        points=points,
        config=config
    )
    mesh = cls.from_data(res['data'])
    return mesh
