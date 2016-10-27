from brg.datastructures.mesh.operations.split import split_edge
from brg.datastructures.mesh.exceptions import MeshError


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


def subdivide(mesh, scheme='t', **options):
    """Subdivide the input mesh.

    Parameters:
        mesh (Mesh) : A mesh object.
        scheme (str) : Optional. The scheme according to which the mesh should be
            subdivided. Defult is 't'. Supported values are:

                - t/tri : subdivide every face into triangles by connecting its
                  vertices to the face centre
                - c/corner : split the edges and replace each face by a face connecting
                  the midpoints and a face per corner connecting adjacent midpoints.
                - q/quad : form new faces by connecting edge midpoints to the
                  face centres.
                - ck/catmull-clark : catmull-clark subdivision.
        options (kwargs) : Optional additional keyword arguments.

    Returns:
        None

    Raises:
        NotImplementedError
        MeshError
    """
    options = options or {}
    if scheme == 'tri':
        tri_subdivision(mesh)
        return
    if scheme == 'corner':
        # TP arity 2 => loop, buttefly
        corner_subdivision(mesh)
        return
    if scheme == 'quad':
        # QP arity 2 => catmull-clark, kobbelt
        quad_subdivision(mesh)
        return
    if scheme == 'catmull-clark':
        catmullclark_subdivision(mesh, **options)
        return
    if scheme == 'doo-sabin':
        # QD arity 2
        return
    if scheme == 'midedge':
        # QD aity sqrt(2)
        return
    if scheme == 'sqrt3':
        # TP arity sqrt(3)
        return
    if scheme == 'four-eight':
        # QP arity sqrt(2)
        return
    # if scheme == 'kobbelt':
    #     return
    # if scheme == 'loop':
    #     return
    # if scheme == 'butterfly':
    #     return
    raise NotImplementedError


def subdivided(mesh):
    """Return a subdivided mesh."""
    pass


def tri_subdivision(mesh):
    """"""
    for fkey in mesh.faces():
        mesh.insert_vertex(fkey)


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


def quad_subdivision(mesh):
    """"""
    # keep a copy of the faces before splitting the edges
    fkey_vertices = dict((fkey, mesh.face_vertices(fkey, ordered=True)) for fkey in mesh.face)
    # split every edge
    for u, v in mesh.edges():
        split_edge(mesh, u, v, allow_boundary=True)
    # insert a vertex at the centroid of every face
    # create a new face for every vertex of the old faces
    # [a (from split), key, d (from split), centroid]
    for fkey in mesh.faces():
        x, y, z = mesh.face_centroid(fkey)
        # ----------------------------------------------------------------------
        # temp
        # ----------------------------------------------------------------------
        attr = {}
        for key in mesh.face_vertices(fkey):
            for name in mesh.vertex[key]:
                attr[name] = None
        # ----------------------------------------------------------------------
        c = mesh.add_vertex(attr_dict=attr, x=x, y=y, z=z)
        for key in fkey_vertices[fkey]:
            rface = dict((j, i) for i, j in mesh.face[fkey].items())
            a = rface[key]
            d = mesh.face[fkey][key]
            mesh.add_face([a, key, d, c])
        del mesh.face[fkey]


def catmullclark_subdivision(mesh, k=1, fixed=None):
    """
    Subdivide a mesh using the Catmull-Clark algorithm.

    Note that *Catmull-Clark* subdivision is like *Quad* subdivision, but with
    smoothing after every level of further subdivision. Smoothing is done
    according to the scheme prescribed by the Catmull-Clark algorithm.

    Parameters
    ----------
    mesh : mesh-like
        The mesh object that will be subdivided.
    k : int, optional [1]
        The number of levels of subdivision.
    fixed : list or keys, optional
        The keys of fixed vertices.

    Returns
    -------
    None
        The given mesh is modified *in place*.
        No new mesh is created.
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
            # ------------------------------------------------------------------
            # temp
            # ------------------------------------------------------------------
            attr = {}
            # count = 0
            # for key in mesh.face_vertices(fkey):
            #     for name in mesh.vertex[key]:
            #         if name not in attr:
            #             attr[name] = 0
            #         try:
            #             attr[name] += mesh.vertex[key][name]
            #         except:
            #             attr[name] = None
            #     count += 1
            # for name in attr:
            #     if attr[name] is not None:
            #         attr[name] = attr[name] / count
            # ------------------------------------------------------------------
            c = mesh.add_vertex(attr_dict=attr, x=x, y=y, z=z)
            # ------------------------------------------------------------------
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
            # ------------------------------------------------------------------
            if key in fixed:
                continue
            # if mesh.vertex[key]['is_fixed']:
            #     continue
            # ------------------------------------------------------------------
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


def doosabin_subdivision(mesh):
    pass


def sqrt3_subdivision(mesh):
    pass


def foureight_subdivision(mesh):
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg
    from brg.datastructures.mesh.mesh import Mesh
    from brg.datastructures.mesh.drawing import draw_mesh

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    subdivide(mesh)

    print mesh

    draw_mesh(mesh)

