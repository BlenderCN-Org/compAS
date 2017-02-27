from math import cos
from math import pi

from compas.datastructures.mesh.operations import split_edge_mesh

from compas.exceptions import BRGMeshError
from compas.exceptions import BRGMeshAlgorithmError


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'subdivide_mesh',
    'subdivide_mesh_tri',
    'subdivide_mesh_corner',
    # 'subdivide_mesh_quad',
    'subdivide_mesh_catmullclark',
    'subdivide_mesh_doosabin',
    'subdivide_trimesh_loop',
]


# distinguish between subd of meshes with and without boundary
# closed vs. open
# pay attention to extraordinary points
# and to special rules on boundaries
# interpolation vs. approxmation?!
# add numerical versions to compas.datastructures.mesh.(algorithms.)numerical
# investigate meaning and definition of limit surface
# any subd algorithm should return a new subd mesh, leaving the control mesh intact

def subdivide_mesh(mesh, scheme='tri', **options):
    """Subdivide the input mesh.

    Parameters:
        mesh (Mesh) : A mesh object.
        scheme (str) : Optional.
            The scheme according to which the mesh should be subdivided.
            Defult is 'tri'. Supported values are:

            * catmullclark : catmull-clark subdivision.
            * doosabin : doo-sabin subdivision.

        options (kwargs) : Optional additional keyword arguments.

    Raises:
        NotImplementedError
        MeshError

    """
    options = options or {}
    # if scheme == 'tri':
    #     return subdivide_mesh_tri(mesh)
    # if scheme == 'corner':
    #     return subdivide_mesh_corner(mesh)
    # if scheme == 'quad':
    #     return subdivide_mesh_quad(mesh)
    if scheme == 'catmullclark':
        return subdivide_mesh_catmullclark(mesh, **options)
    if scheme == 'doosabin':
        return subdivide_mesh_doosabin(mesh, **options)
    raise NotImplementedError


def subdivide_mesh_tri(mesh):
    """"""
    for fkey in mesh.faces():
        mesh.insert_vertex(fkey)


# this is actually loop-subd
# however, corner cutting is a valid technique and should be added
# 'real' loop subd only works on tri meshes
def subdivide_mesh_corner(mesh):
    """"""
    # split every edge
    edgepoints = []
    for u, v in mesh.edges():
        w = split_edge_mesh(mesh, u, v, allow_boundary=True)
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
            raise BRGMeshError
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


# def subdivide_mesh_quad(mesh):
#     """"""
#     # keep a copy of the faces before splitting the edges
#     fkey_vertices = dict((fkey, mesh.face_vertices(fkey, ordered=True)) for fkey in mesh.face)
#     # split every edge
#     ekeys = []
#     for u, v in mesh.edges():
#         w = split_edge_mesh(mesh, u, v, allow_boundary=True)
#         ekeys.append(w)
#     # insert a vertex at the centroid of every face
#     # create a new face for every vertex of the old faces
#     # [a (from split), key, d (from split), centroid]
#     for fkey in mesh.faces():
#         x, y, z = mesh.face_centroid(fkey)
#         c = mesh.add_vertex(x=x, y=y, z=z)
#         for key in fkey_vertices[fkey]:
#             rface = dict((j, i) for i, j in mesh.face[fkey].items())
#             a = rface[key]
#             d = mesh.face[fkey][key]
#             mesh.add_face([a, key, d, c])
#         del mesh.face[fkey]
#     return ekeys


