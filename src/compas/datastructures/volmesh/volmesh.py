import json
from math import sqrt

from compas.datastructures.mesh import Mesh
from compas.datastructures.volmesh.exceptions import VolMeshError

from compas.geometry import centroid_points


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


def center_of_mass(edges, sqrt=sqrt):
    L  = 0
    cx = 0
    cy = 0
    cz = 0
    for sp, ep in edges:
        l   = sqrt(sum((sp[axis] - ep[axis]) ** 2 for axis in range(3)))
        cx += l * 0.5 * (sp[0] + ep[0])
        cy += l * 0.5 * (sp[1] + ep[1])
        cz += l * 0.5 * (sp[2] + ep[2])
        L  += l
    cx = cx / L
    cy = cy / L
    cz = cz / L
    return cx, cy, cz


class VolMesh(object):
    """Class for working with volumetric meshes.

    Volumetric meshes are 3-mainfold, cellular structures.

    The implementation of ``VolMesh`` is based on the notion of *x-maps* [xmaps]
    and the concepts behind the *OpenVolumeMesh* library [ovm].
    In short, we add an additional entity compared to polygonal meshes,
    the *cell*, and relate cells not through *half-edges*, but *half-planes*.

    References:
        .. [xmaps] xxx
        .. [ovm] `Open Volum Mesh <http://www.openvolumemesh.org>`_
    """

    default_vertex_attributes = {}

    def __init__(self):
        self.attributes = {
            'name'                : 'VolMesh',
            'color.vertex'        : (255, 255, 255),
            'color.edge'          : (0, 0, 0),
            'color.face'          : (200, 200, 200),
            'color.normal:vertex' : (0, 255, 0),
            'color.normal:face'   : (0, 255, 0),
        }
        self.vertex = {}
        self.plane = {}
        self.halfface = {}
        self.cell = {}
        self.edge = {}
        self._vkey = 0
        self._fkey = 0
        self._ckey = 0

    # --------------------------------------------------------------------------
    # descriptors
    # --------------------------------------------------------------------------

    def __contains__(self, key):
        return key in self.vertex

    def __len__(self):
        return len(self.vertex)

    def __iter__(self):
        return iter(self.vertex)

    def __getitem__(self, key):
        return self.vertex[key]

    def __str__(self):
        """"""
        print(self.name)

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

    @property
    def data(self):
        """The data representing the mesh."""
        return {
            'attributes': self.attributes,
            'vertex'    : self.vertex,
            'plane'     : self.plane,
            'halfface'  : self.halfface,
            'cell'      : self.cell,
            'edge'      : self.edge,
            '_vkey'     : self._vkey,
            '_fkey'     : self._fkey,
            '_ckey'     : self._ckey,
        }

    @data.setter
    def data(self, data):
        """"""
        attributes = data.get('attributes', None) or {}
        vertex     = data.get('vertex', None) or {}
        plane      = data.get('plane', None) or {}
        halfface   = data.get('halfface', None) or {}
        cell       = data.get('cell', None) or {}
        edge       = data.get('edge', None) or {}
        _vkey      = data.get('_vkey', None) or 0
        _fkey      = data.get('_fkey', None) or 0
        _ckey      = data.get('_ckey', None) or 0
        self.attributes = attributes
        self.vertex     = vertex
        self.plane      = plane
        self.halfface   = halfface
        self.cell       = cell
        self.edge       = edge
        self._vkey      = _vkey
        self._fkey      = _fkey
        self._ckey      = _ckey

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_vertices_and_cells(cls, vertices, cells):
        mesh = cls()
        for x, y, z in vertices:
            mesh.add_vertex(x=x, y=y, z=z)
        for halffaces in cells:
            mesh.add_cell(halffaces)
        return mesh

    @classmethod
    def from_vertices_and_edges(cls, vertices, edges):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data):
        volmesh = cls()
        volmesh.data = data
        return volmesh

    @classmethod
    def from_json(cls, filepath):
        volmesh = cls()
        data = None
        with open(filepath, 'rb') as fp:
            data = json.load(fp)
        if data:
            volmesh.data = data
        return volmesh

    @classmethod
    def from_obj(cls, filepath):
        # the obj should specify vertices and faces
        # and cells by grouping faces
        # note that the faces may or may not be halffaces
        #
        # waht about detecting cells?
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # special
    # --------------------------------------------------------------------------

    def dual(self, cls):
        network = cls()
        for ckey in self.cell:
            x, y, z = self.cell_center(ckey)
            network.add_vertex(key=ckey, x=x, y=y, z=z)
            for nbr in self.cell_neighbours(ckey):
                if nbr in network.edge[ckey]:
                    continue
                if nbr in network.edge and ckey in network.edge[nbr]:
                    continue
                network.add_edge(ckey, nbr)
        return network

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_data(self):
        return self.data

    def to_json(self, filepath):
        with open(filepath, 'wb+') as fp:
            json.dump(self.data, fp)

    def to_obj(self, filepath):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    # vkey should be compatible with int
    # a mesh is a geometrical data structure
    # random keys do not make sense
    def add_vertex(self, vkey=None, attr_dict=None, **kwattr):
        attr = {}
        if attr_dict:
            attr.update(attr_dict)
        attr.update(kwattr)
        if vkey is None:
            vkey = self._vkey
        else:
            if int(vkey) > self._vkey:
                self._vkey = int(vkey)
        self._vkey += 1
        vkey = str(vkey)
        if vkey not in self.vertex:
            self.vertex[vkey] = attr
            self.plane[vkey] = {}
            self.edge[vkey] = {}
        else:
            self.vertex[vkey].update(attr)
        return vkey

    def add_halfface(self, vertices, fkey=None):
        if vertices[0] == vertices[-1]:
            vertices = vertices[:-1]
        if vertices[-2] == vertices[-1]:
            vertices = vertices[:-1]
        if len(vertices) < 3:
            raise VolMeshError('Corrupt halfface.')
        if fkey is None:
            fkey = self._fkey
        else:
            if int(fkey) > self._fkey:
                self._fkey = int(fkey)
        self._fkey += 1
        fkey = str(fkey)
        self.halfface[fkey] = {}
        for i in range(-2, len(vertices) - 2):
            u = str(vertices[i])
            v = str(vertices[i + 1])
            w = str(vertices[i + 2])
            self.add_vertex(vkey=u)
            self.add_vertex(vkey=v)
            self.add_vertex(vkey=w)
            self.halfface[fkey][u] = v
            self.halfface[fkey][v] = w
            if v not in self.plane[u]:
                self.plane[u][v] = {}
            self.plane[u][v][w] = None
            if v not in self.plane[w]:
                self.plane[w][v] = {}
            if u not in self.plane[w][v]:
                self.plane[w][v][u] = None
            if v not in self.edge[u] and u not in self.edge[v]:
                self.edge[u][v] = {}
            if w not in self.edge[v] and v not in self.edge[w]:
                self.edge[v][w] = {}
        u = str(vertices[-1])
        v = str(vertices[0])
        if v not in self.edge[u] and u not in self.edge[v]:
            self.edge[u][v] = {}
        return fkey

    def add_cell(self, halffaces, ckey=None):
        if ckey is None:
            ckey = self._ckey
        else:
            if int(ckey) > self._ckey:
                self._ckey = int(ckey)
        self._ckey += 1
        ckey = str(ckey)
        self.cell[ckey] = {}
        for vertices in halffaces:
            fkey = self.add_halfface(vertices)
            for u in self.halfface[fkey]:
                v = self.halfface[fkey][u]
                w = self.halfface[fkey][v]
                if u not in self.cell[ckey]:
                    self.cell[ckey][u] = {}
                self.cell[ckey][u][v] = fkey
                self.plane[u][v][w] = ckey
        return ckey

    # --------------------------------------------------------------------------
    # lists and iterators
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        return list(self.vertices_iter(data=data))

    def vertices_iter(self, data=False):
        for key in self.vertex:
            if data:
                yield key, self.vertex[key]
            else:
                yield key

    def vertices_enum(self, data=False):
        return enumerate(self.vertices_iter(data=data))

    def cells(self, data=False):
        return list(self.cells_iter(data=data))

    def cells_iter(self, data=False):
        for ckey in self.cell:
            if data:
                raise NotImplementedError
                # data should be stored on the dual network
                # yield ckey, self.cell[ckey]
            else:
                yield ckey

    def cells_enum(self, data=False):
        return enumerate(self.cells_iter(data=data))

    def planes(self):
        raise NotImplementedError

    def planes_iter(self):
        raise NotImplementedError

    def edges(self, data=False):
        return list(self.edges_iter(data))

    def edges_iter(self, data=False):
        for u in self.edge:
            for v in self.edge[u]:
                if data:
                    yield u, v, self.edge[u][v]
                else:
                    yield u, v

    def edges_enum(self, data=False):
        return enumerate(self.edges_iter(data=data))

    # --------------------------------------------------------------------------
    # special purpose
    # --------------------------------------------------------------------------

    def faces(self):
        faces = []
        seen = set()
        for ckey in self.cell:
            for fkey in self.cell_halffaces(ckey):
                vertices = self.halfface_vertices(fkey, ordered=True)
                vset = frozenset(vertices)
                if vset not in seen:
                    faces.append(vertices)
                seen.add(vset)
        return faces

    # --------------------------------------------------------------------------
    # topology
    # --------------------------------------------------------------------------

    def vertex_neighbours(self, vkey):
        return self.plane[vkey].keys()

    def cell_neighbours(self, ckey):
        nbrs = []
        for fkey in self.cell_halffaces(ckey):
            u   = self.halfface[fkey].iterkeys().next()
            v   = self.halfface[fkey][u]
            w   = self.halfface[fkey][v]
            nbr = self.plane[w][v][u]
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def cell_vertex_neighbours(self, ckey):
        raise NotImplementedError

    def halfface_cell(self, fkey):
        u = self.halfface[fkey].iterkeys().next()
        v = self.halfface[fkey][u]
        w = self.halfface[fkey][v]
        return self.plane[u][v][w]

    def halfface_vertices(self, fkey, ordered=False):
        if not ordered:
            return self.halfface[fkey].keys()
        u = self.halfface[fkey].iterkeys().next()
        vertices = [u]
        while True:
            u = self.halfface[fkey][u]
            if u == vertices[0]:
                break
            vertices.append(u)
        return vertices

    def halfface_edges(self, fkey):
        vertices = self.halfface_vertices(fkey, ordered=True)
        edges = []
        for i in range(-1, len(vertices) - 1):
            edges.append((vertices[i], vertices[i + 1]))
        return edges

    def halfface_adjacency(self, ckey):
        raise NotImplementedError

    def cell_halffaces(self, ckey):
        halffaces = set()
        for u in self.cell[ckey]:
            for v in self.cell[ckey][u]:
                fkey = self.cell[ckey][u][v]
                halffaces.add(fkey)
        return list(halffaces)

    def cell_vertices(self, ckey):
        return list(set([vkey for fkey in self.cell_halffaces(ckey) for vkey in self.halfface_vertices(fkey)]))

    def cell_edges(self, ckey):
        halfedges = []
        for fkey in self.cell_halffaces(ckey):
            halfedges += self.halfface_edges(fkey)
        edges = set(frozenset(uv) for uv in halfedges)
        return map(list, edges)

    def cell_vertices_and_halffaces(self, ckey):
        vkeys = self.cell_vertices(ckey)
        fkeys = self.cell_halffaces(ckey)
        vkey_vindex = dict((vkey, index) for index, vkey in enumerate(vkeys))
        vertices = [self.vertex_coordinates(vkey) for vkey in vkeys]
        halffaces = [[vkey_vindex[vkey] for vkey in self.halfface_vertices(fkey, ordered=True)] for fkey in fkeys]
        return vertices, halffaces

    def cell_adjacency(self):
        raise NotImplementedError
        # adjacency = {}
        # for fkey in self.cell_faces(ckey):
        #     neighbours = []
        #     for u, v in self.face[fkey].iteritems():
        #         for test in self.face:
        #             if test == fkey:
        #                 continue
        #             if u in self.face[test]:
        #                 if v == self.face[test][u]:
        #                     neighbours.append(test)
        #                     break
        #             if v in self.face[test]:
        #                 if u == self.face[test][v]:
        #                     neighbours.append(test)
        #                     break
        #     adjacency[fkey] = neighbours
        # return adjacency

    def cell_tree(self, root):
        raise NotImplementedError

    def cell_mesh(self, ckey):
        vertices, halffaces = self.cell_vertices_and_halffaces(ckey)
        return Mesh.from_vertices_and_faces(vertices, halffaces)

    # --------------------------------------------------------------------------
    # geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, vkey, axes='xyz'):
        attr = self.vertex[vkey]
        return [attr[axis] for axis in axes]

    def edge_coordinates(self, u, v, axes='xyz'):
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def face_coordinates(self, fkey, axes='xyz'):
        raise NotImplementedError

    def cell_centroid(self, ckey):
        vkeys = self.cell_vertices(ckey)
        return centroid_points([self.vertex_coordinates(vkey) for vkey in vkeys])

    def cell_center(self, ckey):
        edges = self.cell_edges(ckey)
        return center_of_mass_polyhedron([(self.vertex_coordinates(u), self.vertex_coordinates(v)) for u, v in edges])

    # --------------------------------------------------------------------------
    # geometric operations
    # --------------------------------------------------------------------------

    def scale(self, factor=1.0):
        for key in self.vertex:
            attr = self.vertex[key]
            attr['x'] *= factor
            attr['y'] *= factor
            attr['z'] *= factor

    # --------------------------------------------------------------------------
    # attributes
    # --------------------------------------------------------------------------

    def set_vertex_attributes(self, vkey, attr_dict=None, **kwargs):
        attr = attr_dict or {}
        attr.update(kwargs)
        self.vertex[vkey].update(attr)

    def get_vertex_attributes(self, vkey, attr_dict=None, **kwargs):
        attr = attr_dict or {}
        attr.update(kwargs)
        if not attr:
            return self.vertex[vkey]
        data = {}
        for name, value in attr.items():
            data[name] = self.vertex[vkey].get(name, value)
        return data

    def set_edge_attributes(self, u, v, attr_dict=None, **kwargs):
        attr = attr_dict or {}
        attr.update(kwargs)
        self.edge[u][v].update(attr)

    def get_edge_attributes(self, u, v, attr_dict=None, **kwargs):
        attr = attr_dict or {}
        attr.update(kwargs)
        if not attr:
            return self.edge[u][v]
        data = {}
        for name, value in attr.items():
            data[name] = self.edge[u][v].get(name, value)
        return data


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    #         18------19
    #       16------17|
    #        |      | |
    #   5----|-4----|-11-----15
    # 6------7------10-----14|
    # | |    | |    | |    | |
    # | 3----|-2----|-9----|-13
    # 0------1------8------12

    import compas
    from viewer import VolMeshViewer
    # from compas.viewers import NetworkViewer

    # c1 = [[0, 3, 2, 1],
    #       [0, 1, 7, 6],
    #       [0, 6, 5, 3],
    #       [4, 2, 3, 5],
    #       [4, 7, 1, 2],
    #       [4, 5, 6, 7]]
    # c2 = [[2, 1, 7, 4],
    #       [2, 9, 8, 1],
    #       [8, 9, 11, 10],
    #       [4, 7, 10, 11],
    #       [7, 1, 8, 10],
    #       [4, 11, 9, 2]]
    # c3 = [[10, 11, 9, 8],
    #       [9, 13, 12, 8],
    #       [12, 13, 15, 14],
    #       [10, 14, 15, 11],
    #       [10, 8, 12, 14],
    #       [11, 15, 13, 9]]
    # c4 = [[16, 17, 19, 18],
    #       [4, 18, 19, 11],
    #       [16, 7, 10, 17],
    #       [16, 18, 4, 7],
    #       [19, 17, 10, 11],
    #       [4, 11, 10, 7]]

    # vertices = [[0, 0, 0],
    #             [1, 0, 0],
    #             [1, 1, 0],
    #             [0, 1, 0],
    #             [1, 1, 1],
    #             [0, 1, 1],
    #             [0, 0, 1],
    #             [1, 0, 1],
    #             [2, 0, 0],
    #             [2, 1, 0],
    #             [2, 0, 1],
    #             [2, 1, b1],
    #             [3, 0, 0],
    #             [3, 1, 0],
    #             [3, 0, 1],
    #             [3, 1, 1],
    #             [1, 0, 2],
    #             [2, 0, 2],
    #             [1, 1, 2],
    #             [2, 1, 2]]

    # cells = [c1, c2, c3, c4]

    # mesh = VolMesh.from_vertices_and_cells(vertices, cells)

    # print mesh.edges()
    # print len(mesh.edges())

    # print mesh.vertex_neighbours('10')
    # print mesh.cell_neighbours('0')
    # print mesh.cell_vertices('0')

    # for fkey in mesh.cell_halffaces('0'):
    #     print mesh.halfface_vertices(fkey, True)

    # for ckey in mesh.cell:
    #     cell = mesh.cell_mesh(ckey)
    #     print cell

    mesh = VolMesh.from_json(compas.get_data('boxes.json'))

    print(mesh.name)

    mesh.scale(0.1)

    viewer = VolMeshViewer(mesh, 600, 600, grid_on=False, zoom=5.)

    viewer.grid_on = False
    viewer.axes_on = False

    viewer.axes.x_color = (0.1, 0.1, 0.1)
    viewer.axes.y_color = (0.1, 0.1, 0.1)
    viewer.axes.z_color = (0.1, 0.1, 0.1)

    viewer.setup()
    viewer.show()

    # dual = mesh.dual()

    # viewer = NetworkViewer(dual, 600, 600)
    # viewer.grid_on = True
    # viewer.setup()
    # viewer.show()
