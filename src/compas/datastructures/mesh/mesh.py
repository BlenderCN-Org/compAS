from __future__ import print_function

import os
import json
import ast

from ast import literal_eval as _eval

from copy import deepcopy

from compas.files.obj import OBJ

from compas.geometry import length_vector
from compas.geometry import distance_point_point
from compas.geometry import cross_vectors
from compas.geometry import normal_polygon
from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon
from compas.geometry import area_polygon

from compas.geometry.elements import Line

from compas.utilities import geometric_key

from compas.datastructures.network.algorithms import network_bfs
from compas.datastructures.network.algorithms import network_bfs2


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


# @todo: implement faces as lists!


class Mesh(object):
    """Class representing a mesh.

    The datastructure of the mesh is implemented as a half-edge.

    Parameters:
        vertices (:obj:`list` of :obj:`dict`) : Optional. A sequence of vertices to add to the mesh.
            Each vertex should be a dictionary of vertex attributes.
        faces (:obj:`list` of :obj:`list`) : Optional. A sequence of faces to add to the mesh.
            Each face should be a list of vertex keys.
        dva (dict) : Optional. A dictionary of default vertex attributes.
        dfa (dict) : Optional. A dictionary of default face attributes.
        dea (dict) : Optional. A dictionary of default edge attributes.
        kwargs (dict) : The remaining named parameters. These are added to the attributes
            dictionary of the instance.

    Attributes:
        vertex (dict) : The vertex dictionary.
            With every key in the dictionary corresponds a dictionary of attributes.
        face (dict) : The face dictionary.
            With every key in the dictionary corresponds a dictionary of half-edges.
        halfedge (dict) : The half-edge dictionary.
            Every key in the dictionary corresponds to a vertex of the mesh.
            With every key corresponds a dictionary of neighbours pointing to face keys.
        edge (dict) : The edge dictionary.
            Every key in the dictionary corresponds to a vertex.
            With every key corresponds a dictionary of neighbours pointing to attribute dictionaries.
        attributes (dict) : General mesh attributes.
        facedata (Mesh, optional) : A ``Mesh`` object for keeping track of face attributes
            by storing them on dual vertices.

    Examples:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            mesh.plot(vertexsize=0.2)


        .. plot::
            :include-source:

            import compas
            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            mesh.plot(
                vertexsize=0.2,
                vertexlabel={key: key for key in mesh}
            )


        .. plot::
            :include-source:

            import compas
            from compas.datastructures.mesh import Mesh

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            mesh.plot(
                vertexsize=0.2,
                facelabel={fkey: fkey for fkey in mesh.face}
            )


        >>> for key in mesh.vertex:
        ...     print key
        ...

        >>> for key in mesh.vertices():
        ...     print key
        ...

        >>> for key in mesh.vertices_iter():
        ...     print key
        ...

        >>> for index, key in mesh.vertices_enum():
        ...     print index, key
        ...

        >>> for key, attr in mesh.vertices(True):
        ...     print key, attr
        ...

        >>> for key, attr in mesh.vertices_iter(True):
        ...     print key, attr
        ...

        >>> for index, key, attr in mesh.vertices_enum(True):
        ...     print index, key, attr
        ...

    """

    def __init__(self):
        self._max_int_fkey = -1
        self._max_int_key  = -1
        self._plotter      = None
        self.vertex        = {}
        self.face          = {}
        self.halfedge      = {}
        self.edge          = {}
        self.facedata      = {}
        self.attributes    = {
            'name'         : 'Mesh',
            'color.vertex' : (0, 0, 0),
            'color.edge'   : (0, 0, 0),
            'color.face'   : (0, 0, 0),
        }
        self.default_vertex_attributes = {'x': 0, 'y': 0, 'z': 0}
        self.default_face_attributes   = {}
        self.default_edge_attributes   = {}

    def __contains__(self, key):
        """Verify if the mesh contains a specific vertex.

        Parameters:
            key (str) : The identifier ('key') of the vertex.

        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        '0'
        >>> '0' in mesh
        True
        >>> '1' in mesh
        False
        """
        return key in self.vertex

    def __len__(self):
        """Defines the length of the mesh as the number of vertices in the mesh.

        >>> len(mesh) == len(mesh.vertex) == len(mesh.vertex.keys())
        True
        """
        return len(self.vertex)

    def __iter__(self):
        """Defines mesh iteration as iteration over the vertex keys.

        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        >>> mesh.add_vertex()
        >>> for key in mesh: print key
        '0'
        '1'
        """
        return iter(self.vertex)

    def __getitem__(self, key):
        """Defines the behaviour of the mesh when it is treated as a container and
        one of its items is accessed directly. Because of this implementation,
        the mesh will respond by returning the vertex attributes corresponding to
        the requested vertex key.

        >>> mesh = Mesh()
        >>> mesh.add_vertex(x=0, y=0, z=0)
        '0'
        >>> mesh.vertex['0']
        {'x': 0, 'y': 0, 'z': 0}
        >>> mesh['0']
        {'x': 0, 'y': 0, 'z': 0}
        """
        return self.vertex[key]

    def __delitem__(self, key):
        """Defines the behaviour of the mesh when ..."""
        self.delete_vertex(key)

    def __str__(self):
        """Defines the bahaviour of the mesh when it is converted to a string,
        printed, or used by :obj:`format`.

        >>> str(mesh)
        >>> print mesh
        >>> "{}".format(mesh)
        """
        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
mesh summary
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- number of vertices: {0}
- number of faces: {1}
- number of edges: {2}

- vertex degree min: {3}
- vertex degree max: {4}
- face size min: {5}
- face size max: {6}

