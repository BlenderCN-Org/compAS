from brg.geometry.elements import Line


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'split_edge_network',
]


def split_edge_network(network, u, v, t=0.5, allow_boundary=True):
    """Split and edge by inserting a vertex along its length.

    Parameters:
        u (str): The key of the first vertex of the edge.
        v (str): The key of the second vertex of the edge.
        t (float): The position of the inserted vertex.
        allow_boundary (bool): Optional. Split boundary edges, if ``True``.
            Defaults is ``True``.

    Returns:
        str: The key of the inserted vertex.

    Raises:
        ValueError: If `u` and `v` are not neighbours.

    """
    if t <= 0.0:
        raise ValueError('t should be greater than 0.0.')
    if t >= 1.0:
        raise ValueError('t should be smaller than 1.0.')
    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = network.halfedge[u][v]
    fkey_vu = network.halfedge[v][u]
    # if not allow_boundary:
    #     if fkey_uv is None or fkey_vu is None:
    #         return
    # the split vertex
    sp = network.vertex_coordinates(u)
    ep = network.vertex_coordinates(v)
    line = Line(sp, ep)
    line.scale(t)
    x, y, z = line.end
    w = network.add_vertex(x=x, y=y, z=z)
    network.add_edge(u, w)
    network.add_edge(w, v)
    if v in network.edge[u]:
        del network.edge[u][v]
    elif u in network.edge[v]:
        del network.edge[v][u]
    else:
        raise Exception
    # split half-edge UV
    network.halfedge[u][w] = fkey_uv
    network.halfedge[w][v] = fkey_uv
    del network.halfedge[u][v]
    # update the UV face if it is not None
    if fkey_uv is not None:
        vertices = network.face[fkey_uv]
        i = vertices.index(u)
        vertices.insert(i, w)
    # split half-edge VU
    network.halfedge[v][w] = fkey_vu
    network.halfedge[w][u] = fkey_vu
    del network.halfedge[v][u]
    # update the VU face if it is not None
    if fkey_vu is not None:
        vertices = network.face[fkey_vu]
        i = vertices.index(v)
        vertices.insert(i, w)
    # return the key of the split vertex
    return w


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg
    from brg.datastructures.network import Network
    from brg.datastructures.network.algorithms import find_network_faces

    data = brg.get_data('lines.obj')
    network = Network.from_obj(data)

    find_network_faces(network, breakpoints=network.leaves())

    a = split_edge_network(network, '0', '22')
    b = split_edge_network(network, '2', '30')

    print network.halfedge['0'][a]
    print network.halfedge[a]['22']

    print network.halfedge[a]['0']
    print network.halfedge['22'][a]

    network.plot(
        vlabel=dict((key, key) for key in network),
        flabel=dict((fkey, fkey) for fkey in network.face)
    )
