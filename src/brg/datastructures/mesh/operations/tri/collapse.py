from brg.geometry.elements.line import Line
from brg.datastructures.mesh.exceptions import MeshError


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2015-12-03 13:43:05'


__all__ = ['collapse_edge', ]


# def collapse_edge(mesh, u, v, t=0.5):
#     """Collapse an edge to its first or second vertex, or to an intermediate
#     point.

#     An edge can only be collapsed if the collapse is `legal`. A collapse is
#     legal if it meets the following requirements:

#         * any vertex `w` that is a neighbour of both `u` and `v` is a face
#           of the mesh
#         * `u` and `v` are not on the boundary
#         * ...

#     See [] for a detailed explanation of these requirements.

#     Parameters:
#         u (str): The first vertex of the (half-) edge.
#         v (str): The second vertex of the (half-) edge.
#         t (float): Determines where to collapse to. If `t == 0.0` collapse
#             to `u`. If `t == 1.0` collapse to `v`. If `0.0 < t < 1.0`,
#             collapse to a point between `u` and `v`.

#     Returns:
#         None

#     Raises:
#         ValueError: If `u` and `v` are not neighbours.
#     """
#     if t < 0.0:
#         raise ValueError('Parameter t should be greater than or equal to 0.')
#     if t > 1.0:
#         raise ValueError('Parameter t should be smaller than or equal to 1.')
#     # conditions
#     # collapsing of boundary vertices is currently not supported
#     # change this to `and` to support collapsing to or from the boundary
#     if mesh.is_vertex_on_boundary(u) or mesh.is_vertex_on_boundary(v):
#         return
#     # check for contained faces
#     for nbr in mesh.halfedge[u]:
#         if nbr in mesh.halfedge[v]:
#             # check if U > V > NBR is a face
#             if (mesh.halfedge[u][v] != mesh.halfedge[v][nbr] or mesh.halfedge[u][v] != mesh.halfedge[nbr][u]):
#                 # check if V > U > NBR is a face
#                 if (mesh.halfedge[v][u] != mesh.halfedge[u][nbr] or mesh.halfedge[v][u] != mesh.halfedge[nbr][v]):
#                     return
#     for nbr in mesh.halfedge[v]:
#         if nbr in mesh.halfedge[u]:
#             # check if U > V > NBR is a face
#             if (mesh.halfedge[u][v] != mesh.halfedge[v][nbr] or mesh.halfedge[u][v] != mesh.halfedge[nbr][u]):
#                 # check if V > U > NBR is a face
#                 if (mesh.halfedge[v][u] != mesh.halfedge[u][nbr] or mesh.halfedge[v][u] != mesh.halfedge[nbr][v]):
#                     return
#     # move U
#     sp = mesh.vertex_coordinates(u)
#     ep = mesh.vertex_coordinates(v)
#     line = Line(sp, ep)
#     line.scale(t)
#     x, y, z = line.end
#     mesh.vertex[u]['x'] = x
#     mesh.vertex[u]['y'] = y
#     mesh.vertex[u]['z'] = z
#     # UV face
#     fkey = mesh.halfedge[u][v]
#     face = mesh.face[fkey]
#     f = len(face)
#     # switch between UV face sizes
#     # note: in a trimesh this is not necessary!
#     if f < 3:
#         raise MeshError(fkey)
#     if f == 3:
#         # delete UV
#         o = face[v]
#         del mesh.halfedge[u][v]
#         del mesh.halfedge[v][o]
#         del mesh.halfedge[o][u]
#         del mesh.face[fkey]
#     else:
#         # u > v > d => u > d
#         rface = dict((d, k) for k, d in face.items())
#         d = face[v]
#         del face[v]
#         face[u] = d
#         del mesh.halfedge[u][v]
#         del mesh.halfedge[v][d]
#         mesh.halfedge[u][d] = fkey
#     # VU face
#     fkey = mesh.halfedge[v][u]
#     face = mesh.face[fkey]
#     f = len(face)
#     # switch between VU face sizes
#     # note: in a trimesh this is not necessary!
#     if f < 3:
#         raise MeshError(fkey)
#     if f == 3:
#         # delete UV
#         o = face[u]
#         del mesh.halfedge[v][u]  # the collapsing halfedge
#         del mesh.halfedge[u][o]
#         del mesh.halfedge[o][v]
#         del mesh.face[fkey]
#     else:
#         # a > v > u => a > u
#         rface = dict((d, k) for k, d in face.items())
#         a = rface[v]
#         del face[v]
#         face[a] = u
#         del mesh.halfedge[a][v]
#         del mesh.halfedge[v][u]
#         mesh.halfedge[a][u] = fkey
#     # V neighbours and halfedges coming into V
#     for nbr, fkey in mesh.halfedge[v].items():
#         # a > v > nbr => a > u > nbr
#         face = mesh.face[fkey]
#         rface = dict((k, a) for a, k in face.items())
#         a = rface[v]
#         face[a] = u
#         face[u] = nbr
#         del face[v]
#         if v in mesh.halfedge[a]:
#             del mesh.halfedge[a][v]
#         del mesh.halfedge[v][nbr]
#         mesh.halfedge[a][u] = fkey
#         mesh.halfedge[u][nbr] = fkey
#         # only update what will not be updated in the previous part
#         # verify what this is exactly
#         # nbr > v > d => nbr > u > d
#         if v in mesh.halfedge[nbr]:
#             fkey = mesh.halfedge[nbr][v]
#             del mesh.halfedge[nbr][v]
#             mesh.halfedge[nbr][u] = fkey
#     # delete V
#     del mesh.halfedge[v]
#     del mesh.vertex[v]