- is valid: {7}
- is connected: {8}
- is manifold: {9}
- is tri mesh: {10}
- is quad mesh: {11}

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
\n""".format(len(self.vertex),
             len(self.face),
             len(self.edges()),
             (0 if not self.vertex else min(self.vertex_degree(key) for key in self.vertex)),
             (0 if not self.vertex else max(self.vertex_degree(key) for key in self.vertex)),
             (0 if not self.face else min(len(self.face_vertices(fkey)) for fkey in self.face)),
             (0 if not self.face else max(len(self.face_vertices(fkey)) for fkey in self.face)),
             ('True' if self.is_valid() else 'False'),
             ('True' if self.is_connected() else 'False'),
             ('True' if self.is_manifold() else 'False'),
             ('True' if self.is_trimesh() else 'False'),
             ('True' if self.is_quadmesh() else 'False'))

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # descriptors
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    @property
    def data(self):
        """:obj:`dict` : The data representing the mesh.

        By assigning a data dict to this property, the current data of the mesh
        will be replaced by the data in the dict. The data getter and setter should
        always be used in combination with each other. They are also used by the
        Mesh.from_data() class method and the mesh.to_data() instance method.
        """
        data = {'attributes'  : self.attributes,
                'dva'         : self.default_vertex_attributes,
                'dea'         : self.default_edge_attributes,
                'dfa'         : self.default_face_attributes,
                'vertex'      : {},
                'edge'        : {},
                'halfedge'    : {},
                'face'        : {},
                'facedata'    : {},
                'max_int_key' : self._max_int_key,
                'max_int_fkey': self._max_int_fkey, }

        key_rkey = {}

        for key in self.vertex:
            rkey = repr(key)
            key_rkey[key] = rkey
            data['vertex'][rkey] = self.vertex[key]
            data['edge'][rkey] = {}
            data['halfedge'][rkey] = {}

        for u in self.edge:
            ru = key_rkey[u]
            for v in self.edge[u]:
                rv = key_rkey[v]
                data['edge'][ru][rv] = self.edge[u][v]

        for u in self.halfedge:
            ru = key_rkey[u]
            for v in self.halfedge[u]:
                rv = key_rkey[v]
                data['halfedge'][ru][rv] = self.halfedge[u][v]

        for fkey in self.face:
            rfkey = repr(fkey)
            data['face'][rfkey] = self.face[fkey]

        for fkey in self.facedata:
            rfkey = repr(fkey)
            data['facedata'][rfkey] = self.facedata[fkey]

        return data

    @data.setter
    def data(self, data):
        attributes   = data.get('attributes')
        dva          = data.get('dva')
        dfa          = data.get('dfa')
        dea          = data.get('dea')
        vertex       = data.get('vertex')
        halfedge     = data.get('halfedge')
        face         = data.get('face')
        facedata     = data.get('facedata')
        edge         = data.get('edge')
        max_int_key  = data.get('max_int_key', -1)
        max_int_fkey = data.get('max_int_fkey', -1)

        if not vertex or not halfedge or not face:
            return

        self.clear()

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_face_attributes.update(dfa)
        self.default_edge_attributes.update(dea)

        for rkey, attr in vertex.iteritems():
            key = _eval(rkey)
            self.vertex[key] = self.default_vertex_attributes.copy()
            if attr:
                self.vertex[key].update(attr)
            self.edge[key] = {}
            self.halfedge[key] = {}

        for ru, nbrs in edge.iteritems():
            nbrs = nbrs or {}
            u = _eval(ru)
            for rv, attr in nbrs.iteritems():
                v = _eval(rv)
                self.edge[u][v] = self.default_edge_attributes.copy()
                if attr:
                    self.edge[u][v].update(attr)

        for rkey, nbrs in halfedge.iteritems():
            if not nbrs:
                nbrs = {}
            key = _eval(rkey)
            for rnbr, fkey in nbrs.iteritems():
                nbr = _eval(rnbr)
                self.halfedge[key][nbr] = fkey

        for rfkey, vertices in face.iteritems():
            fkey = _eval(rfkey)
            self.face[fkey] = vertices

        # make a separate facedata key dict?
        for rfkey, attr in facedata.iteritems():
            fkey = _eval(rfkey)
            self.facedata[fkey] = attr

        self._max_int_key = max_int_key
        self._max_int_fkey = max_int_fkey

    @property
    def name(self):
        """:obj:`str` : The name of the mesh.

        Any value of appropriate type assigned to this property will be stored in
        the instance's attribute dict.
        """
        return self.attributes.get('name', None)

    @name.setter
    def name(self, value):
        self.attributes['name'] = value

    @property
    def plotter(self):
        if not self._plotter:
            from compas.datastructures.mesh.plotter import MeshPlotter2D
            self._plotter = MeshPlotter2D(self)
        return self._plotter

    @property
    def xyz(self):
        """:obj:`list` : The `xyz` coordinates of the vertices of the mesh."""
        return [(a['x'], a['y'], a['z']) for k, a in self.vertices_iter(True)]

    @property
    def xy(self):
        """:obj:`list` : The `xy` coordinates of the vertices of the mesh."""
        return [(a['x'], a['y']) for k, a in self.vertices_iter(True)]

    @property
    def x(self):
        """:obj:`list` : The `x` coordinates of the vertices of the mesh."""
        return [a['x'] for k, a in self.vertices_iter(True)]

    @property
    def y(self):
        """:obj:`list` : The `y` coordinates of the vertices of the mesh."""
        return [a['y'] for k, a in self.vertices_iter(True)]

    @property
    def z(self):
        """:obj:`list` : The `z` coordinates of the vertices of the mesh."""
        return [a['z'] for k, a in self.vertices_iter(True)]

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # helpers
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def key_index(self):
        """Returns a *key-to-index* map.

        This function is primarily intended for working with arrays.
        For example::

            >>> import compas
            >>> import numpy as np
            >>> mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            >>> xyz = np.array(mesh.vertex_coordinates(xyz='xyz'), dtype=float)
            >>> k2i = mesh.key_index()

            # do stuff to the coordinates
            # for example, apply smoothing
            # then update the vertex coordinates in the data structure

            >>> for key in mesh:
            ...     index = k2i[key]
            ...     mesh.vertex[key]['x'] = xyz[index, 0]
            ...     mesh.vertex[key]['y'] = xyz[index, 1]
            ...     mesh.vertex[key]['z'] = xyz[index, 2]

        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        '0'
        >>> k_i = mesh.key_index()
        >>> k_i['0']
        0
        """
        return dict((k, i) for i, k in self.vertices_enum())

    def index_key(self):
        """Returns an *index-to-key* map.

        This function is primarily intended for working with arrays.
        For example::

            >>>

        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        '0'
        >>> i_k = mesh.index_key()
        >>> i_k[0]
        '0'
        """
        return dict(self.vertices_enum())

    def copy(self):
        cls  = type(self)
        data = deepcopy(self.data)
        mesh = cls.from_data(data)
        return mesh

    def clear(self):
        del self.vertex
        del self.edge
        del self.halfedge
        del self.face
        del self.facedata
        self.vertex     = {}
        self.halfedge   = {}
        self.face       = {}
        self.facedata   = {}
        self.edge       = {}
        self._max_int_key = -1
        self._max_int_fkey = -1

    def get_any_vertex(self):
        return next(self.vertices_iter())

    def get_any_face(self):
        return next(self.faces_iter())

    def get_any_face_vertex(self, fkey):
        return self.face_vertices(fkey)[0]

    def vertex_color(self, key, qualifier=None):
        if qualifier:
            if self.vertex[key][qualifier]:
                return self.attributes.get('color.vertex:{0}'.format(qualifier))
        return self.attributes['color.vertex']

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # constructors
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    @classmethod
    def from_data(cls, data, **kwargs):
        """Construct a mesh from actual mesh data.

        This function should be used in combination with the data obtained from
        ``mesh.data``.

        Parameters:
            data (dict): The data dictionary.
            kwargs (dict) : Remaining named parameters. Default is an empty :obj:`dict`.

        Returns:
            Mesh: A ``Mesh`` of class ``cls``.

        >>> data = m1.to_data()
        >>> m2 = Mesh.from_data(data)

        """
        mesh = cls()
        mesh.attributes.update(kwargs)
        mesh.data = data
        return mesh

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces, **kwargs):
        """Initialise a mesh from a list of vertices and faces.

        Parameters:
            vertices (list) : A list of vertices, represented by their XYZ coordinates.
            faces (list) : A list of faces. Each face is a list of indices referencing
                the list of vertex coordinates.
            kwargs (dict) : Remaining named parameters. Default is an empty :obj:`dict`.

        Returns:
            Mesh: A ``Mesh`` of class ``cls``.

        >>> vertices = []
        >>> faces = []
        >>> mesh = Mesh.from_vertices_and_faces(vertices, faces)

        """
        mesh = cls()
        mesh.attributes.update(kwargs)
        for x, y, z in vertices:
            mesh.add_vertex(x=x, y=y, z=z)
        for face in faces:
            mesh.add_face(face)
        return mesh

    @classmethod
    def from_lines(cls, lines, boundary_face=False, precision='3f'):
        """"""
        from compas.datastructures.network.algorithms.duality import _sort_neighbours
        from compas.datastructures.network.algorithms.duality import _find_first_neighbour
        from compas.datastructures.network.algorithms.duality import _find_edge_face

        mesh = cls()
        edges   = []
        vertex  = {}
        for line in lines:
            sp = line[0]
            ep = line[1]
            a  = geometric_key(sp, precision)
            b  = geometric_key(ep, precision)
            vertex[a] = sp
            vertex[b] = ep
            edges.append((a, b))
        key_index = dict((k, i) for i, k in enumerate(iter(vertex)))
        for key, xyz in vertex.iteritems():
            i = key_index[key]
            mesh.add_vertex(i, x=xyz[0], y=xyz[1], z=xyz[2])
        edges_uv = []
        for u, v in edges:
            i = key_index[u]
            j = key_index[v]
            edges_uv.append((i, j))
        # the clear commands below are from the network equivalent. Needed?
        # network.clear_facedict()
        # network.clear_halfedgedict()
        mesh.halfedge = dict((key, {}) for key in mesh.vertex)
        for u, v in edges_uv:
            mesh.halfedge[u][v] = None
            mesh.halfedge[v][u] = None
        _sort_neighbours(mesh)

        u = sorted(mesh.vertices_iter(True), key=lambda x: (x[1]['y'], x[1]['x']))[0][0]
        v = _find_first_neighbour(u, mesh)
        key_boundary_face = _find_edge_face(u, v, mesh)
        print(key_boundary_face)
        for u, v in mesh.edges_iter():
            if mesh.halfedge[u][v] is None:
                _find_edge_face(u, v, mesh)
            if mesh.halfedge[v][u] is None:
                _find_edge_face(v, u, mesh)

        if not boundary_face:
            mesh.delete_face(key_boundary_face)
        return mesh

    @classmethod
    def from_obj(cls, filepath, **kwargs):
        """Initialise a mesh from the data described in an obj file.

        Parameters:
            filepath (str): The path to the obj file.
            kwargs (dict) : Remaining named parameters. Default is an empty :obj:`dict`.

        Returns:
            Mesh: A ``Mesh`` of class ``cls``.

        >>> mesh = Mesh.from_obj('path/to/file.obj')

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

    @classmethod
    def from_dxf(cls, filepath, **kwargs):
        raise NotImplementedError

    @classmethod
    def from_stl(cls, filepath, **kwargs):
        raise NotImplementedError

    @classmethod
    def from_json(cls, filepath, **kwargs):
        data = None
        with open(filepath, 'rb') as fp:
            data = json.load(fp)
        mesh = cls.from_data(data)
        mesh.attributes.update(kwargs)
        return mesh

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # conversion methods
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def to_data(self):
        """Return the data dict that represents the mesh, and from which it can
        be reconstructed."""
        return self.data

    def to_obj(self, filepath):
        """Write the mesh to an OBJ file.

        Parameters:
            filepath (str): Full path of the file to write.

        Notes:
            Use the framework ``OBJ`` functionality for this. How to write vertices
            and faces to an ``OBJ`` is not necessarily something a mesh knows how
            to do.
        """
        key_index = dict((key, index) for index, key in self.vertices_enum())
        with open(filepath, 'wb+') as fh:
            for key, attr in self.vertices_iter(True):
                fh.write('v {0[x]:.3f} {0[y]:.3f} {0[z]:.3f}\n'.format(attr))
            for fkey in self.face:
                vertices = self.face_vertices(fkey, ordered=True)
                vertices = [key_index[key] + 1 for key in vertices]
                ixs = ['f']
                for vkey in vertices:
                    ixs.append('{0}'.format(vkey))
                fh.write(' '.join(ixs) + '\n')

    def to_json(self, filepath):
        """Serialize the mesh data to a JSON file.

        Parameters:
            filepath (str): Path to the file to write.

        Returns:
            None
        """
        data = self.to_data()
        with open(filepath, 'wb+') as fh:
            json.dump(data, fh)

    def to_lines(self, axes='xyz'):
        return [(self.vertex_coordinates(u, axes), self.vertex_coordinates(v, axes))
                for u, v in self.edges_iter()]

    def to_points(self, axes='xyz'):
        return [self.vertex_coordinates(key, axes) for key in self]

    def to_vertices_and_faces(self):
        """Return the vertices and faces of a mesh.

        Returns:
            (list, list): A tuple with a list of vertices, represented by their
                XYZ coordinates, and a list of faces. Each face is a list of
                indices referencing the list of vertex coordinates.
        """
        vertices = [self.vertex_coordinates(key) for key in self.vertex]
        faces = [self.face_vertices(fkey, ordered=True) for fkey in self.face]
        return vertices, faces

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # modify the mesh
    # ---------------
    # add / remove / ...
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def _get_vertexkey(self, key):
        if key is None:
            key = self._max_int_key = self._max_int_key + 1
        else:
            # try:
            #     int(key)
            # except (ValueError, TypeError):
            #     pass
            # else:
            if int(key) > self._max_int_key:
                self._max_int_key = int(key)
        return key

    def _get_facekey(self, fkey):
        if fkey is None:
            fkey = self._max_int_fkey = self._max_int_fkey + 1
        else:
            # try:
            #     int(fkey)
            # except (ValueError, TypeError):
            #     pass
            # else:
            if int(fkey) > self._max_int_fkey:
                self._max_int_fkey = int(fkey)
        return fkey

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a single vertex.

        Note:
            If no key is provided for the vertex, one is generated
            automatically. An automatically generated key increments the highest
            key in use by 1::

                key = int(sorted(self.vertex.keys())[-1]) + 1

        Parameters:
            key (int): An identifier for the vertex. Defaults to None. The key
                is converted to a string before it is used.
            attr_dict (dict): Vertex attributes, defaults to ``None``.
            **attr: Other named vertex attributes, defaults to an empty :obj:`dict`.

        Returns:
            str: The key of the vertex.

        Examples:
            >>> mesh = Mesh()
            >>> mesh.add_vertex()
            '0'
            >>> mesh.add_vertex(x=0, y=0, z=0)
            '1'
            >>> mesh.add_vertex(key=2)
            '2'
            >>> mesh.add_vertex(key=0, x=1)
            '0'
        """
        attr = self.default_vertex_attributes.copy()
        if attr_dict:
            attr.update(attr_dict)
        attr.update(kwattr)
        key = self._get_vertexkey(key)
        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
        self.vertex[key].update(attr)
        return key

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a topological relation between vertices in the form of a face.
        A dictionary key for the face will be generated automatically, based on
        the keys of its vertices.

        Note:
            All faces are closed. The closing link is implied and, therefore,
            the last vertex in the list should be different from the first.

        Note:
            Building a face_adjacency list is slow, if we can't rely on the fact
            that all faces have the same cycle directions. Therefore, it is
            worth considering to ensure unified cycle directions upon addition
            of a new face.

        Parameters:
            vertices (list): A list of vertex keys.

        Returns:
            str: The key of the face.
        """
        attr = self.default_face_attributes.copy()
        if attr_dict is None:
            attr_dict = kwattr
        else:
            attr_dict.update(kwattr)
        attr.update(attr_dict)
        # check if the face is valid
        if vertices[0] == vertices[-1]:
            del vertices[-1]
        if vertices[-2] == vertices[-1]:
            del vertices[-1]
        if len(vertices) < 3:
            return
        # get the correct face key
        fkey = self._get_facekey(fkey)
        self.face[fkey] = {}
        for i in range(-1, len(vertices) - 1):
            u = vertices[i]
            v = vertices[i + 1]
            self.face[fkey][u] = v
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None
        return fkey

    def add_vertices(self):
        raise NotImplementedError

    # this should be delete_vertex
    def remove_vertex(self, key):
        nbrs = self.vertex_neighbours(key)
        for nbr in nbrs:
            fkey = self.halfedge[key][nbr]
            if fkey is None:
                continue
            for u, v in self.face[fkey].items():
                self.halfedge[u][v] = None
            del self.face[fkey]
        for nbr in nbrs:
            del self.halfedge[nbr][key]
        for nbr in nbrs:
            for n in self.vertex_neighbours(nbr):
                if self.halfedge[nbr][n] is None and self.halfedge[n][nbr] is None:
                    del self.halfedge[nbr][n]
                    del self.halfedge[n][nbr]
        del self.halfedge[key]
        del self.vertex[key]

    def delete_vertex(self, key):
        raise NotImplementedError

    def insert_vertex(self, fkey, key=None, xyz=None):
        """Insert a vertex in the specified face.

        Parameters:
            fkey (str): The key of the face in which the vertex should be inserted.

        Returns:
            str: The keys of the newly created faces.

        Raises:
            ValueError: If the face does not exist.
        """
        fkeys = []
        if not xyz:
            x, y, z = self.face_center(fkey)
        else:
            x, y, z = xyz
        w = self.add_vertex(key=key, x=x, y=y, z=z)
        for u, v in self.face[fkey].iteritems():
            fkeys.append(self.add_face([u, v, w]))
        del self.face[fkey]
        return fkeys

    def add_faces(self):
        raise NotImplementedError

    def delete_face(self, fkey):
        for u, v in self.face[fkey].items():
            self.halfedge[u][v] = None
            if self.halfedge[v][u] is None:
                del self.halfedge[u][v]
                del self.halfedge[v][u]
        del self.face[fkey]

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # attributes
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_vertex_attributes.update(attr_dict)
        for key in self.vertex:
            attr = attr_dict.copy()
            attr.update(self.vertex[key])
            self.vertex[key] = attr

    def set_vertex_attribute(self, key, name, value):
        self.vertex[key][name] = value

    def set_vertex_attributes(self, key, attr_dict=None, **kwattr):
        attr_dict = attr_dict or {}
        attr_dict.update(kwattr)
        self.vertex[key].update(attr_dict)

    def set_vertices_attribute(self, name, value, keys=None):
        if not keys:
            for key, attr in self.vertices_iter(True):
                attr[name] = value
        else:
            for key in keys:
                self.vertex[key][name] = value

    def set_vertices_attributes(self, keys=None, attr_dict=None, **kwattr):
        attr_dict = attr_dict or {}
        attr_dict.update(kwattr)
        if not keys:
            for key, attr in self.vertices_iter(True):
                attr.update(attr_dict)
        else:
            for key in keys:
                self.vertex[key].update(attr_dict)

    def get_vertex_attribute(self, key, name, default=None):
        return self.vertex[key].get(name, default)

    def get_vertex_attributes(self, key, names, defaults=None):
        if not defaults:
            defaults = [None] * len(names)
        return [self.vertex[key].get(name, default) for name, default in zip(names, defaults)]

    def get_vertices_attribute(self, name, default=None, keys=None):
        if not keys:
            return [attr.get(name, default) for key, attr in self.vertices_iter(True)]
        return [self.vertex[key].get(name, default) for key in keys]

    def get_vertices_attributes(self, names, defaults=None, keys=None):
        if not defaults:
            defaults = [None] * len(names)
        temp = zip(names, defaults)
        if not keys:
            return [[attr.get(name, default) for name, default in temp] for key, attr in self.vertices_iter(True)]
        return [[self.vertex[key].get(name, default) for name, default in temp] for key in keys]

    # --------------------------------------------------------------------------
    # attributes: face
    # --------------------------------------------------------------------------

    def update_default_face_attributes(self, attr_dict=None, **kwargs):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwargs)
        self.default_face_attributes.update(attr_dict)
        for fkey in self.face:
            attr = attr_dict.copy()
            attr.update(self.facedata[fkey])
            self.facedata[fkey] = attr

    def set_face_attribute(self, fkey, name, value):
        if fkey not in self.facedata:
            self.facedata[fkey] = self.default_face_attributes.copy()
        self.facedata[fkey][name] = value

    def set_face_attributes(self, fkey, attr_dict=None, **kwattr):
        attr_dict = attr_dict or {}
        attr_dict.update(kwattr)
        if fkey not in self.facedata:
            self.facedata[fkey] = self.default_face_attributes.copy()
        self.facedata[fkey].update(attr_dict)

    def set_faces_attribute(self, name, value, fkeys=None):
        if not fkeys:
            for fkey, attr in self.faces_iter():
                attr[name] = value
        else:
            for fkey in fkeys:
                if fkey not in self.facedata:
                    self.facedata[fkey] = self.default_face_attributes.copy()
                self.facedata[fkey][name] = value

    def set_faces_attributes(self, fkeys=None, attr_dict=None, **kwattr):
        attr_dict = attr_dict or {}
        attr_dict.update(kwattr)
        if not fkeys:
            for fkey, attr in self.faces_iter():
                attr.update(attr_dict)
        else:
            for fkey in fkeys:
                if fkey not in self.facedata:
                    self.facedata[fkey] = self.default_face_attributes.copy()
                self.facedata[fkey].update(attr_dict)

    def get_face_attribute(self, fkey, name, default=None):
        if not self.facedata:
            return default
        if fkey not in self.facedata:
            return default
        return self.facedata[fkey].get(name, default)

    def get_face_attributes(self, fkey, names, defaults=None):
        if not defaults:
            defaults = [None] * len(names)
        if not self.facedata:
            return defaults
        if fkey not in self.facedata:
            return defaults
        return [self.facedata[fkey].get(name, default) for name, default in zip(names, defaults)]

    def get_faces_attribute(self, name, default=None, fkeys=None):
        if not fkeys:
            if not self.facedata:
                return [default for fkey in self.face]
            return [self.get_face_attribute(fkey, name, default) for fkey in self.face]
        if not self.facedata:
            return [default for fkey in fkeys]
        return [self.get_face_attribute(fkey, name, default) for fkey in fkeys]

    def get_faces_attributes(self, names, defaults=None, fkeys=None):
        if not defaults:
            defaults = [None] * len(names)
        temp = zip(names, defaults)
        if not fkeys:
            if not self.facedata:
                return [[default for name, default in temp] for fkey in self.face]
            return [[self.get_face_attribute(fkey, name, default) for name, default in temp] for fkey in self.face]
        if not self.facedata:
            return [[default for name, default in temp] for fkey in fkeys]
        return [[self.get_face_attribute(fkey, name, default) for name, default in temp] for fkey in fkeys]

    # ..........................................................................
    # edge attributes
    # ---------------
    # - edges are virtual
    # - none of the topological operations/algorithms care about/take into account edges
    # - the only purpose of the edge dict is to store edge data
    # - unused edges can be culled
    # ..........................................................................

    def update_default_edge_attributes(self, attr_dict=None, **kwargs):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwargs)
        self.default_edge_attributes.update(attr_dict)
        for u, v in self.edges():
            attr = attr_dict.copy()
            attr.update(self.edge[u][v])
            self.edge[u][v] = attr

    def set_edge_attribute(self, u, v, name, value):
        if u in self.halfedge and v in self.halfedge[u]:
            if u not in self.edge:
                self.edge[u] = {}
            if v not in self.edge[u]:
                self.edge[u][v] = {}
            self.edge[u][v][name] = value

    def set_edge_attributes(self, u, v, attr_dict=None, **kwattr):
        attr_dict = attr_dict or kwattr
        attr_dict.update(kwattr)
        if u in self.halfedge and v in self.halfedge[u]:
            if u not in self.edge:
                self.edge[u] = {}
            if v not in self.edge[u]:
                self.edge[u][v] = {}
            self.edge[u][v].update(attr_dict)

    def set_edges_attribute(self, name, value, keys=None):
        if not keys:
            for u, v, attr in self.edges_iter(True):
                attr[name] = value
        else:
            for u, v in keys:
                self.set_edge_attribute(u, v, name, value)

    def set_edges_attributes(self, keys=None, attr_dict=None, **kwattr):
        attr_dict = attr_dict or {}
        attr_dict.update(kwattr)
        if not keys:
            for u, v, attr in self.edges_iter(True):
                attr.update(attr_dict)
        else:
            for u, v in keys:
                self.edge_attributes(u, v, attr_dict=attr_dict)

    def get_edge_attribute(self, u, v, name, default=None):
        if u in self.edge:
            if v in self.edge[u]:
                return self.edge[u][v].get(name, default)
        if v in self.edge:
            if u in self.edge[v]:
                return self.edge[v][u].get(name, default)
        return default

    def get_edge_attributes(self, u, v, names, defaults=None):
        if not defaults:
            defaults = [None] * len(names)
        if v in self.edge[u]:
            return [self.edge[u][v].get(name, default) for name, default in zip(names, defaults)]
        return [self.edge[v][u].get(name, default) for name, default in zip(names, defaults)]

    def get_edges_attribute(self, name, default=None, keys=None):
        if not keys:
            return [attr.get(name, default) for u, v, attr in self.edges_iter(True)]
        return [self.edge[u][v].get(name, default) for u, v in keys]

    def get_edges_attributes(self, names, defaults=None, keys=None):
        if not defaults:
            defaults = [None] * len(names)
        temp = zip(names, defaults)
        if not keys:
            return [[attr.get(name, default) for name, default in temp] for u, v, attr in self.edges_iter(True)]
        return [[self.edge[u][v].get(name, default) for name, default in temp] for u, v in keys]

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # culling
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def cull_unused_vertices(self):
        for u in self.vertices():
            if u not in self.halfedge:
                del self.vertex[u]
            else:
                if not self.halfedge[u]:
                    del self.vertex[u]
                    del self.halfedge[u]

    def cull_unused_edges(self):
        for u, v in self.edges():
            if u not in self.halfedge:
                del self.edge[u][v]
            if v not in self.halfedge[u]:
                del self.edge[u][v]
            if len(self.edge[u]) == 0:
                del self.edge[u]

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # accessors
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def vertices(self, data=False):
        """Get a list of vertex keys. If `data` is True, get a list of key, data
        pairs.

        Parameters:
            data (bool): Return key, data pairs, defaults to False.

        Returns:
            list: A list of vertex keys, if data is False.
            list: A list of key, data pairs, if data is True.
        """
        if data:
            return self.vertex.items()
        return self.vertex.keys()

    def vertices_iter(self, data=False):
        """Get an iterator over the list of vertex keys. If `data` is True, get
        an iterator over key, data pairs.

        Parameters:
            data (bool): Return key, data pairs, defaults to False.

        Returns:
            iter: An iterator of vertex keys, if data is False.
            iter: An iterator of key, data pairs, if data is True.
        """
        if data:
            return self.vertex.iteritems()
        return self.vertex.iterkeys()

    def vertices_enum(self, data=False):
        """Get an enumeration of the vertex keys.

        Parameters:
            data (bool) : If ``True``, return the vertex attributes as part of
                the enumeration. Default is ``False``.

        Returns:
            iter : The enumerating iterator of vertex keys.

        >>> for index, key in mesh.vertices_enum():
        ...     print index, key
        ...

        >>> for index, key, attr in mesh.vertices_enum(data=True):
        ...     print index, key, attr
        ...

        """
        return enumerate(self.vertices_iter(data))

    def faces(self):
        """"""
        return self.face.keys()

    def faces_iter(self):
        """"""
        return self.face.iterkeys()

    def faces_enum(self):
        """"""
        return enumerate(self.faces_iter())

    # ..........................................................................
    # edge lists and iterators
    # ..........................................................................

    def edges(self, data=False):
        """"""
        return list(self.edges_iter(data))

    def edges_iter(self, data=False):
        """"""
        seen = set()
        for u in self.halfedge:
            for v in self.halfedge[u]:
                if (u, v) not in seen and (v, u) not in seen:
                    seen.add((u, v))
                    seen.add((v, u))
                    if u in self.edge and v in self.edge[u]:
                        if data:
                            yield u, v, self.edge[u][v]
                        else:
                            yield u, v
                    elif v in self.edge and u in self.edge[v]:
                        if data:
                            yield v, u, self.edge[v][u]
                        else:
                            yield v, u
                    else:
                        attr = {}
                        attr.update(self.default_edge_attributes)
                        if u not in self.edge:
                            self.edge[u] = {}
                        self.edge[u][v] = attr
                        if data:
                            yield u, v, attr
                        else:
                            yield u, v

    def edges_enum(self, data=False):
        """"""
        return enumerate(self.edges_iter(data))

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # properties
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def is_valid(self):
        # a mesh is valid if the following conditions are true
        # - halfedges don't point at non-existing faces
        # - all vertices are in the halfedge dict
        # - there are no None-None halfedges
        # - all faces have corresponding halfedge entries
        for key in self.vertex:
            if key not in self.halfedge:
                return False
        for u in self.halfedge:
            if u not in self.vertex:
                return False
            for v in self.halfedge[u]:
                if v not in self.vertex:
                    return False
                if self.halfedge[u][v] is None and self.halfedge[v][u] is None:
                    return False
                fkey = self.halfedge[u][v]
                if fkey:
                    if fkey not in self.face:
                        return False
        for fkey in self.face:
            for u, v in self.face[fkey].iteritems():
                if u not in self.vertex:
                    return False
                if v not in self.vertex:
                    return False
                if u not in self.halfedge:
                    return False
                if v not in self.halfedge[u]:
                    return False
                if fkey != self.halfedge[u][v]:
                    return False
        return True

    def is_regular(self):
        """Return True if all faces have the same number of edges, and all vertices
        have the same degree (i.e. have the same valence: are incident to the same
        number of edges).

        Note:
            Not sure if the second condition makes sense.
            Example of a regular mesh?
        """
        if not self.vertex or not self.face:
            return False
        viter = self.vertices_iter()
        vkey = viter.next()
        degree = self.vertex_degree(vkey)
        for vkey in viter:
            if self.vertex_degree(vkey) != degree:
                return False
        fiter = self.faces_iter()
        fkey = fiter.next()
        vcount = len(self.face_vertices(fkey))
        for fkey in fiter:
            vertices = self.face_vertices(fkey)
            if len(vertices) != vcount:
                return False
        return True

    def is_connected(self):
        """Return True if for every two vertices a path exists connecting them."""
        if not self.vertex:
            return False
        root = self.vertices_iter().next()
        nodes = network_bfs2(self.halfedge, root)
        return len(nodes) == len(self.vertex)

    def is_manifold(self):
        """Return True if each edge is incident to only one or two faces, and the
        faces incident to a vertex form a closed or an open fan.

        Note:
            The first condition seems to be fullfilled by construction?!
        """
        if not self.vertex:
            return False
        for key in self.vertex:
            nbrs = self.vertex_neighbours(key, ordered=True)
            if not nbrs:
                return False
            if self.halfedge[nbrs[0]][key] is None:
                for nbr in nbrs[1:-1]:
                    if self.halfedge[key][nbr] is None:
                        return False
                if self.halfedge[key][nbrs[-1]] is not None:
                    return False
            else:
                for nbr in nbrs[1:]:
                    if self.halfedge[key][nbr] is None:
                        return False
        return True

    def is_orientable(self):
        """A manifold mesh is orientable if any two adjacent faces have compatible
        orientation (i.e. if the faces have a unified cycle direction)."""
        raise NotImplementedError

    # as in "does the mesh have a boundary?"
    # and no holes?
    def is_closed(self):
        raise NotImplementedError

    # as in "does the mesh have planar faces?"
    def is_planar(self):
        raise NotImplementedError

    def is_trimesh(self):
        if not self.face:
            return False
        for fkey in self.face:
            if len(self.face[fkey]) != 3:
                return False
        return True

    def is_quadmesh(self):
        if not self.face:
            return False
        for fkey in self.face:
            if len(self.face[fkey]) != 4:
                return False
        return True

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # vertex topology
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def vertex_adjacency(self, ordered=False):
        if not ordered:
            # return dict((key, set(self.halfedge[key])) for key in self.vertex)
            return self.halfedge
        raise NotImplementedError

    def vertex_neighbours(self, key, ordered=False):
        if not ordered:
            return self.halfedge[key].keys()
        temp = self.halfedge[key].keys()
        if len(temp) < 1:
            return []
        start = temp[0]
        for nbr in temp:
            if self.halfedge[key][nbr] is None:
                start = nbr
                break
        fkey = self.halfedge[start][key]
        nbrs = []
        nbrs.append(start)
        count = 1000
        while count:
            count -= 1
            d = self.face[fkey][key]
            fkey = self.halfedge[d][key]
            if d == nbrs[0]:
                break
            nbrs.append(d)
            if fkey is None:
                break
        return nbrs

    def vertex_neighbourhood(self, key, ring=1):
        raise NotImplementedError

    def vertex_cycle(self, key):
        nbrs = self.vertex_neighbours(key, ordered=True)
        return dict((nbrs[i], nbrs[i + 1]) for i in range(-1, len(nbrs) - 1))

    def vertex_descendant(self, u, v):
        """Return the descendant vertex of halfedge ``uv``.

        Parameters:
            u (str) : The *from* vertex.
            v (str) : The *to* vertex.

        Returns:
            str : The key of the descendant.
            None : If ``uv`` has no descendant.

        Raises:
            KeyError : If the halfedge is not part of the mesh.
            MeshError : If something else went wrong.
        """
        fkey = self.halfedge[u][v]
        if fkey is not None:
            # the face is on the inside
            return self.face[fkey][v]
        # the face is on the outside
        for nbr in self.halfedge[v]:
            if nbr != u:
                if self.halfedge[v][nbr] is None:
                    return nbr
        # raise a ``MeshError`` here.
        return None

    def vertex_ancestor(self, u, v):
        """Return the key of the vertex before u in the face that contains uv."""
        fkey = self.halfedge[v][u]
        if fkey is not None:
            return self.face[fkey][u]
        for nbr in self.halfedge[u]:
            if nbr != v:
                if self.halfedge[u][nbr] is None:
                    return nbr
        return None

    def vertex_faces(self, key, ordered=False):
        if not ordered:
            return self.halfedge[key].values()
        nbrs = self.vertex_neighbours(key, ordered=True)
        return [self.halfedge[key][n] for n in nbrs]

    def vertex_degree(self, key):
        return len(self.halfedge[key])

    def is_vertex_leaf(self, key):
        return not self.vertex_degree(key) > 1

    def is_vertex_orphan(self, key):
        return not self.vertex_degree(key) > 0

    def is_vertex_connected(self, key):
        return self.vertex_degree(key) > 0

    def is_vertex_on_boundary(self, key):
        for nbr in self.halfedge[key]:
            if self.halfedge[key][nbr] is None:
                return True
        return False

    def is_vertex_extraordinary(self, key, mtype=None):
        raise NotImplementedError

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # face topology
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def face_vertices(self, fkey, ordered=False):
        if not ordered:
            return self.face[fkey].keys()
        start = iter(self.face[fkey]).next()
        v = self.face[fkey][start]
        vertices = [start]
        count = 1000
        while count:
            if v == start:
                break
            vertices.append(v)
            v = self.face[fkey][v]
            count -= 1
        return vertices

    def face_neighbours(self, fkey, ordered=False):
        neighbours = []
        if not ordered:
            for u, v in self.face[fkey].iteritems():
                neighbours.append(self.halfedge[v][u])
            return neighbours
        vertices = self.face_vertices(fkey, ordered=True)
        for i in range(-1, len(vertices) - 1):
            u = vertices[i]
            v = vertices[i + 1]
            neighbours.append(self.halfedge[v][u])
        return neighbours

    def face_vertex_neighbours(self, fkey):
        seen = set()
        faces = []
        for u in self.face[fkey]:
            for test in self.halfedge[u].values():
                if fkey == test:
                    continue
                if test not in seen:
                    seen.add(test)
                    faces.append(test)
        return faces

    def face_neighbourhood(self, fkey):
        enbrs = self.face_neighbours(fkey)
        vnbrs = self.face_vertex_neighbours(fkey)
        return set(enbrs + vnbrs)

    def face_adjacency(self):
        # this function does not actually use any of the topological information
        # provided by the halfedges
        # it is used for unifying face cycles
        # so the premise is that halfedge data is not valid/reliable
        try:
            from scipy.spatial import cKDTree
        except ImportError:
            have_scipy = False
        else:
            have_scipy = True
        fkey_index = dict((fkey, index) for index, fkey in self.faces_enum())
        index_fkey = dict(self.faces_enum())
        points = [self.face_centroid(fkey) for fkey in self.faces_iter()]
        tree = cKDTree(points)
        _, closest = tree.query(points, k=10, n_jobs=-1)
        adjacency = {}
        for fkey in self.face:
            nbrs  = []
            index = fkey_index[fkey]
            # point = points[index]
            # _, nnbrs = tree.query(point, k=10, n_jobs=-1)
            nnbrs = closest[index]
            found = set()
            for u, v in self.face[fkey].iteritems():
                for index in nnbrs:
                    nbr = index_fkey[index]
                    if nbr == fkey:
                        continue
                    if nbr in found:
                        continue
                    if v in self.face[nbr] and u == self.face[nbr][v]:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break
                    if u in self.face[nbr] and v == self.face[nbr][u]:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break
            adjacency[fkey] = nbrs
        return adjacency

    def face_tree(self, root, algo=network_bfs):
        return algo(self.face_adjacency(), root)

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # (half)edge topology
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def has_edge(self, u, v, strict=False):
        return v in self.halfedge[u] and u in self.halfedge[v]

    def is_edge_naked(self, u, v):
        return (self.halfedge[u][v] is None or self.halfedge[v][u] is None)

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # geometry
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def vertex_area(self, key, length=length_vector, cross=cross_vectors):
        a  = 0
        p0 = self.vertex_coordinates(key)
        for nbr in self.halfedge[key]:
            p1   = self.vertex_coordinates(nbr)
            v01  = [p1[i] - p0[i] for i in range(3)]
            fkey = self.halfedge[key][nbr]
            if fkey is not None:
                p2  = self.face_centroid(fkey)
                v02 = [p2[i] - p0[i] for i in range(3)]
                a  += 0.25 * length(cross(v01, v02))
            fkey = self.halfedge[nbr][key]
            if fkey is not None:
                p3  = self.face_centroid(fkey)
                v03 = [p3[i] - p0[i] for i in range(3)]
                a  += 0.25 * length(cross(v01, v03))
        return a

    def vertex_coordinates(self, key, xyz='xyz'):
        return [self.vertex[key][_] for _ in xyz]

    def vertex_normal(self, key):
        nx = 0
        ny = 0
        nz = 0
        for nbr in self.halfedge[key]:
            fkey = self.halfedge[key][nbr]
            if fkey is None:
                continue
            n   = self.face_normal(fkey, unitized=False)
            nx += n[0]
            ny += n[1]
            nz += n[2]
        a = length_vector(n)
        return nx / a, ny / a, nz / a

    def face_coordinates(self, fkey, ordered=False):
        coords = self.vertex_coordinates
        vertices = self.face_vertices(fkey, ordered=ordered)
        return [coords(key) for key in vertices]

    def face_normal(self, fkey, unitized=True):
        coords = self.vertex_coordinates
        vertices = self.face_vertices(fkey, ordered=True)
        return normal_polygon([coords(key) for key in vertices], unitized=unitized)

    def face_centroid(self, fkey):
        coords = self.vertex_coordinates
        vertices = self.face_vertices(fkey, ordered=True)
        return centroid_points([coords(key) for key in vertices])

    def face_center(self, fkey):
        coords = self.vertex_coordinates
        vertices = self.face_vertices(fkey, ordered=True)
        return center_of_mass_polygon([coords(key) for key in vertices])

    def face_area(self, fkey):
        coords = self.vertex_coordinates
        vertices = self.face_vertices(fkey, ordered=True)
        return area_polygon([coords(key) for key in vertices])

    def edge_length(self, u, v):
        sp = self.vertex_coordinates(u)
        ep = self.vertex_coordinates(v)
        return distance_point_point(sp, ep)

    def edge_midpoint(self, u, v):
        sp = self.vertex_coordinates(u)
        ep = self.vertex_coordinates(v)
        return [0.5 * (sp[i] + ep[i]) for i in range(3)]

    def point_on_edge(self, u, v, t=0.5):
        sp = self.vertex_coordinates(u)
        ep = self.vertex_coordinates(v)
        line = Line(sp, ep)
        line.scale(t)
        x, y, z = line.end
        return x, y, z

    def edge_vector(self, u, v, unitized=False):
        sp  = self.vertex_coordinates(u)
        ep  = self.vertex_coordinates(v)
        vec = [ep[i] - sp[i] for i in range(3)]
        if not unitized:
            return vec
        vec_len = length_vector(vec)
        return [axis / vec_len for axis in vec]

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # boundary
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def vertices_on_boundary(self, ordered=False):
        if not ordered:
            vertices = set()
            for key, nbrs in self.halfedge.iteritems():
                for nbr, face in nbrs.iteritems():
                    if face is None:
                        vertices.add(key)
                        vertices.add(nbr)
            return vertices
        key = sorted(self.vertices_iter(data=True), key=lambda x: (x[1]['y'], x[1]['x']))[0][0]
        vertices = [key]
        start = key
        while 1:
            for nbr, fkey in self.halfedge[key].iteritems():
                if fkey is None:
                    vertices.append(nbr)
                    key = nbr
                    break
            if key == start:
                break
        return vertices

    def faces_on_boundary(self):
        faces = {}
        for key, nbrs in self.halfedge.iteritems():
            for nbr, fkey in nbrs.iteritems():
                if fkey is None:
                    faces[self.halfedge[nbr][key]] = 1
        return faces.keys()

    def edges_on_boundary(self):
        return [(u, v) for u, v in self.edges_iter() if self.is_edge_naked(u, v)]

    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # visualisation
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************
    # **************************************************************************

    def plot(self,
             axes=None,
             vertices_on=True,
             edges_on=True,
             faces_on=True,
             vertexcolor=None,
             edgecolor=None,
             facecolor=None,
             vertexlabel=None,
             facelabel=None,
             vertexsize=None,
             points=None,
             lines=None):
        import matplotlib.pyplot as plt
        from compas.plotters.drawing import create_axes_2d
        local_axes = False
        if not axes:
            axes = create_axes_2d()
            local_axes = True
        plotter = self.plotter
        plotter.vertices_on = vertices_on
        plotter.edges_on = edges_on
        plotter.faces_on = faces_on
        if edgecolor:
            plotter.ecolor = edgecolor
        if vertexcolor:
            plotter.vcolor = vertexcolor
        if vertexlabel:
            plotter.vlabel = vertexlabel
        if vertexsize:
            plotter.vsize = vertexsize
        if facecolor:
            plotter.fcolor = facecolor
        if facelabel:
            plotter.flabel = facelabel
        if points:
            plotter.points = points
        if lines:
            plotter.lines = lines
        plotter.plot(axes)
        if local_axes:
            axes.autoscale()
            plt.show()

    def view(self):
        from compas.datastructures.mesh.viewer import MeshViewer
        viewer = MeshViewer(self)
        viewer.setup()
        viewer.show()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    mesh.update_default_vertex_attributes({'px': 0.0, 'py': 0.0, 'pz': 0.0})
    mesh.update_default_vertex_attributes({'is_fixed': False})

    print(mesh)

    mesh.plot(
        vertexsize=0.2,
        vertexlabel={key: '{0:.1f}'.format(mesh.vertex_area(key)) for key in mesh}
    )