def subdivide_mesh_catmullclark(mesh, k=1, fixed=None):
    """Subdivide a mesh using the Catmull-Clark algorithm.

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

    subd = mesh.copy()

    for _ in range(k):
        # keep track of original connectivity and vertex locations
        bkeys           = set(subd.vertices_on_boundary())
        bkey_edgepoints = {}
        keys            = subd.vertices()
        key_fkeys       = dict((key, subd.vertex_faces(key)) for key in keys)
        fkey_vertices   = dict((fkey, subd.face_vertices(fkey, ordered=True)) for fkey in subd.faces())
        fkey_centroid   = dict((fkey, subd.face_centroid(fkey)) for fkey in subd.face)

        # apply quad subdivision scheme
        # keep track of the created edge points that are not on the boundary
        # keep track track of the new edge points on the boundary
        # and their relation to the previous boundary points
        edgepoints = []

        for u, v in subd.edges():

            w = split_edge_mesh(subd, u, v, allow_boundary=True)

            if u in bkeys and v in bkeys:
                if u not in bkey_edgepoints:
                    bkey_edgepoints[u] = []
                if v not in bkey_edgepoints:
                    bkey_edgepoints[v] = []

                bkey_edgepoints[u].append(w)
                bkey_edgepoints[v].append(w)
                continue

            edgepoints.append(w)

        for fkey in subd.faces():
            x, y, z = fkey_centroid[fkey]
            c = subd.add_vertex(x=x, y=y, z=z)
            for key in fkey_vertices[fkey]:
                rface = dict((j, i) for i, j in subd.face[fkey].items())
                a = rface[key]
                d = subd.face[fkey][key]
                subd.add_face([a, key, d, c])
            del subd.face[fkey]

        # these are the coordinates before updating
        key_xyz = dict((key, subd.vertex_coordinates(key)) for key in subd.vertex)

        # move each edge point to the average of the neighbouring centroids and
        # the original end points

        for w in edgepoints:
            nbrs = [key_xyz[nbr] for nbr in subd.halfedge[w]]
            # move w to the average of its neighbours
            x, y, z = average(nbrs)
            subd.vertex[w]['x'] = x
            subd.vertex[w]['y'] = y
            subd.vertex[w]['z'] = z

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
                nbrs = [key_xyz[nbr] for nbr in subd.halfedge[key]]
                n = len(nbrs)
                n = float(len(nbrs))
                f = 1. / n
                e = 2. / n
                v = (n - 3.) / n
                F = [coord * f for coord in average(fnbrs)]
                E = [coord * e for coord in average(nbrs)]
                V = [coord * v for coord in key_xyz[key]]
                x, y, z = [F[_] + E[_] + V[_] for _ in range(3)]

            subd.vertex[key]['x'] = x
            subd.vertex[key]['y'] = y
            subd.vertex[key]['z'] = z

    return subd


# def _subdivide_mesh_catmullclark(mesh, k=1, fixed=None):
#     """"""

#     if not fixed:
#         fixed = []

#     fixed = set(fixed)
#     subd = mesh.copy()

#     for level in range(k):

#         ekeys = subdivide_mesh_quad(subd)

#         key_xyz = dict((key, subd.vertex_coordinates(key)) for key in subd)

#         for ekey in ekeys:
#             nbrs = [key_xyz[nbr] for nbr in subd.halfedge[ekey]]
#             xyz  = [axis / 4. for axis in map(sum, zip(*nbrs))]
#             subd.vertex[ekey]['x'] = xyz[0]
#             subd.vertex[ekey]['y'] = xyz[1]
#             subd.vertex[ekey]['z'] = xyz[2]

#         for key in subd.vertices_iter():
#             epoints = []
#             fpoints = []

#             for enbr in subd.halfedge[key]:
#                 fkey = subd.halfedge[key][enbr]
#                 fnbr = subd.face[fkey][enbr]
#                 epoints.append(key_xyz[enbr])
#                 fpoints.append(key_xyz[fnbr])

#             n = float(len(epoints))
#             E = [axis / n for axis in map(sum, zip(*epoints))]
#             F = [axis / n for axis in map(sum, zip(*fpoints))]
#             V = key_xyz[key]
#             e = 2. / n
#             f = 1. / n
#             v = (n - 3.) / n
#             xyz = [e * E[i] + f * F[i] + v * V[i] for i in range(3)]
#             subd.vertex[key]['x'] = xyz[0]
#             subd.vertex[key]['y'] = xyz[1]
#             subd.vertex[key]['z'] = xyz[2]

#     return subd


def subdivide_mesh_doosabin(mesh, k=1, fixed=None):
    """"""
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


def subdivide_trimesh_loop(mesh, k=1, fixed=None):
    """Subdivide a triangle mesh using the Loop algorithm.

    Examples:

        >>> from compas.datastructures.mesh.mesh import Mesh
        >>> from compas.geometry.polyhedron import Polyhedron
        >>> from compas.datastructures.mesh.algorithms.orientation import mesh_flip_cycle_directions
        >>> from compas.datastructures.mesh.viewer import SubdMeshViewer

        >>> tet = Polyhedron.generate(4)

        >>> mesh = Mesh.from_vertices_and_faces(tet.vertices, tet.faces)
        >>> mesh_flip_cycle_directions(mesh)

        >>> viewer = SubdMeshViewer(mesh, subdfunc=loop_subdivision, width=600, height=600)

        >>> viewer.axes.x_color = (0.1, 0.1, 0.1)
        >>> viewer.axes.y_color = (0.1, 0.1, 0.1)
        >>> viewer.axes.z_color = (0.1, 0.1, 0.1)

        >>> viewer.axes_on = False
        >>> viewer.grid_on = False

        >>> for _ in range(20):
        ...    viewer.camera.zoom_in()

        >>> viewer.setup()
        >>> viewer.show()

    """
    if not fixed:
        fixed = []

    fixed = set(fixed)
    subd = mesh.copy()

    for _ in range(k):
        key_xyz       = {key: subd.vertex_coordinates(key) for key in subd}
        fkey_vertices = {fkey: subd.face_vertices(fkey, ordered=True) for fkey in subd.face}
        uv_w          = {(u, v): subd.face[subd.halfedge[u][v]][v] for u in subd.halfedge for v in subd.halfedge[u]}
        edgepoints    = {}

        for key in subd:
            nbrs = subd.vertex_neighbours(key)
            n = len(nbrs)

            if n == 3:
                a = 3. / 16.
            else:
                a = (5. / 8. - (3. / 8. + 0.25 * cos(2 * pi / n)) ** 2) / n

            nbrs = [key_xyz[nbr] for nbr in nbrs]
            nbrs = [sum(axis) for axis in zip(*nbrs)]
            xyz = key_xyz[key]
            xyz = [(1. - n * a) * xyz[i] + a * nbrs[i] for i in range(3)]
            subd.vertex[key]['x'] = xyz[0]
            subd.vertex[key]['y'] = xyz[1]
            subd.vertex[key]['z'] = xyz[2]

        for u, v in subd.edges():
            w = split_edge_mesh(subd, u, v)
            edgepoints[(u, v)] = w
            edgepoints[(v, u)] = w
            v1 = key_xyz[u]
            v2 = key_xyz[v]
            vl = key_xyz[uv_w[(u, v)]]
            vr = key_xyz[uv_w[(v, u)]]
            xyz = [3. * (v1[i] + v2[i]) / 8. + (vl[i] + vr[i]) / 8. for i in range(3)]
            subd.vertex[w]['x'] = xyz[0]
            subd.vertex[w]['y'] = xyz[1]
            subd.vertex[w]['z'] = xyz[2]

        for fkey, vertices in fkey_vertices.items():
            u, v, w = vertices
            uv = edgepoints[(u, v)]
            vw = edgepoints[(v, w)]
            wu = edgepoints[(w, u)]
            subd.add_face([wu, u, uv])
            subd.add_face([uv, v, vw])
            subd.add_face([vw, w, wu])
            subd.add_face([uv, vw, wu])
            del subd.face[fkey]

    return subd


# this was used as a basis for the implementation of doo-sabin
# and the update of catmull-clark
# don't use this for anything other then an example...
# this implementation assumes the mesh is closed
# when extraordinary vertices exist in the control mesh, any subd mesh has gas faces with more than 4 vertices
def subdivide_quadmesh_quad(mesh, k=1):
    """Subdivide a quad mesh using the quad algorithm.

    Examples:

        >>> from compas.datastructures.mesh.quad import QuadMesh
        >>> from compas.geometry.polyhedron import Polyhedron

        >>> cube = Polyhedron.generate(6)

        >>> quad = QuadMesh.from_vertices_and_faces(cube.vertices, cube.faces)
        >>> quad = quad_subdivision(quad)

        >>> quad.draw()

    """
    c1 = 3. / 16.
    c2 = 9. / 16.
    c3 = 3. / 16.
    c4 = 1. / 16.

    cls = type(mesh)

    for _ in range(k):
        old_xyz = dict((key, mesh.vertex_coordinates(key)) for key in mesh)
        fkey_old_new = dict((fkey, {}) for fkey in mesh.face)
        subd = cls()

        for fkey in mesh.face:
            vertices = mesh.face_vertices(fkey, ordered=True)
            if len(vertices) != 4:
                raise BRGMeshAlgorithmError
            o1 = old_xyz[vertices[0]]
            o2 = old_xyz[vertices[1]]
            o3 = old_xyz[vertices[2]]
            o4 = old_xyz[vertices[3]]
            n1 = [c1 * o4[i] + c2 * o1[i] + c3 * o2[i] + c4 * o3[i] for i in range(3)]
            n2 = [c1 * o1[i] + c2 * o2[i] + c3 * o3[i] + c4 * o4[i] for i in range(3)]
            n3 = [c1 * o2[i] + c2 * o3[i] + c3 * o4[i] + c4 * o1[i] for i in range(3)]
            n4 = [c1 * o3[i] + c2 * o4[i] + c3 * o1[i] + c4 * o2[i] for i in range(3)]
            a = subd.add_vertex(x=n1[0], y=n1[1], z=n1[2])
            b = subd.add_vertex(x=n2[0], y=n2[1], z=n2[2])
            c = subd.add_vertex(x=n3[0], y=n3[1], z=n3[2])
            d = subd.add_vertex(x=n4[0], y=n4[1], z=n4[2])
            fkey_old_new[fkey][vertices[0]] = a
            fkey_old_new[fkey][vertices[1]] = b
            fkey_old_new[fkey][vertices[2]] = c
            fkey_old_new[fkey][vertices[3]] = d

        for fkey in mesh.face:
            if len(vertices) != 4:
                raise BRGMeshAlgorithmError
            vertices = mesh.face_vertices(fkey, ordered=True)
            old_new = fkey_old_new[fkey]
            subd.add_face([old_new[old] for old in vertices])

        for key in mesh.vertex:
            if mesh.is_vertex_on_boundary(key):
                continue
            face = []
            for nbr in mesh.vertex_neighbours(key, ordered=True):
                fkey = mesh.halfedge[key][nbr]
                if fkey is not None:
                    face.append(fkey_old_new[fkey][key])
            if len(face) > 2:
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

    import compas

    from compas.datastructures.mesh import Mesh

    from compas.geometry.elements.polyhedron import Polyhedron
    from compas.datastructures.mesh.viewer import SubdMeshViewer

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    subd = subdivide_mesh_doosabin(mesh, k=2)

    subd.plot(vertexsize=0.05, vertexcolor={key: (255, 0, 0) for key in mesh})

    # cube = Polyhedron.generate(6)

    # mesh = Mesh.from_vertices_and_faces(cube.vertices, cube.faces)

    # viewer = SubdMeshViewer(mesh, subdfunc=subdivide_mesh_catmullclark, width=600, height=600)

    # viewer.axes.x_color = (0.1, 0.1, 0.1)
    # viewer.axes.y_color = (0.1, 0.1, 0.1)
    # viewer.axes.z_color = (0.1, 0.1, 0.1)

    # viewer.axes_on = False
    # viewer.grid_on = False

    # viewer.setup()
    # viewer.show()
