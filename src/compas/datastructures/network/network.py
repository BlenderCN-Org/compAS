import json
from copy import deepcopy

from compas.files.obj import OBJ

from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import area_polygon
from compas.geometry import subtract_vectors

from compas.utilities import geometric_key

from compas.datastructures.network.algorithms import network_bfs


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


class Network(object):
    """Definition of a network object.

    The ``Network`` class is implemented as a directed edge graph, with optional support
    for face topology and face data if the network is planar.

    Attributes:
        vertex (dict): The vertex dictionary. Each key in the vertex dictionary
            represents a vertex of the network and maps to a dictionary of
            vertex attributes.
        edge (dict of dict): The edge dictionary. Each key in the edge dictionary
            corresponds to a key in the vertex dictionary, and maps to a dictionary
            with connected vertices. In the latter, the keys are again references
            to items in the vertex dictionary, and the values are dictionaries
            of edge attributes.
        halfedge (dict of dict): A half-edge dictionary, which keeps track of
            undirected adjacencies. If the network is planar, the halfedges point
            at entries in the face dictionary.
        face (dict): The face dictionary. If the network is planar, this dictionary
            is populated by a face finding algorithm. Each key represents a face
            and points to its corresponding vertex cycle.
        facedata (dict): Face attributes.
        attributes (dict): A dictionary of miscellaneous information about the network.

    Examples:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            network.plot(
                vlabel={key: key for key in network},
                vsize=0.2
            )


        .. code-block:: python

            import compas
            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            # structure of the vertex dict

            for key in network.vertex:
                print key, network.vertex[key]

            # structure of the edge dict

            for u in network.edge:
                for v in network.edge[u]:
                    print u, v, network.edge[u][v]

            # structure of the halfedge dict

            for u in network.halfedge:
                for v in network.halfedge[u]:
                    if network.halfedge[u][v] is not None:
                        print network.face[network.halfedge[u][v]]
                    if network.halfedge[v][u] is not None:
                        print network.face[network.halfedge[v][u]]

            # structure of the face dict

            for fkey in network.face:
                print fkey, network.face[fkey], network.facedata[fkey]

    """

    def __init__(self):
        self._key_to_str   = False
        self._max_int_key  = -1
        self._max_int_fkey = -1
        self._plotter      = None
        self.vertex        = {}
        self.edge          = {}
        self.halfedge      = {}
        self.face          = {}
        self.facedata      = {}
        self.attributes    = {
            'name'         : 'Network',
            'color.vertex' : (0, 0, 0),
            'color.edge'   : (0, 0, 0),
            'color.face'   : (0, 0, 0),
        }
        self.default_vertex_attributes = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.default_edge_attributes   = {}
        self.default_face_attributes   = {}

    def __contains__(self, key):
        # if key in network: ...
        return key in self.vertex

    def __len__(self):
        # len(network)
        return len(self.vertex)

    def __iter__(self):
        # for key in network: ...
        return iter(self.vertex)

    def __getitem__(self, key):
        # network[key]
        return self.vertex[key]

    def __str__(self):
        """"""
        v = len(self.vertex)
        e = len(self.edges())
        dmin = 0 if not self.vertex else min(self.degree(key) for key in self.vertex)
        dmax = 0 if not self.vertex else max(self.degree(key) for key in self.vertex)
        if not self.default_vertex_attributes:
            dva = None
        else:
            dva = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_vertex_attributes.items()])
        if not self.default_edge_attributes:
            dea = None
        else:
            dea = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_edge_attributes.items()])
        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
network: {0}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- default vertex attributes

{5}

- default edge attributes

{6}

- number of vertices: {1}
- number of edges: {2}

- vertex degree min: {3}
- vertex degree max: {4}

