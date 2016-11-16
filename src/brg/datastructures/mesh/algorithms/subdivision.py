""""""

from math import cos
from math import pi

from brg.datastructures.mesh.operations.split import split_edge
from brg.datastructures.mesh.exceptions import MeshError


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


# distinguish between subd of meshes with and without boundary
# closed vs. open
# pay attention to extraordinary points
# and to special rules on boundaries
# interpolation vs. approxmation?!
# add numerical versions to brg.datastructures.mesh.(algorithms.)numerical
# investigate meaning and definition of limit surface
# any subd algorithm should return a new subd mesh, leaving the control mesh intact
def subdivide(mesh, scheme='tri', **options):
    """Subdivide the input mesh.

    Parameters:
        mesh (Mesh) : A mesh object.
        scheme (str) : Optional. The scheme according to which the mesh should be
            subdivided. Defult is 'tri'. Supported values are:

                - tri : subdivide every face into triangles by connecting its
                  vertices to the face centre
                - corner : split the edges and replace each face by a face connecting
                  the midpoints and a face per corner connecting adjacent midpoints.
                - quad : form new faces by connecting edge midpoints to the
                  face centres.
                - catmull-clark : catmull-clark subdivision.
                - doo-sabin : doo-sabin subdivision.
        options (kwargs) : Optional additional keyword arguments.

    Returns:
        None

    Raises:
        NotImplementedError
        MeshError
    """
    options = options or {}
    if scheme == 'tri':
        return tri_subdivision(mesh)
    if scheme == 'corner':
        return corner_subdivision(mesh)
    if scheme == 'quad':
        return quad_subdivision(mesh)
    if scheme == 'catmullclark':
        return _catmullclark_subdivision(mesh, **options)
    if scheme == 'doosabin':
        return doosabin_subdivision(mesh, **options)
    raise NotImplementedError


def subdivided(mesh):
    """Return a subdivided mesh."""
    pass


def tri_subdivision(mesh):
    """"""
    for fkey in mesh.faces():
        mesh.insert_vertex(fkey)


# this is actually loop-subd
# however, corner cutting is a valid technique and should be added
# 'real' loop subd only works on tri meshes
# it should be added explicitely there
def corner_subdivision(mesh):
    """"""
    # split every edge
    edgepoints = []
    for u, v in mesh.edges():
        w = split_edge(mesh, u, v, allow_boundary=True)
        edgepoints.append(w)
    edgepoints = set(edgepoints)
    # create 4 new faces for every old face
    for fkey in mesh.faces():
        cycle = mesh.face[fkey]
        vertices = set(cycle)
        start = None
        for key in vertices:
            if key in edgepoints:
                start = key
                break
        if not start:
            raise MeshError
        face = []
        while True:
            a = key
            b = cycle[a]
            c = cycle[b]
            mesh.add_face([a, b, c])
            face.append(a)
            if c == start:
                break
            key = c
        mesh.add_face(face)
        del mesh.face[fkey]


# give this a different name
# see also: brg.datastructures.mesh.algorithms.quad.subdivision.quad_subdivision
def quad_subdivision(mesh):
    """"""
    # keep a copy of the faces before splitting the edges
    fkey_vertices = dict((fkey, mesh.face_vertices(fkey, ordered=True)) for fkey in mesh.face)
    # split every edge
    ekeys = []
    for u, v in mesh.edges():
        w = split_edge(mesh, u, v, allow_boundary=True)
        ekeys.append(w)
    # insert a vertex at the centroid of every face
    # create a new face for every vertex of the old faces
    # [a (from split), key, d (from split), centroid]
    for fkey in mesh.faces():
        x, y, z = mesh.face_centroid(fkey)
        c = mesh.add_vertex(x=x, y=y, z=z)
        for key in fkey_vertices[fkey]:
            rface = dict((j, i) for i, j in mesh.face[fkey].items())
            a = rface[key]
            d = mesh.face[fkey][key]
            mesh.add_face([a, key, d, c])
        del mesh.face[fkey]
    return ekeys


