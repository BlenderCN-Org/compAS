import json

from copy import deepcopy

from brg.geometry import length
from brg.geometry import cross
from brg.geometry import normal
from brg.geometry import normal2
from brg.geometry import centroid
from brg.geometry import center_of_mass
from brg.geometry import area

from brg.geometry.elements.line import Line

from brg.datastructures.mesh.exceptions import MeshError

from brg.datastructures.traversal import bfs
from brg.datastructures.traversal import bfs2

from brg.datastructures.mesh.algorithms.orientation import mesh_unify_cycle_directions
from brg.datastructures.mesh.algorithms.orientation import mesh_flip_cycle_directions

from brg.datastructures.mesh.constructors import mesh_from_data
from brg.datastructures.mesh.constructors import mesh_from_obj
from brg.datastructures.mesh.constructors import mesh_from_json
from brg.datastructures.mesh.constructors import mesh_from_vertices_and_faces
from brg.datastructures.mesh.constructors import mesh_from_boundary
from brg.datastructures.mesh.constructors import mesh_from_points


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 10, 2014'


# ==============================================================================
# ==============================================================================
# ==============================================================================
# Base mesh implementation
# ==============================================================================
# ==============================================================================
# ==============================================================================


class _Mesh(object):
    default_vertex_attributes = {}
    default_face_attributes = {}
    default_edge_attributes = {}

    def __init__(self):
        self._fkey = 0
        self._vkey = 0
        self.vertex = {}
        self.face = {}
        self.halfedge = {}
        self.edge = {}
        self.dualdata = None

    def __contains__(self, key):
        # if key in mesh: ...
        return key in self.vertex

    def __len__(self):
        # len(mesh)
        return len(self.vertex)

    def __iter__(self):
        # for key in mesh: ...
        return iter(self.vertex)

    def __getitem__(self, key):
        # mesh[key]
        return self.vertex[key]

    def __str__(self):
        """"""
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

- is_valid: {7}
- is_connected: {8}
- is_manifold: {9}
- is_trimesh: {10}
- is_quadmesh: {11}

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

