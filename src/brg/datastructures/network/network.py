# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

import json

from brg.files.obj import OBJ

from brg.geometry.functions import centroid
from brg.geometry.functions import center_of_mass
from brg.geometry.functions import cross
from brg.geometry.functions import length
from brg.geometry.functions import area

from brg.datastructures.utilities import geometric_key

from brg.datastructures.traversal import bfs


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 7, 2014'


class Network(object):
    """"""

    def __init__(self, **kwargs):
        self.vertex       = {}
        self.edge         = {}
        self.halfedge     = {}
        self.face         = {}
        self.dualdata     = None
        self.vertex_count = 0
        self.face_count   = 0
        self.attributes   = {
            'name'         : 'Network',
            'color.vertex' : (0, 0, 0),
            'color.edge'   : (0, 0, 0),
        }
        self.attributes.update(kwargs)
        self.dva = {}
        self.dea = {}
        self.dfa = {}

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
        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
network summary (under construction)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

name: {0}

- number of vertices: {1}
- number of edges: {2}

- vertex degree min: {3}
- vertex degree max: {4}

""".format(self.name,
           len(self.vertex),
           len(self.edges()),
           (0 if not self.vertex else min(self.degree(key) for key in self.vertex)),
           (0 if not self.vertex else max(self.degree(key) for key in self.vertex)),)

    # --------------------------------------------------------------------------
    # descriptors
    # --------------------------------------------------------------------------

    @property
    def name(self):
        return self.attributes['name']

    @name.setter
    def name(self, name):
        self.attributes['name'] = name

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

    # include dualdata for data of faces

    @property
    def data(self):
        return {'attributes' : self.attributes,
                'dva'        : self.dva,
                'dea'        : self.dea,
                'dfa'        : self.dfa,
                'vertex'     : self.vertex,
                'edge'       : self.edge,
                'halfedge'   : self.halfedge,
                'face'       : self.face,
                'vcount'     : self.vertex_count,
                'fcount'     : self.face_count}

    @data.setter
    def data(self, data):
        attributes = data.get('attributes') or {}
        dva        = data.get('dva') or {}
        dea        = data.get('dea') or {}
        dfa        = data.get('dfa') or {}
        vertex     = data.get('vertex') or {}
        edge       = data.get('edge') or {}
        halfedge   = data.get('halfedge') or {}
        face       = data.get('face') or {}
        vcount     = data.get('vcount') or 0
        fcount     = data.get('fcount') or 0
        if not vertex or not edge or not halfedge:
            return
        del self.vertex
        del self.edge
        del self.halfedge
        del self.face
        self.attributes.update(attributes)
        self.dva.update(dva)
        self.dea.update(dea)
        self.dfa.update(dfa)
        self.vertex   = {}
        self.edge     = {}
        self.halfedge = {}
        self.face     = {}
        for key, attr in vertex.iteritems():
            self.vertex[key] = self.dva.copy()
            if attr:
                self.vertex[key].update(attr)
        for u, nbrs in edge.iteritems():
            if u not in self.edge:
                self.edge[u] = {}
            nbrs = nbrs or {}
            for v, attr in nbrs.iteritems():
                self.edge[u][v] = self.dea.copy()
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
        self.vertex_count = vcount
        self.face_count = fcount

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_data(cls, data, **kwargs):
        network = cls(**kwargs)
        network.data = data
        return network

    @classmethod
    def from_json(cls, filepath, **kwargs):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        network = cls(**kwargs)
        network.data = data
        return network

    # should the processing of anchors be implicit?
    # no, but there should be (a) function(s) to identify features based on
    # data info from an obj
    @classmethod
    def from_obj(cls, filepath, precision='3f', **kwargs):
        network  = cls(**kwargs)
        obj      = OBJ(filepath, precision=precision)
        vertices = obj.parser.vertices
        edges    = obj.parser.lines
        points   = obj.parser.points
        for i, (x, y, z) in enumerate(vertices):
            if i in points:
                network.add_vertex(i, x=x, y=y, z=z, is_anchor=True)
            else:
                network.add_vertex(i, x=x, y=y, z=z, is_anchor=False)
        for u, v in edges:
            network.add_edge(u, v)
        return network

    @classmethod
    def from_lines(cls, lines, precision='3f', **kwargs):
        network = cls(**kwargs)
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
    def from_vertices_and_edges(cls, vertices, edges, **kwargs):
        network = cls(**kwargs)
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

    def to_obj(self, filepath):
        raise NotImplementedError

    def to_lines(self):
        raise NotImplementedError

    def to_vertices_and_edges(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # modify
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """"""
        attr = self.dva.copy()
        if attr_dict is None:
            attr_dict = kwattr
        else:
            attr_dict.update(kwattr)
        attr.update(attr_dict)
        if key is None:
            key = self.vertex_count
        else:
            if int(key) > self.vertex_count:
                self.vertex_count = int(key)
        self.vertex_count += 1
        key = str(key)
        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
            self.edge[key] = {}
        self.vertex[key].update(attr)
        return key

    def add_edge(self, u, v, attr_dict=None, **kwattr):
        """"""
        attr = self.dea.copy()
        if attr_dict is None:
            attr_dict = kwattr
        else:
            attr_dict.update(kwattr)
        attr.update(attr_dict)
        u = str(u)
        v = str(v)
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

    def add_face(self, vertices, fkey=None):
        attr = self.dfa.copy()
        if vertices[-2] == vertices[-1]:
            del vertices[-1]
        if len(vertices) < 3:
            return
        if fkey is None:
            fkey = self.face_count
        else:
            if int(fkey) > self.face_count:
                self.face_count = int(fkey)
        self.face_count += 1
        fkey = str(fkey)
        self.face[fkey] = vertices
        for i in range(0, len(vertices) - 1):
            u = str(vertices[i])
            v = str(vertices[i + 1])
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
        # use this function to make sure dualdata exists
        # there should be a better way to do this
        # dualdata is really about face data
        # dualdata => facedata
        # dual function / attributes ?
        for name, value in attr.items():
            self.set_face_attribute(fkey, name, value)
        return fkey

    # --------------------------------------------------------------------------
    # face construction
    # --------------------------------------------------------------------------

    # remove this
    # add it to the face finding algorithm
    def breakpoints(self, key_index=None):
        return self.leaves(key_index=key_index)

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

    # add if data
    def faces(self):
        return list(self.faces_iter())

    # add if data
    def faces_iter(self):
        return self.face.iterkeys()

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

    def leaves(self, key_index=None):
        keys = [key for key, nbrs in self.halfedge.iteritems() if len(nbrs) == 1]
        if not key_index:
            return keys
        return [key_index[key] for key in keys]

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    def vertex_faces(self, key, ordered=False):
        if not ordered:
            return self.halfedge[key].values()
        nbrs = self.neighbours(key, ordered=True)
        return [self.halfedge[key][n] for n in nbrs]

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

    def face_edges(self, fkey):
        vertices = self.face_vertices(fkey)
        edges = []
        for i in range(0, len(vertices) - 1):
            u = vertices[i]
            v = vertices[i + 1]
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

    def face_tree(self, root, algo=bfs):
        adj = self.face_adjacency()
        tree = algo(root, adj)
        return tree

    # --------------------------------------------------------------------------
    # attributes
    # --------------------------------------------------------------------------

    def set_dva(self, attr_dict=None, **kwargs):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwargs)
        self.dva = attr_dict
        for key in self.vertex:
            attr = attr_dict.copy()
            attr.update(self.vertex[key])
            self.vertex[key] = attr

    def set_dea(self, attr_dict=None, **kwargs):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwargs)
        self.dea = attr_dict
        for u, v in self.edges_iter():
            attr = attr_dict.copy()
            attr.update(self.edge[u][v])
            self.edge[u][v] = attr

    def set_dfa(self, attr_dict=None, **kwargs):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwargs)
        self.dfa = attr_dict
        if not self.dualdata:
            self.dualdata = Network()
        for fkey in self.face:
            attr = attr_dict.copy()
            attr.update(self.dualdata.vertex[fkey])
            self.dualdata.vertex[fkey] = attr

    def set_vertex_attribute(self, key, name, value):
        self.vertex[key][name] = value

    def get_vertex_attribute(self, key, name, default=None):
        return self.vertex[key].get(name, default)

    def set_edge_attribute(self, u, v, name, value):
        self.edge[u][v][name] = value

    def get_edge_attribute(self, u, v, name, default=None):
        return self.edge[u][v].get(name, default)

    def set_face_attribute(self, fkey, name, value):
        if not self.dualdata:
            self.dualdata = Network()
        if fkey not in self.dualdata.vertex:
            self.dualdata.vertex[fkey] = {}
        self.dualdata.vertex[fkey][name] = value

    def get_face_attribute(self, fkey, name, default=None):
        if not self.dualdata:
            return default
        return self.dualdata.vertex[fkey].get(name, default)

    # --------------------------------------------------------------------------

    def set_vertices_attribute(self, name, value):
        if not isinstance(value, (list, tuple)):
            for i, key, attr in self.vertices_enum(True):
                attr[name] = value
        else:
            for i, key, attr in self.vertices_enum(True):
                attr[name] = value[i]

    def get_vertices_attribute(self, name, default=None):
        return [attr.get(name, default) for key, attr in self.vertices_iter(True)]

    def get_vertices_attributes(self, names, default=None):
        return [[attr.get(name, default) for name in names] for key, attr in self.vertices_iter(True)]

    def set_edges_attribute(self, name, values):
        for i, u, v, attr in self.edges_enum(True):
            attr[name] = values[i]

    def get_edges_attribute(self, name, default=None):
        return [attr.get(name, default) for u, v, attr in self.edges_iter(True)]

    def get_edges_attributes(self, names, default=None):
        return [[attr.get(name, default) for name in names] for u, v, attr in self.edges_iter(True)]

    def set_faces_attribute(self, name, values):
        for i, fkey, attr in self.edges_enum(True):
            attr[name] = values[i]

    def get_faces_attribute(self, name, default=None):
        return [self.get_face_attribute(fkey, name, default) for fkey in self.face]

    def get_faces_attributes(self, names, default=None):
        return [[self.get_face_attribute(fkey, name, default) for name in names] for fkey in self.face]

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, key, xyz='xyz'):
        return [self.vertex[key][axis] for axis in xyz]

    def vertex_area(self, key):
        key_xyz = self.vertex_coordinates()
        fkey_centroid = {}
        for fkey, vertices in self.face.items():
            if vertices[0] != vertices[-1] and len(vertices) > 4:
                continue
            fkey_centroid[fkey] = centroid([key_xyz[k] for k in set(vertices)])
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
                area += 0.25 * length(cross(v01, v02))
            fkey = self.halfedge[nbr][key]
            if fkey in fkey_centroid:
                p3 = fkey_centroid[fkey]
                v03 = [p3[i] - p0[i] for i in range(3)]
                area += 0.25 * length(cross(v01, v03))
        return area

    def edge_length(self, u, v):
        sp = self.vertex_coordinates(u)
        ep = self.vertex_coordinates(v)
        return (sum([(ep[i] - sp[i])**2 for i in range(len(ep))]))**0.5

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

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
        return centroid([self.vertex_coordinates(key) for key in set(self.face[fkey])])

    def face_center(self, fkey):
        vertices = self.face[fkey]
        if vertices[-1] == vertices[0]:
            vertices = vertices[0:-1]
        return center_of_mass([self.vertex_coordinates(key) for key in vertices])

    def face_area(self, fkey):
        vertices = self.face_vertices(fkey)
        if vertices[0] == vertices[-1]:
            vertices = vertices[0:-1]
        return area([self.vertex_coordinates(key) for key in vertices])

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
        return dict((key, index) for index, key in self.vertices_enum())

    def index_key(self):
        return dict(self.vertices_enum())

    def uv_index(self):
        return dict(((u, v), index) for index, u, v in self.edges_enum())

    def index_uv(self):
        return dict((index, (u, v)) for index, u, v in self.edges_enum())

    def vertex_color(self, key, qualifier=None):
        if qualifier:
            if self.vertex[key][qualifier]:
                return self.attributes.get('color.vertex:{0}'.format(qualifier))
            return self.attributes.get('color.vertex')
        return self.attributes.get('color.vertex')

    # --------------------------------------------------------------------------
    # drawing
    # --------------------------------------------------------------------------

    def draw(self, vcolor=None, vlabel=None, vsize=None, ecolor=None, elabel=None, ewidth=None, axes=None):
        from brg.datastructures.network.drawing import draw_network
        draw_network(self,
                     vcolor=vcolor,
                     vlabel=vlabel,
                     vsize=vsize,
                     ecolor=ecolor,
                     ewidth=ewidth,
                     elabel=elabel,
                     axes=axes)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg
    from brg.datastructures.network.drawing import draw_network

    network = Network.from_obj(brg.get_data('lines.obj'))

    vcolor = dict((key, '#ff0000') for key in network.vertex if network.degree(key) == 1)

    draw_network(network, vcolor=vcolor)