def catmullclark_subdivision(mesh, k=1, fixed=None):
    """
    Subdivide a mesh using the Catmull-Clark algorithm.

    Note that *Catmull-Clark* subdivision is like *Quad* subdivision, but with
    smoothing after every level of further subdivision. Smoothing is done
    according to the scheme prescribed by the Catmull-Clark algorithm.

    Parameters:
        mesh (Mesh) : The mesh object that will be subdivided.
        k (int) : Optional. The number of levels of subdivision. Default is `1`.
        fixed (list) : Optional. A list of fixed vertices. Default is `None`.

    Returns:
        None : The given mesh is modified *in place*. No new mesh is created.
    """
    def average(points):
        p = len(points)
        return [coord / p for coord in map(sum, zip(*points))]
    if not fixed:
        fixed = []
    fixed = set(fixed)
    for _ in range(k):
        # keep track of original connectivity and vertex locations
        bkeys           = set(mesh.vertices_on_boundary())
        bkey_edgepoints = {}
        keys            = mesh.vertices()
        key_fkeys       = dict((key, mesh.vertex_faces(key)) for key in keys)
        fkey_vertices   = dict((fkey, mesh.face_vertices(fkey, ordered=True)) for fkey in mesh.faces())
        fkey_centroid   = dict((fkey, mesh.face_centroid(fkey)) for fkey in mesh.face)
        # apply quad subdivision scheme
        # keep track of the created edge points that are not on the boundary
        # keep track track of the new edge points on the boundary
        # and their relation to the previous boundary points
        edgepoints = []
        for u, v in mesh.edges():
            # is_edge_naked?
            w = split_edge(mesh, u, v, allow_boundary=True)
            if u in bkeys and v in bkeys:
                if u not in bkey_edgepoints:
                    bkey_edgepoints[u] = []
                if v not in bkey_edgepoints:
                    bkey_edgepoints[v] = []
                bkey_edgepoints[u].append(w)
                bkey_edgepoints[v].append(w)
                continue
            edgepoints.append(w)
        for fkey in mesh.faces():
            x, y, z = fkey_centroid[fkey]
            c = mesh.add_vertex(x=x, y=y, z=z)
            for key in fkey_vertices[fkey]:
                rface = dict((j, i) for i, j in mesh.face[fkey].items())
                a = rface[key]
                d = mesh.face[fkey][key]
                mesh.add_face([a, key, d, c])
            del mesh.face[fkey]
        # these are the coordinates before updating
        key_xyz = dict((key, mesh.vertex_coordinates(key)) for key in mesh.vertex)
        # move each edge point to the average of the neighbouring centroids and
        # the original end points
        for w in edgepoints:
            nbrs = [key_xyz[nbr] for nbr in mesh.halfedge[w]]
            # move w to the average of its neighbours
            x, y, z = average(nbrs)
            mesh.vertex[w]['x'] = x
            mesh.vertex[w]['y'] = y
            mesh.vertex[w]['z'] = z
        # move each vertex to the weighted average of itself, the neighbouring
        # centroids and the neighbouring mipoints
        for key in keys:
            if key in fixed:
                continue
            if key in bkeys:
                nbrs = bkey_edgepoints[key]
                nbrs = set(nbrs)
                nbrs = [key_xyz[nbr] for nbr in nbrs]
                e = 0.5
                v = 0.5
                E = [coord * e for coord in average(nbrs)]
                V = [coord * v for coord in key_xyz[key]]
                x, y, z = [E[_] + V[_] for _ in range(3)]
            else:
                fnbrs = [fkey_centroid[fkey] for fkey in key_fkeys[key] if fkey is not None]
                nbrs = [key_xyz[nbr] for nbr in mesh.halfedge[key]]
                n = len(nbrs)
                n = float(len(nbrs))
                f = 1. / n
                e = 2. / n
                v = (n - 3.) / n
                F = [coord * f for coord in average(fnbrs)]
                E = [coord * e for coord in average(nbrs)]
                V = [coord * v for coord in key_xyz[key]]
                x, y, z = [F[_] + E[_] + V[_] for _ in range(3)]
            mesh.vertex[key]['x'] = x
            mesh.vertex[key]['y'] = y
            mesh.vertex[key]['z'] = z


