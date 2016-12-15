""""""

__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


def split_edge(mesh, u, v, t=0.5, allow_boundary=False, interpolate_attr=False):
    """"""
    if t <= 0.0:
        raise ValueError('t should be greater than 0.0.')
    if t >= 1.0:
        raise ValueError('t should be smaller than 1.0.')
    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]
    if not allow_boundary:
        if fkey_uv is None or fkey_vu is None:
            return
    # coordinates
    sp = mesh.vertex_coordinates(u)
    ep = mesh.vertex_coordinates(v)
    vec = [ep[i] - sp[i] for i in range(3)]
    x, y, z = [sp[i] + t * vec[i] for i in range(3)]
    # the split vertex
    w = mesh.add_vertex(x=x, y=y, z=z)
    # the UV face
    if fkey_uv is None:
        mesh.halfedge[u][w] = None
        mesh.halfedge[w][v] = None
        del mesh.halfedge[u][v]
    else:
        o = mesh.face[fkey_uv][v]
        mesh.add_face([u, w, o])
        mesh.add_face([w, v, o])
        del mesh.halfedge[u][v]
        del mesh.face[fkey_uv]
    # the VU face
    if fkey_vu is None:
        mesh.halfedge[v][w] = None
        mesh.halfedge[w][u] = None
        del mesh.halfedge[v][u]
    else:
        o = mesh.face[fkey_vu][u]
        mesh.add_face([v, w, o])
        mesh.add_face([w, u, o])
        del mesh.halfedge[v][u]
        del mesh.face[fkey_vu]
    # return the key of the split vertex
    return w