def collapse_edge(mesh, u, v, t=0.5):
    """Collapse an edge to its first or second vertex, or to an intermediate
    point.

    An edge can only be collapsed if the collapse is `legal`. A collapse is
    legal if it meets the following requirements:

        * any vertex `w` that is a neighbour of both `u` and `v` is a face
          of the mesh
        * `u` and `v` are not on the boundary
        * ...

    See [] for a detailed explanation of these requirements.

    Parameters:
        u (str): The first vertex of the (half-) edge.
        v (str): The second vertex of the (half-) edge.
        t (float): Determines where to collapse to. If `t == 0.0` collapse
            to `u`. If `t == 1.0` collapse to `v`. If `0.0 < t < 1.0`,
            collapse to a point between `u` and `v`.

    Returns:
        None

    Raises:
        ValueError: If `u` and `v` are not neighbours.
    """
    if t < 0.0:
        raise ValueError('Parameter t should be greater than or equal to 0.')
    if t > 1.0:
        raise ValueError('Parameter t should be smaller than or equal to 1.')
    # conditions
    # collapsing of boundary vertices is currently not supported
    # change this to `and` to support collapsing to or from the boundary
    if mesh.is_vertex_on_boundary(u) or mesh.is_vertex_on_boundary(v):
        return
    # check for contained faces
    for nbr in mesh.halfedge[u]:
        if nbr in mesh.halfedge[v]:
            # check if U > V > NBR is a face
            if (mesh.halfedge[u][v] != mesh.halfedge[v][nbr] or mesh.halfedge[u][v] != mesh.halfedge[nbr][u]):
                # check if V > U > NBR is a face
                if (mesh.halfedge[v][u] != mesh.halfedge[u][nbr] or mesh.halfedge[v][u] != mesh.halfedge[nbr][v]):
                    return
    for nbr in mesh.halfedge[v]:
        if nbr in mesh.halfedge[u]:
            # check if U > V > NBR is a face
            if (mesh.halfedge[u][v] != mesh.halfedge[v][nbr] or mesh.halfedge[u][v] != mesh.halfedge[nbr][u]):
                # check if V > U > NBR is a face
                if (mesh.halfedge[v][u] != mesh.halfedge[u][nbr] or mesh.halfedge[v][u] != mesh.halfedge[nbr][v]):
                    return
    # move U
    sp = mesh.vertex_coordinates(u)
    ep = mesh.vertex_coordinates(v)
    line = Line(sp, ep)
    line.scale(t)
    x, y, z = line.end
    mesh.vertex[u]['x'] = x
    mesh.vertex[u]['y'] = y
    mesh.vertex[u]['z'] = z
    # UV face
    fkey = mesh.halfedge[u][v]
    face = mesh.face[fkey]
    # delete UV
    o = face[v]
    del mesh.halfedge[u][v]
    del mesh.halfedge[v][o]
    del mesh.halfedge[o][u]
    del mesh.face[fkey]
    # VU face
    fkey = mesh.halfedge[v][u]
    face = mesh.face[fkey]
    # delete UV
    o = face[u]
    del mesh.halfedge[v][u]  # the collapsing halfedge
    del mesh.halfedge[u][o]
    del mesh.halfedge[o][v]
    del mesh.face[fkey]
    # V neighbours and halfedges coming into V
    for nbr, fkey in mesh.halfedge[v].items():
        # a > v > nbr => a > u > nbr
        face = mesh.face[fkey]
        rface = dict((k, a) for a, k in face.items())
        a = rface[v]
        face[a] = u
        face[u] = nbr
        del face[v]
        if v in mesh.halfedge[a]:
            del mesh.halfedge[a][v]
        del mesh.halfedge[v][nbr]
        mesh.halfedge[a][u] = fkey
        mesh.halfedge[u][nbr] = fkey
        # only update what will not be updated in the previous part
        # verify what this is exactly
        # nbr > v > d => nbr > u > d
        if v in mesh.halfedge[nbr]:
            fkey = mesh.halfedge[nbr][v]
            del mesh.halfedge[nbr][v]
            mesh.halfedge[nbr][u] = fkey
    # delete V
    del mesh.halfedge[v]
    del mesh.vertex[v]