""".format(self.attributes['name'], v, e, dmin, dmax, dva, dea)

    # --------------------------------------------------------------------------
    # descriptors
    # --------------------------------------------------------------------------

    @property
    def name(self):
        return self.attributes['name']

    @name.setter
    def name(self, value):
        self.attributes['name'] = value

    @property
    def adjacency(self):
        """Alias for the halfedge attribute."""
        return self.halfedge

    @property
    def data(self):
        """A dictionary describing the fundamental data making up the network data structure.

        The data dict contains the following keys:

        * attributes
        * default_vertex_attributes
        * dea
        * dfa
        * vertex
        * edge
        * halfedge
        * face
        * facedata
        * vcount
        * fcount

        """
        return {'attributes'  : self.attributes,
                'dva'         : self.default_vertex_attributes,
                'dea'         : self.default_edge_attributes,
                'dfa'         : self.default_face_attributes,
                'vertex'      : self.vertex,
                'edge'        : self.edge,
                'halfedge'    : self.halfedge,
                'face'        : self.face,
                'facedata'    : self.facedata,
                'max_int_key' : self._max_int_key,
                'max_int_fkey': self._max_int_fkey}

    @data.setter
    def data(self, data):
        attributes   = data.get('attributes') or {}
        dva          = data.get('dva') or {}
        dea          = data.get('dea') or {}
        dfa          = data.get('dfa') or {}
        vertex       = data.get('vertex') or {}
        edge         = data.get('edge') or {}
        halfedge     = data.get('halfedge') or {}
        face         = data.get('face') or {}
        facedata     = data.get('facedata') or {}
        vcount       = data.get('vcount') or 0
        fcount       = data.get('fcount') or 0
        max_int_key  = data.get('max_int_key') or vcount - 1
        max_int_fkey = data.get('max_int_fkey') or fcount - 1

        if not vertex or not edge or not halfedge:
            return

        del self.vertex
        del self.edge
        del self.halfedge
        del self.face
        del self.facedata

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_edge_attributes.update(dea)
        self.default_face_attributes.update(dfa)
        self.vertex   = {}
        self.edge     = {}
        self.halfedge = {}
        self.face     = {}
        self.facedata = {}

        for key, attr in vertex.iteritems():
            self.vertex[key] = self.default_vertex_attributes.copy()
            if attr:
                self.vertex[key].update(attr)

        for u, nbrs in edge.iteritems():
            if u not in self.edge:
                self.edge[u] = {}
            nbrs = nbrs or {}
            for v, attr in nbrs.iteritems():
                self.edge[u][v] = self.default_edge_attributes.copy()
                if attr:
                    self.edge[u][v].update(attr)

        for key, nbrs in halfedge.iteritems():
            if key not in self.halfedge:
                self.halfedge[key] = {}
            if not nbrs:
                nbrs = {}
            for nbr, fkey in nbrs.iteritems():
                self.halfedge[key][nbr] = fkey

        for fkey, vertices in face.iteritems():
            self.face[fkey] = vertices

        for fkey, attr in facedata.iteritems():
            self.facedata[fkey] = attr

        self._max_int_key = max_int_key
        self._max_int_fkey = max_int_fkey

    @property
    def plotter(self):
        """Provide read access to a plotter object."""
        if not self._plotter:
            from compas.datastructures.network.plotter import NetworkPlotter2D
            self._plotter = NetworkPlotter2D(self)
        return self._plotter

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_data(cls, data):
        network = cls()
        network.data = data
        return network

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        network = cls()
        network.data = data
        return network

    @classmethod
    def from_yaml(cls, filepath):
        raise NotImplementedError

    @classmethod
    def from_obj(cls, filepath, precision='3f'):
        network  = cls()
        obj      = OBJ(filepath, precision=precision)
        vertices = obj.parser.vertices
        edges    = obj.parser.lines
        for i, (x, y, z) in enumerate(vertices):
            network.add_vertex(i, x=x, y=y, z=z)
        for u, v in edges:
            network.add_edge(u, v)
        return network

    @classmethod
    def from_lines(cls, lines, precision='3f'):
        network = cls()
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
            network.add_vertex(i, x=xyz[0], y=xyz[1], z=xyz[2])
        for u, v in edges:
            i = key_index[u]
            j = key_index[v]
            network.add_edge(i, j)
        return network

    @classmethod
    def from_vertices_and_edges(cls, vertices, edges):
        network = cls()
        for x, y, z in vertices:
            network.add_vertex(x=x, y=y, z=z)
        for u, v in edges:
            network.add_edge(u, v)
        return network

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_data(self):
        return self.data

    def to_json(self, filepath):
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)

    def to_yaml(self, filepath):
        raise NotImplementedError

    def to_obj(self, filepath):
        raise NotImplementedError

    def to_lines(self):
        return [(self.vertex_coordinates(u), self.vertex_coordinates(v)) for u, v in self.edges_iter()]

    def to_vertices_and_edges(self):
        key_index = dict((key, index) for index, key in self.vertices_enum())
        vertices  = [self.vertex_coordinates(key) for key in self]
        edges     = [(key_index[u], key_index[v]) for u, v in self.edges_iter()]
        return vertices, edges

    # --------------------------------------------------------------------------
    # reset
    # --------------------------------------------------------------------------

    def clear_vertexdict(self):
        del self.vertex
        self.vertex = {}
        self._max_int_key = -1

    def clear_facedict(self):
        del self.face
        self.face = {}
        self._max_int_fkey = -1

    def clear_halfedgedict(self):
        del self.halfedge
        self.halfedge = {}

    # --------------------------------------------------------------------------
    # modify
    # --------------------------------------------------------------------------

    def _get_vertexkey(self, key):
        if key is None:
            key = self._max_int_key = self._max_int_key + 1
        else:
            try:
                int(key)
            except (ValueError, TypeError):
                pass
            else:
                if int(key) > self._max_int_key:
                    self._max_int_key = int(key)
        return key

    def _get_facekey(self, fkey):
        if fkey is None:
            fkey = self._max_int_fkey = self._max_int_fkey + 1
        else:
            try:
                int(fkey)
            except (ValueError, TypeError):
                pass
            else:
                if int(fkey) > self._max_int_fkey:
                    self._max_int_fkey = int(fkey)
        return fkey

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """"""
        attr = self.default_vertex_attributes.copy()
        if attr_dict is None:
            attr_dict = kwattr
        else:
            attr_dict.update(kwattr)
        attr.update(attr_dict)
        key = self._get_vertexkey(key)
        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
            self.edge[key] = {}
        self.vertex[key].update(attr)
        return key

    def add_edge(self, u, v, attr_dict=None, **kwattr):
        """"""
        attr = self.default_edge_attributes.copy()
        if attr_dict is None:
            attr_dict = kwattr
        else:
            attr_dict.update(kwattr)
        attr.update(attr_dict)
        if u not in self.vertex:
            u = self.add_vertex(u)
        if v not in self.vertex:
            v = self.add_vertex(v)
        data_dict = self.edge[u].get(v, {})
        data_dict.update(attr)
        self.edge[u][v] = data_dict
        self.halfedge[u][v] = None
        self.halfedge[v][u] = None
        return u, v

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        attr = self.default_face_attributes.copy()
        if attr_dict is None:
            attr_dict = kwattr
        else:
            attr_dict.update(kwattr)
        attr.update(attr_dict)
        # check if face is valid
        if vertices[-2] == vertices[-1]:
            del vertices[-1]
        if len(vertices) < 3:
            return
        # get the correct face key
        fkey = self._get_facekey(fkey)
        self.face[fkey] = vertices
        self.facedata[fkey] = attr
        for i in range(0, len(vertices) - 1):
            u = vertices[i]
            v = vertices[i + 1]
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None
            if u in self.edge and v in self.edge[u]:
                continue
            if v in self.edge and u in self.edge[v]:
                continue
            if u not in self.edge:
                self.edge[u] = {}
            self.edge[u][v] = {}
        return fkey

    # def remove_vertex(self, key):
    #     pass

    # def remove_edge(self, u, v):
    #     raise NotImplementedError
    #     if self.face:
    #         # there are faces
    #         f1 = self.halfedge[u][v]
    #         f2 = self.halfedge[v][u]
    #         if f1 is not None and f2 is not None:
    #             vertices1 = self.face[f1]
    #             vertices2 = self.face[f2]
    #     else:
    #         # there are no faces
    #         del self.halfedge[u][v]
    #         del self.halfedge[v][u]
    #         del self.edge[u][v]

    # --------------------------------------------------------------------------
    # face construction
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # lists and iterators
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        if data:
            return self.vertex.items()
        return self.vertex.keys()

    def vertices_iter(self, data=False):
        if data:
            return self.vertex.iteritems()
        return self.vertex.iterkeys()

    def vertices_enum(self, data=False):
        for index, (key, attr) in enumerate(self.vertices_iter(True)):
            if data:
                yield index, key, attr
            else:
                yield index, key

    def edges(self, data=False):
        return list(self.edges_iter(data))

    def edges_iter(self, data=False):
        for u, nbrs in self.edge.iteritems():
            for v, attr in nbrs.iteritems():
                if data:
                    yield u, v, attr
                else:
                    yield u, v

    def edges_enum(self, data=False):
        index = 0
        for u, nbrs in self.edge.iteritems():
            for v, attr in nbrs.iteritems():
                if data:
                    yield index, u, v, attr
                else:
                    yield index, u, v
                index += 1

    # --------------------------------------------------------------------------
    # face lists and iterators
    # --------------------------------------------------------------------------

    def faces(self, data=False):
        if data:
            return [(fkey, self.facedata.setdefault(fkey, self.default_face_attributes.copy())) for fkey in self.face]
        return list(self.faces_iter())

    def faces_iter(self, data=False):
        for fkey in self.face:
            if data:
                yield fkey, self.facedata.setdefault(fkey, self.default_face_attributes.copy())
            else:
                yield fkey

    def faces_enum(self, data=False):
        for index, fkey in enumerate(self.faces_iter()):
            if data:
                yield index, fkey, self.facedata.setdefault(fkey, self.default_face_attributes.copy())
            else:
                yield index, fkey

    # --------------------------------------------------------------------------
    # topology
    # --------------------------------------------------------------------------

    def has_vertex(self, key):
        return key in self.vertex

    def has_edge(self, u, v):
        return u in self.edge and v in self.edge[u]

    # change to ordered?
    # clarify CCW vs CW in blog post
    def neighbours(self, key, ordered=None):
        nbrs = list(self.halfedge[key])
        if not ordered:
            return nbrs
        if len(nbrs) == 1:
            return nbrs
        nbr = nbrs[0]
        start = nbr
        nbrs = [start]
        while True:
            fkey = self.halfedge[key][nbr]  # the fkey should not be None
            vertices = self.face_vertices(fkey)[:-1]
            i = vertices.index(key)
            nbr = vertices[i - 1]
            if nbr == start:
                break
            nbrs.append(nbr)
        return nbrs

    def neighbours_out(self, key):
        return list(self.edge[key])

    def neighbours_in(self, key):
        return list(set(self.halfedge[key]) - set(self.edge[key]))

    def degree(self, key):
        return len(self.neighbours(key))

    def degree_out(self, key):
        return len(self.neighbours_out(key))

    def degree_in(self, key):
        return len(self.neighbours_in(key))

    def leaves(self):
        return [key for key, nbrs in self.halfedge.iteritems() if len(nbrs) == 1]

    def connected_edges(self, key):
        edges = []
        for nbr in self.neighbours(key):
            if nbr in self.edge[key]:
                edges.append((key, nbr))
            else:
                edges.append((nbr, key))
        return edges

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    def vertex_faces(self, key, ordered=False):
        if not ordered:
            return self.halfedge[key].values()
        nbrs = self.neighbours(key, ordered=True)
        return [self.halfedge[key][n] for n in nbrs]

    def is_vertex_leaf(self, key):
        return self.degree(key) == 1

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    def face_vertices(self, fkey):
        return self.face[fkey]

    def face_descendant(self, fkey, key):
        vertices = self.face_vertices(fkey)
        for i in range(0, len(vertices) - 1):
            u = vertices[i]
            v = vertices[i + 1]
            if u == key:
                return v
        return None

    def face_ancestor(self, fkey, key):
        raise NotImplementedError

    def face_halfedges(self, fkey):
        vertices = self.face_vertices(fkey)
        halfedges = []
        for i in range(0, len(vertices) - 1):
            u = vertices[i]
            v = vertices[i + 1]
            halfedges.append((u, v))
        return halfedges

    def face_edges(self, fkey):
        edges = []
        for u, v in self.face_halfedges(fkey):
            if v not in self.edge[u]:
                u, v = v, u
            edges.append((u, v))
        return edges

    def face_adjacency(self):
        adj = {}
        for fkey, vertices in self.face.iteritems():
            adj[fkey] = []
            for i in range(0, len(vertices) - 1):
                u = vertices[i]
                v = vertices[i + 1]
                nkey = self.halfedge[v][u]
                adj[fkey].append(nkey)
        return adj

    def face_tree(self, root, algo=network_bfs):
        adj = self.face_adjacency()
        tree = algo(root, adj)
        return tree

    def face_adjacency_edge(self, f1, f2):
        for u, v in self.face_halfedges(f1):
            if self.halfedge[v][u] == f2:
                if v in self.edge[u]:
                    return u, v
                return v, u

    # --------------------------------------------------------------------------
    # attributes: vertex
    # --------------------------------------------------------------------------

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
    # attributes: edge
    # --------------------------------------------------------------------------

    def update_default_edge_attributes(self, attr_dict=None, **kwargs):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwargs)
        self.default_edge_attributes.update(attr_dict)
        for u, v in self.edges_iter():
            attr = attr_dict.copy()
            attr.update(self.edge[u][v])
            self.edge[u][v] = attr

    def set_edge_attribute(self, u, v, name, value):
        self.edge[u][v][name] = value

    def set_edge_attributes(self, u, v, attr_dict=None, **kwattr):
        attr_dict = attr_dict or kwattr
        attr_dict.update(kwattr)
        self.edge[u][v].update(attr_dict)

    def set_edges_attribute(self, name, value, keys=None):
        if not keys:
            for u, v, attr in self.edges_iter(True):
                attr[name] = value
        else:
            for u, v in keys:
                self.edge[u][v][name] = value

    def set_edges_attributes(self, keys=None, attr_dict=None, **kwattr):
        attr_dict = attr_dict or {}
        attr_dict.update(kwattr)
        if not keys:
            for u, v, attr in self.edges_iter(True):
                attr.update(attr_dict)
        else:
            for u, v in keys:
                self.edge[u][v].update(attr_dict)

    def get_edge_attribute(self, u, v, name, default=None):
        if u in self.edge[v]:
            return self.edge[v][u].get(name, default)
        return self.edge[u][v].get(name, default)

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
            for fkey, attr in self.faces_iter(True):
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
            for fkey, attr in self.faces_iter(True):
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

    # --------------------------------------------------------------------------
    # attribute filters
    # --------------------------------------------------------------------------

    def vertices_where(self, where):
        """Get vertices for which a certain condition or set of conditions is ``True``.

        Parameters:
            where (dict): A set of conditions in the form of key-value pairs.
                The keys should be attribute names. The values can be attribute
                values or ranges of attribute values in the form of min/max pairs.

        Returns:
            list: A list of vertex keys that satisfy the condition(s).

        """
        keys = []
        for key, attr in self.vertices_iter(True):
            is_match = True
            for name, value in where.items():
                if name not in attr:
                    is_match = False
                    break
                if isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if attr[name] < minval or attr[name] > maxval:
                        is_match = False
                        break
                else:
                    if value != attr[name]:
                        is_match = False
                        break
            if is_match:
                keys.append(key)
        return keys

    def edges_where(self, where):
        """Get edges for which a certain condition or set of conditions is ``True``.

        Parameters:
            where (dict) : A set of conditions in the form of key-value pairs.
                The keys should be attribute names. The values can be attribute
                values or ranges of attribute values in the form of min/max pairs.

        Returns:
            list: A list of edge keys that satisfy the condition(s).

        """
        keys = []
        for u, v, attr in self.edges_iter(True):
            is_match = True
            for name, value in where.items():
                if name not in attr:
                    is_match = False
                    break
                if isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if attr[name] < minval or attr[name] > maxval:
                        is_match = False
                        break
                else:
                    if value != attr[name]:
                        is_match = False
                        break
            if is_match:
                keys.append((u, v))
        return keys

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, key, xyz='xyz'):
        return [self.vertex[key][axis] for axis in xyz]

    def vertex_area(self, key):
        key_xyz = dict((key, self.vertex_coordinates(key)) for key in self)
        fkey_centroid = {}
        for fkey, vertices in self.face.items():
            if vertices[0] != vertices[-1] and len(vertices) > 4:
                continue
            fkey_centroid[fkey] = centroid_points([key_xyz[k] for k in set(vertices)])
        return self._vertex_area(key, key_xyz, fkey_centroid)

    def _vertex_area(self, key, key_xyz, fkey_centroid):
        area = 0
        p0 = key_xyz[key]
        for nbr in self.halfedge[key]:
            p1 = key_xyz[nbr]
            v01 = [p1[i] - p0[i] for i in range(3)]
            fkey = self.halfedge[key][nbr]
            if fkey in fkey_centroid:
                p2 = fkey_centroid[fkey]
                v02 = [p2[i] - p0[i] for i in range(3)]
                area += 0.25 * length_vector(cross_vectors(v01, v02))
            fkey = self.halfedge[nbr][key]
            if fkey in fkey_centroid:
                p3 = fkey_centroid[fkey]
                v03 = [p3[i] - p0[i] for i in range(3)]
                area += 0.25 * length_vector(cross_vectors(v01, v03))
        return area

    def vertex_laplacian(self, key):
        centroid = centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbours(key)])
        point = self.vertex_coordinates(key)
        return subtract_vectors(centroid, point)

    def vertex_neighbourhood_centroid(self, key):
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbours(key)])

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def edge_vector(self, u, v):
        sp = self.vertex_coordinates(u)
        ep = self.vertex_coordinates(v)
        return [ep[i] - sp[i] for i in range(3)]

    def edge_length(self, u, v):
        vec = self.edge_vector(u, v)
        return sum(vec[i] ** 2 for i in range(3)) ** 0.5

    def edge_coordinates(self, u, v, xyz='xyz'):
        return (self.vertex_coordinates(u, xyz=xyz),
                self.vertex_coordinates(v, xyz=xyz))

    def edge_midpoint(self, u, v, xyz='xyz'):
        sp, ep = self.edge_coordinates(u, v, xyz=xyz)
        return [0.5 * (sp[i] + ep[i]) for i in range(len(xyz))]

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    def face_centroid(self, fkey):
        return centroid_points([self.vertex_coordinates(key) for key in set(self.face[fkey])])

    def face_center(self, fkey):
        vertices = self.face[fkey]
        if vertices[-1] == vertices[0]:
            vertices = vertices[0:-1]
        return center_of_mass_polygon([self.vertex_coordinates(key) for key in vertices])

    def face_area(self, fkey):
        vertices = self.face_vertices(fkey)
        if vertices[0] == vertices[-1]:
            vertices = vertices[0:-1]
        return area_polygon([self.vertex_coordinates(key) for key in vertices])

    # --------------------------------------------------------------------------
    # boundary
    # remove?
    # --------------------------------------------------------------------------

    def boundary_faces(self):
        faces = []
        for fkey, vertices in self.face.iteritems():
            if vertices[0] != vertices[-1]:
                if len(vertices) > 4:
                    faces.append(fkey)
        return faces

    def boundary_vertices(self):
        vertices = []
        seen = set()
        for fkey in self.boundary_faces():
            for key in self.face[fkey]:
                if key not in seen:
                    seen.add(key)
                    vertices.append(key)
        return vertices

    def boundary_edges(self):
        edges = []
        for fkey in self.boundary_faces():
            vertices = self.face[fkey]
            for i in range(len(vertices) - 1):
                u = vertices[i]
                v = vertices[i + 1]
                if v in self.edge[u]:
                    edges.append((u, v))
                else:
                    edges.append((v, u))
        return edges

    # --------------------------------------------------------------------------
    # names
    # --------------------------------------------------------------------------

    def vertex_name(self, key):
        return '{0}.vertex.{1}'.format(self.name, key)

    def edge_name(self, u, v):
        return '{0}.edge.{1}-{2}'.format(self.name, u, v)

    def face_name(self, fkey):
        return '{0}.face.{1}'.format(self.name, fkey)

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def key_index(self):
        return {key: index for index, key in self.vertices_enum()}

    def index_key(self):
        return dict(self.vertices_enum())

    def uv_index(self):
        return {(u, v): index for index, u, v in self.edges_enum()}

    def index_uv(self):
        return {index: (u, v) for index, u, v in self.edges_enum()}

    def vertex_color(self, key, qualifier=None):
        if qualifier:
            if self.vertex[key][qualifier]:
                return self.attributes.get('color.vertex:{0}'.format(qualifier))
            return self.attributes.get('color.vertex')
        return self.attributes.get('color.vertex')

    def copy(self):
        cls  = type(self)
        data = deepcopy(self.data)
        return cls.from_data(data)

    def edge_index(self, u, v):
        uv_index = self.uv_index()
        return uv_index[(u, v)]

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # visualisation
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------

    def plot(self,
             vertices_on=True,
             edges_on=True,
             faces_on=False,
             vcolor=None,
             ecolor=None,
             fcolor=None,
             vlabel=None,
             vsize=None,
             elabel=None,
             ewidth=None,
             flabel=None,
             points=None,
             lines=None):
        import matplotlib.pyplot as plt
        from compas.plotters.drawing import create_axes_2d
        # the network plotter should take care of axes, bounds, autoscale, show, ...
        # only necessary import should be the plotter
        axes = create_axes_2d()
        plotter = self.plotter
        plotter.vertices_on = vertices_on
        plotter.edges_on = edges_on
        plotter.faces_on = faces_on
        if vcolor:
            plotter.vcolor = vcolor
        if ecolor:
            plotter.ecolor = ecolor
        if fcolor:
            plotter.fcolor = fcolor
        if vlabel:
            plotter.vlabel = vlabel
        if vsize:
            plotter.vsize = vsize
        if elabel:
            plotter.elabel = elabel
        if ewidth:
            plotter.ewidth = ewidth
        if flabel:
            plotter.flabel = flabel
        if points:
            plotter.points = points
        if lines:
            plotter.lines = lines
        plotter.plot(axes)
        axes.autoscale()
        plt.show()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas

    network = Network.from_obj(compas.get_data('lines.obj'))

    print network

    network.plot(vlabel={key: key for key in network})