def _catmullclark_subdivision(mesh, k=1, fixed=None):
    """"""

    if not fixed:
        fixed = []

    fixed = set(fixed)
    subd = mesh.copy()

    for level in range(k):

        ekeys = quad_subdivision(subd)

        key_xyz = dict((key, subd.vertex_coordinates(key)) for key in subd)

        for ekey in ekeys:
            nbrs = [key_xyz[nbr] for nbr in subd.halfedge[ekey]]
            xyz  = [axis / 4. for axis in map(sum, zip(*nbrs))]
            subd.vertex[ekey]['x'] = xyz[0]
            subd.vertex[ekey]['y'] = xyz[1]
            subd.vertex[ekey]['z'] = xyz[2]

        for key in subd.vertices_iter():
            epoints = []
            fpoints = []
            for enbr in subd.halfedge[key]:
                fkey = subd.halfedge[key][enbr]
                fnbr = subd.face[fkey][enbr]
                epoints.append(key_xyz[enbr])
                fpoints.append(key_xyz[fnbr])
            n = float(len(epoints))
            E = [axis / n for axis in map(sum, zip(*epoints))]
            F = [axis / n for axis in map(sum, zip(*fpoints))]
            V = key_xyz[key]
            e = 2. / n
            f = 1. / n
            v = (n - 3.) / n
            xyz = [e * E[i] + f * F[i] + v * V[i] for i in range(3)]
            subd.vertex[key]['x'] = xyz[0]
            subd.vertex[key]['y'] = xyz[1]
            subd.vertex[key]['z'] = xyz[2]

    return subd


def doosabin_subdivision(mesh, k=1, fixed=None):
    if not fixed:
        fixed = []
    fixed = set(fixed)
    cls = type(mesh)
    for _ in range(k):
        old_xyz  = dict((key, mesh.vertex_coordinates(key)) for key in mesh)
        fkey_old_new = dict((fkey, {}) for fkey in mesh.face)
        subd = cls()
        for fkey in mesh.face:
            vertices = mesh.face_vertices(fkey, ordered=True)
            n = len(vertices)
            _4n = 1. / (4 * n)
            for i in range(n):
                old = vertices[i]
                c = [0, 0, 0]
                for j in range(n):
                    xyz = old_xyz[vertices[j]]
                    if i == j:
                        alpha = _4n * (n + 5)
                    else:
                        alpha = _4n * (3 + 2 * cos(2 * pi * (i - j) / n))
                    c[0] += alpha * xyz[0]
                    c[1] += alpha * xyz[1]
                    c[2] += alpha * xyz[2]
                new = subd.add_vertex(x=c[0], y=c[1], z=c[2])
                fkey_old_new[fkey][old] = new
        for fkey in mesh.face:
            vertices = mesh.face_vertices(fkey, ordered=True)
            old_new = fkey_old_new[fkey]
            subd.add_face([old_new[key] for key in vertices])
        for key in mesh.vertex:
            if mesh.is_vertex_on_boundary(key):
                continue
            face = []
            for nbr in mesh.vertex_neighbours(key, ordered=True):
                fkey = mesh.halfedge[key][nbr]
                if fkey is not None:
                    face.append(fkey_old_new[fkey][key])
            subd.add_face(face[::-1])
        edges = set()
        for u in mesh.halfedge:
            for v in mesh.halfedge[u]:
                if (u, v) in edges:
                    continue
                edges.add((u, v))
                edges.add((v, u))
                uv_fkey = mesh.halfedge[u][v]
                vu_fkey = mesh.halfedge[v][u]
                if uv_fkey is None or vu_fkey is None:
                    continue
                face = []
                face.append(fkey_old_new[uv_fkey][u])
                face.append(fkey_old_new[vu_fkey][u])
                face.append(fkey_old_new[vu_fkey][v])
                face.append(fkey_old_new[uv_fkey][v])
                subd.add_face(face)
        mesh = subd
    return mesh


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from brg.datastructures.mesh.mesh import Mesh
    from brg.geometry.polyhedron import Polyhedron
    from brg.datastructures.mesh.viewer import SubdMeshViewer

    cube = Polyhedron.generate(6)

    mesh = Mesh.from_vertices_and_faces(cube.vertices, cube.faces)

    viewer = SubdMeshViewer(mesh, subdfunc=_catmullclark_subdivision)

    viewer.axes.x_color = (0.1, 0.1, 0.1)
    viewer.axes.y_color = (0.1, 0.1, 0.1)
    viewer.axes.z_color = (0.1, 0.1, 0.1)

    viewer.setup()
    viewer.show()
