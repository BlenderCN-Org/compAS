""""""

from brg.geometry.elements.line import Line
from brg.exceptions import MeshError


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


def is_collapse_legal(mesh, u, v):
    """Verify if the requested collapse is legal fro a triangle mesh.

    Parameters:
        mesh (brg.datastructures.mesh.Mesh) :
            The mesh.
        u (str) : The vertex to collapse towards.
        v (str) : The vertex to collapse.

    Returns:
        bool :
            `True` if the collapse is legal. `False` otherwise.

    Note:
        ...

    >>> ...

    """
    # collapsing of boundary vertices is currently not supported
    # change this to `and` to support collapsing to or from the boundary
    if mesh.is_vertex_on_boundary(u) or mesh.is_vertex_on_boundary(v):
        return False
    # check for contained faces
    for nbr in mesh.halfedge[u]:
        if nbr in mesh.halfedge[v]:
            # check if U > V > NBR is a face
            fkey = mesh.halfedge[u][v]
            if fkey != mesh.halfedge[v][nbr] or fkey != mesh.halfedge[nbr][u]:
                # check if V > U > NBR is a face
                fkey = mesh.halfedge[v][u]
                if fkey != mesh.halfedge[u][nbr] or fkey != mesh.halfedge[nbr][v]:
                    return False
    for nbr in mesh.halfedge[v]:
        if nbr in mesh.halfedge[u]:
            # check if U > V > NBR is a face
            fkey = mesh.halfedge[u][v]
            if fkey != mesh.halfedge[v][nbr] or fkey != mesh.halfedge[nbr][u]:
                # check if V > U > NBR is a face
                fkey = mesh.halfedge[v][u]
                if fkey != mesh.halfedge[u][nbr] or fkey != mesh.halfedge[nbr][v]:
                    return False
    return True


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
    # check value of `t`
    # is this necessary?
    if t < 0.0:
        raise ValueError('Parameter t should be greater than or equal to 0.')
    if t > 1.0:
        raise ValueError('Parameter t should be smaller than or equal to 1.')
    # check collapse conditions
    if not is_collapse_legal(mesh, u, v):
        return False
    # move U
    sp = mesh.vertex_coordinates(u)
    ep = mesh.vertex_coordinates(v)
    # this might be a lot faster w/o making a line object
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
            # *if*s are a little bit suspicious in these kind of algorithms
            del mesh.halfedge[a][v]
        del mesh.halfedge[v][nbr]
        mesh.halfedge[a][u] = fkey
        mesh.halfedge[u][nbr] = fkey
        # only update what will not be updated in the previous part
        # verify what this is exactly
        # nbr > v > d => nbr > u > d
        if v in mesh.halfedge[nbr]:
            # *if*s are a little bit suspicious in these kind of algorithms
            fkey = mesh.halfedge[nbr][v]
            del mesh.halfedge[nbr][v]
            mesh.halfedge[nbr][u] = fkey
    # delete V
    del mesh.halfedge[v]
    del mesh.vertex[v]
    return True


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