""".format(len(self.vertex),
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
           ('True' if self.is_quadmesh() else 'False'),)

    @property
    def data(self):
        """The data representing the mesh."""
        return {'attributes' : self.attributes,
                'vertex'     : self.vertex,
                'halfedge'   : self.halfedge,
                'face'       : self.face,
                'edge'       : self.edge,
                'vkey'       : self._vkey,
                'fkey'       : self._fkey, }

    @data.setter
    def data(self, data):
        """"""
        attributes = data.get('attributes')
        vertex     = data.get('vertex')
        halfedge   = data.get('halfedge')
        face       = data.get('face')
        edge       = data.get('edge')
        vkey       = data.get('vkey')
        fkey       = data.get('fkey')
        if not vertex or not halfedge or not face:
            return
        self.attributes = attributes or {}
        self.edge       = edge or {}
        self.vertex     = {}
        self.halfedge   = {}
        self.face       = {}
        self._fkey      = fkey if fkey else int(max(face.keys(), key=int)) + 1
        self._vkey      = vkey if vkey else int(max(vertex.keys(), key=int)) + 1
        for k, a in vertex.items():
            a = a or {}
            da = self.default_vertex_attributes.copy()
            da.update(a)
            self.vertex[k] = da
        for k, n in halfedge.items():
            self.halfedge[k] = n or {}
        for k, c in face.items():
            self.face[k] = c or {}

    # **************************************************************************
    # constructors
    # **************************************************************************

    # @see: brg.datastructures.mesh.constructors
    # not to self: move them in

    # **************************************************************************
    # conversion methods
    # ------------------
    # to_...
    # **************************************************************************

    def to_data(self):
        return self.data

    def to_obj(self, filepath):
        """Write the mesh to an OBJ file.

        Parameters:
            filepath (str): Full path of the file to write.

        Returns:
            None
        """
        key_index = dict((key, index) for index, key in self.vertices_enum())
        with open(filepath, 'wb+') as fh:
            for key, attr in self.vertices_iter(True):
                fh.write('v {0[x]:.3f} {0[y]:.3f} {0[z]:.3f}\n'.format(attr))
            for fkey in self.face:
                vertices = self.face_vertices(fkey, ordered=True)
                vertices = [key_index[key] + 1 for key in vertices]
                fh.write('f {0[0]} {0[1]} {0[2]} {0[3]}\n'.format(vertices))

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

    def to_trimesh(self):
        from tri import TriMesh
        mesh = TriMesh()
        for key in self.vertex:
            attr = self.vertex[key]
            mesh.add_vertex(key=key, attr_dict=attr)
        for fkey in self.face:
            vertices = self.face_vertices(fkey)
            mesh.add_face(vertices, fkey=fkey)
        return mesh

    def to_quadmesh(self):
        from quad import QuadMesh
        mesh = QuadMesh()
        for key in self.vertex:
            attr = self.vertex[key]
            mesh.add_vertex(key=key, attr_dict=attr)
        for fkey in self.face:
            vertices = self.face_vertices(fkey)
            mesh.add_face(vertices, fkey=fkey)
        return mesh

    # **************************************************************************
    # modify the mesh
    # ---------------
    # add / remove / ...
    # **************************************************************************

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
            attr_dict (dict): Vertex attributes, defaults to None.
            **attr: Other named vertex attributes, defaults to None.

        Returns:
            str: The key of the vertex.
        """
        attr = self.default_vertex_attributes.copy()
        if attr_dict:
            attr.update(attr_dict)
        attr.update(kwattr)
        if key is None:
            key = self._vkey
            self._vkey += 1
        else:
            try:
                int(key)
            except ValueError:
                # do not let this pass!
                # raise MeshKeyError
                pass
            else:
                if int(key) > self._vkey:
                    self._vkey = int(key)
                self._vkey += 1
        key = str(key)
        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
        self.vertex[key].update(attr)
        return key

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

    def insert_vertex(self, fkey, xyz=None):
        """Insert a vertex in the specified face.

        Parameters:
            fkey (str): The key of the face in which the vertex should be inserted.

        Returns:
            str: The keys of the newly created faces.

        Raises:
            VelueError: If the face does not exist.
        """
        fkeys = []
        if not xyz:
            x, y, z = self.face_center(fkey)
        else:
            x, y, z = xyz
        w = self.add_vertex(x=x, y=y, z=z)
        for u, v in self.face[fkey].iteritems():
            fkeys.append(self.add_face([u, v, w]))
        del self.face[fkey]
        return fkeys

    def add_face(self, vertices, fkey=None):
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
        if vertices[0] == vertices[-1]:
            del vertices[-1]
        if vertices[-2] == vertices[-1]:
            del vertices[-1]
        if len(vertices) < 3:
            return
        if fkey is None:
            fkey = self._fkey
        else:
            if int(fkey) > self._fkey:
                self._fkey = int(fkey)
        self._fkey += 1
        fkey = str(fkey)
        self.face[fkey] = {}
        for i in range(-1, len(vertices) - 1):
            u = str(vertices[i])
            v = str(vertices[i + 1])
            self.face[fkey][u] = v
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None
        return fkey

    def remove_face(self, fkey):
        for u, v in self.face[fkey].items():
            self.halfedge[u][v] = None
            if self.halfedge[v][u] is None:
                del self.halfedge[u][v]
                del self.halfedge[v][u]
        del self.face[fkey]

    # **************************************************************************
    # helpers
    # **************************************************************************

    def key_index(self):
        return dict((key, index) for index, key in self.vertices_enum())

    def index_key(self):
        return dict((index, key) for index, key in self.vertices_enum())

    def copy(self):
        cls  = type(self)
        data = deepcopy(self.data)
        mesh = cls.from_data(data)
        return mesh

    def get_any_vertex(self):
        return next(self.vertices_iter())

    def get_any_face(self):
        return next(self.faces_iter())

    def get_any_face_vertex(self, fkey):
        return self.face_vertices(fkey)[0]

    # **************************************************************************
    # attributes
    # **************************************************************************

    def set_default_vertex_attributes(self, attr_dict=None, **kwargs):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwargs)
        self.default_vertex_attributes = attr_dict
        for key in self.vertex:
            attr = attr_dict.copy()
            attr.update(self.vertex[key])
            self.vertex[key] = attr

    def set_default_face_attributes(self, attr_dict=None, **kwargs):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwargs)
        self.default_face_attributes = attr_dict
        if not self.dualdata:
            self.dualdata = Mesh()
            for fkey in self.face:
                self.dualdata.add_vertex(key=fkey)
        for fkey in self.face:
            attr = attr_dict.copy()
            attr.update(self.dualdata.vertex[fkey])
            self.dualdata.vertex[fkey] = attr

    def set_vertex_attribute(self, key, name, value):
        self.vertex[key][name] = value

    def get_vertex_attribute(self, key, name, default=None):
        return self.vertex[key].get(name, default)

    def set_face_attribute(self, fkey, name, value):
        if not self.dualdata:
            self.dualdata = Mesh()
            self.dualdata.add_vertex(key=fkey)
        self.dualdata.vertex[fkey][name] = value

    def get_face_attribute(self, fkey, name, default=None):
        if not self.dualdata:
            return default
        return self.dualdata.vertex[fkey].get(name, default)

    # ..........................................................................
    # edge attributes
    # ---------------
    # - edges are virtual
    # - the only purpose of the edge dict is to store edge data
    # - unused edges can be culled
    # ..........................................................................

    def set_default_edge_attributes(self, attr_dict=None, **kwargs):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwargs)
        self.default_edge_attributes = attr_dict
        for u, v in self.edges():
            attr = attr_dict.copy()
            attr.update(self.edge[u][v])
            self.edge[u][v] = attr

    def set_edge_attribute(self, u, v, name, value):
        if u in self.edge and v in self.edge[u]:
            self.edge[u][v][name] = value
            return
        if v in self.edge and u in self.edge[v]:
            self.edge[v][u][name] = value
            return
        if u not in self.edge:
            self.edge[u] = {}
        self.edge[u][v] = {}
        self.edge[u][v][name] = value

    def get_edge_attribute(self, u, v, name, default=None):
        if u in self.edge:
            if v in self.edge[u]:
                return self.edge[u][v].get(name, default)
        if v in self.edge:
            if u in self.edge[v]:
                return self.edge[v][u].get(name, default)
        return default

    # **************************************************************************
    # culling
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
    # accessors
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
        """Get an enumeration of the vertex keys."""
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

    def edges_enum(self):
        """"""
        return enumerate(self.edges_iter())

    # **************************************************************************
    # properties
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
        nodes = bfs2(self.halfedge, root)
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
            if len(self.face[fkey]) > 3:
                return False
        return True

    def is_quadmesh(self, strict=False):
        if not self.face:
            return False
        for fkey in self.face:
            if len(self.face[fkey]) > 4:
                return False
            if strict and len(self.face[fkey]) < 4:
                return False
        return True

    # **************************************************************************
    # duality
    # **************************************************************************

    # @see: brg.datastructures.mesh.algorithms.duality

    # **************************************************************************
    # vertex topology
    # **************************************************************************

    def vertex_adjacency(self, ordered=False):
        if not ordered:
            # return dict((key, set(self.halfedge[key])) for key in self.vertex)
            return self.halfedge
        raise NotImplementedError

    # ordered vs ordering
    # see equivalent function in network
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
        if fkey is None:
            raise MeshError
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

    def vertex_ring(self, key):
        raise NotImplementedError

    def vertex_cycle(self, key):
        nbrs = self.vertex_neighbours(key, ordered=True)
        return dict((nbrs[i], nbrs[i + 1]) for i in range(-1, len(nbrs) - 1))

    def vertex_descendant(self, u, v):
        """Return the key of the vertex after v in the face that contains uv."""
        fkey = self.halfedge[u][v]
        # the face is on the inside
        if fkey is not None:
            return self.face[fkey][v]
        # the face is on the outside
        for nbr in self.halfedge[v]:
            if nbr != u:
                if self.halfedge[v][nbr] is None:
                    return nbr
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

    boundary_vertices = vertices_on_boundary

    # **************************************************************************
    # face topology
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
        adjacency = {}
        for fkey in self.face:
            neighbours = []
            for u, v in self.face[fkey].iteritems():
                for test in self.face:
                    if test == fkey:
                        continue
                    if u in self.face[test]:
                        if v == self.face[test][u]:
                            neighbours.append(test)
                            break
                    if v in self.face[test]:
                        if u == self.face[test][v]:
                            neighbours.append(test)
                            break
            adjacency[fkey] = neighbours
        return adjacency

    def faces_on_boundary(self):
        faces = {}
        for key, nbrs in self.halfedge.iteritems():
            for nbr, fkey in nbrs.iteritems():
                if fkey is None:
                    faces[self.halfedge[nbr][key]] = 1
        return faces.keys()

    boundary_faces = faces_on_boundary

    def face_tree(self, root, algo=bfs):
        return algo(self.face_adjacency(), root)

    # **************************************************************************
    # (half)edge topology
    # **************************************************************************

    def has_edge(self, u, v, strict=False):
        return v in self.halfedge[u] and u in self.halfedge[v]

    def is_edge_naked(self, u, v):
        return (self.halfedge[u][v] is None or self.halfedge[v][u] is None)

    def edges_on_boundary(self):
        return [(u, v) for u, v in self.edges_iter() if self.is_edge_naked(u, v)]

    boundary_edges = edges_on_boundary

    # **************************************************************************
    # geometry
    # **************************************************************************

    def vertex_area(self, key, length=length, cross=cross):
        a  = 0
        p0 = self.vertex_coordinates(key)
        for nbr in self.halfedge[key]:
            p1   = self.vertex_coordinates(nbr)
            v01  = [p1[i] - p0[i] for i in range(3)]
            fkey = self.halfedge[key][nbr]
            if fkey:
                p2  = self.face_centroid(fkey)
                v02 = [p2[i] - p0[i] for i in range(3)]
                a  += 0.25 * length(cross(v01, v02))
            fkey = self.halfedge[nbr][key]
            if fkey:
                p3  = self.face_centroid(fkey)
                v03 = [p3[i] - p0[i] for i in range(3)]
                a  += 0.25 * length(cross(v01, v03))
        return a

    def vertex_coordinates(self, key=None, xyz='xyz'):
        if key is not None:
            return [self.vertex[key][_] for _ in xyz]
        return [self.vertex_coordinates(k, xyz=xyz) for k in self.vertex]

    def vertex_normal(self, key):
        a  = 0
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
            a  += self.face_area(fkey)
        return nx / a, ny / a, nz / a

    def face_coordinates(self, fkey=None, ordered=False):
        if fkey is not None:
            vertices = self.face_vertices(fkey, ordered=ordered)
            return [self.vertex_coordinates(key) for key in vertices]
        return [self.face_coordinates(k, ordered=ordered) for k in self.face]

    def face_normal(self, fkey, unitized=True):
        vertices = self.face_vertices(fkey, ordered=True)
        return normal2([self.vertex_coordinates(key) for key in vertices], unitized)

    def face_centroid(self, fkey):
        vertices = self.face_vertices(fkey, ordered=True)
        return centroid([self.vertex_coordinates(key) for key in vertices])

    def face_center(self, fkey):
        vertices = self.face_vertices(fkey, ordered=True)
        return center_of_mass([self.vertex_coordinates(key) for key in vertices])

    def face_area(self, fkey):
        vertices = self.face_vertices(fkey, ordered=True)
        return area([self.vertex_coordinates(key) for key in vertices])

    def edge_length(self, u, v):
        sp = self.vertex_coordinates(u)
        ep = self.vertex_coordinates(v)
        l = sum((ep[i] - sp[i]) ** 2 for i in range(3)) ** 0.5
        return l

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
        l = sum(axis ** 2 for axis in vec) ** 0.5
        return [axis / l for axis in vec]


# ==============================================================================
# ==============================================================================
# ==============================================================================
# Mesh implementation with functionality for practical use
# ==============================================================================
# ==============================================================================
# ==============================================================================


class Mesh(_Mesh):
    """"""

    unify_cycles = mesh_unify_cycle_directions
    flip_cycles = mesh_flip_cycle_directions

    def __init__(self):
        super(Mesh, self).__init__()
        self.attributes = {
            'name'         : 'Mesh',
            'color.vertex' : (0, 0, 0),
            'color.edge'   : (0, 0, 0),
            'color.face'   : (0, 0, 0),
        }

    @property
    def name(self):
        """The name of the mesh."""
        return self.attributes.get('name', None)

    @name.setter
    def name(self, value):
        self.attributes['name'] = value

    @property
    def color(self):
        return dict(
            (key[6:], self.attributes[key])
            for key in self.attributes if key.startswith('color.')
        )

    @color.setter
    def color(self, value):
        try:
            value[0]
            value[1]
            value[1][2]
        except Exception:
            return
        self.attributes['color.{0}'.format(value[0])] = value[1]

    # move this somewhere else
    # with other repr functions...
    # this function has to be overwritten by environment-specific wrappers!!
    def draw(self, **kwargs):
        from brg.datastructures.mesh.drawing import draw_mesh
        draw_mesh(self, **kwargs)


Mesh.from_vertices_and_faces = classmethod(mesh_from_vertices_and_faces)
Mesh.from_data               = classmethod(mesh_from_data)
Mesh.from_obj                = classmethod(mesh_from_obj)
Mesh.from_json               = classmethod(mesh_from_json)
Mesh.from_boundary           = classmethod(mesh_from_boundary)
Mesh.from_points             = classmethod(mesh_from_points)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    print mesh
    print 'is_valid', mesh.is_valid()
    print 'is_regular:', mesh.is_regular()

    mesh.draw(
        show_vertices=True,
        face_label=dict((fkey, fkey) for fkey in mesh.face)
    )
