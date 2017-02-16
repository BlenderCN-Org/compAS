from brg.geometry import angle_smallest_vectors
from brg.geometry.planar import is_ccw_2d


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


__all__ = [
    'construct_dual_network',
    'find_network_faces',
]


def construct_dual_network(network, cls=None):
    """Construct the dual of a network.

    Parameters:
        network (brg.datastructures.network.Network): The network object.
        cls (brg.datastructures.network.Network):
            Optional.
            The class of the dual.
            Default is ``None``.
            If ``None``, the cls is inferred from the type of the provided network
            object.

    Warning:
        A network (or a graph) has a dual if, and only if, it is planar.
        Constructing the dual relies on the information about the faces of the
        network, or, in other words, about the ordering of neighbouring vertices
        around a vertex. To determine the faces of the network (using :func:`find_network_faces`)
        the network should be embedded in the plane, i.e drawn such that it is a
        proper cell decomposition of the plane (it divides the plane in non-overlapping
        spaces).

    Example:

        .. plot::
            :include-source:

            import brg
            from brg.datastructures.network import Network
            from brg.datastructures.network.algorithms import find_network_faces
            from brg.datastructures.network.algorithms import construct_dual_network

            network = Network.from_obj(brg.get_data('grid_irregular.obj'))

            find_network_faces(network, breakpoints=network.leaves())

            dual = construct_dual_network(network, Network)

            points = []
            for key in dual:
                points.append({
                    'pos': dual.vertex_coordinates(key, 'xy'),
                    'facecolor': '#ffffff',
                    'edgecolor': '#444444',
                    'textcolor': '#000000',
                    'size': 0.15,
                    'text': key
                })

            lines = []
            for u, v in dual.edges():
                lines.append({
                    'start': dual.vertex_coordinates(u, 'xy'),
                    'end': dual.vertex_coordinates(v, 'xy'),
                    'color': '#000000'
                })

            network.plot(
                vertices_on=True,
                vsize=0.075,
                vcolor={key: '#ff0000' for key in network.leaves()},
                ecolor={(u, v): '#cccccc' for u, v in network.edges()},
                points=points,
                lines=lines
            )

    """
    if not cls:
        cls = type(network)
    dual = cls()
    for fkey in network.face:
        x, y, z = network.face_center(fkey)
        dual.add_vertex(fkey, x=x, y=y, z=z)
    for u, v in network.edges_iter():
        f1 = network.halfedge[u][v]
        f2 = network.halfedge[v][u]
        dual.add_edge(f1, f2)
    return dual


def find_network_faces(network, breakpoints=None):
    if not breakpoints:
        breakpoints = []
    network.clear_facedict()
    network.clear_halfedgedict()
    network.halfedge = dict((key, {}) for key in network.vertex)
    for u, v in network.edges_iter():
        network.halfedge[u][v] = None
        network.halfedge[v][u] = None
    _sort_neighbours(network)
    leaves = network.leaves()
    if leaves:
        u = sorted([(key, network.vertex[key]) for key in leaves], key=lambda x: (x[1]['y'], x[1]['x']))[0][0]
    else:
        u = sorted(network.vertices_iter(True), key=lambda x: (x[1]['y'], x[1]['x']))[0][0]
    v = _find_first_neighbour(u, network)
    _find_edge_face(u, v, network)
    for u, v in network.edges_iter():
        if network.halfedge[u][v] is None:
            _find_edge_face(u, v, network)
        if network.halfedge[v][u] is None:
            _find_edge_face(v, u, network)
    _break_faces(network, breakpoints)
    return network.face


def _find_first_neighbour(key, network):
    angles = []
    nbrs = network.halfedge[key].keys()
    if len(nbrs) == 1:
        return nbrs[0]
    vu = [-1, -1, 0]
    for nbr in nbrs:
        w = [network.vertex[nbr][_] for _ in 'xyz']
        v = [network.vertex[key][_] for _ in 'xyz']
        vw = [w[0] - v[0], w[1] - v[1], 0]
        angles.append(angle_smallest_vectors(vu, vw))
    return nbrs[angles.index(min(angles))]


def _sort_neighbours(network, ccw=True):
    sorted_neighbours = {}
    xyz = dict((key, network.vertex_coordinates(key)) for key in network.vertices_iter())
    for key in network.vertex:
        nbrs = network.halfedge[key].keys()
        if len(nbrs) == 1:
            sorted_neighbours[key] = nbrs
            continue
        ordered = [nbrs[0]]
        a = xyz[key]
        for i, nbr in enumerate(nbrs[1:]):
            c = xyz[nbr]
            pos = 0
            b = xyz[ordered[pos]]
            while not is_ccw_2d(a, b, c):
                pos += 1
                if pos > i:
                    break
                b = xyz[ordered[pos]]
            if pos == 0:
                pos = -1
                b = xyz[ordered[pos]]
                while is_ccw_2d(a, b, c):
                    pos -= 1
                    if pos < -len(ordered):
                        break
                    b = xyz[ordered[pos]]
                pos += 1
            ordered.insert(pos, nbr)
        if not ccw:
            sorted_neighbours[key] = ordered[::-1]
        sorted_neighbours[key] = ordered
    for key, nbrs in sorted_neighbours.iteritems():
        network.vertex[key]['sorted_neighbours'] = nbrs[::-1]
    return sorted_neighbours


def _find_edge_face(u, v, network):
    cycle = [u]
    while True:
        cycle.append(v)
        nbrs = network.vertex[v]['sorted_neighbours']
        nbr = nbrs[nbrs.index(u) - 1]
        u, v = v, nbr
        if v == cycle[0]:
            cycle.append(v)
            break
    fkey = network.add_face(cycle)
    return fkey


def _break_faces(network, breakpoints):
    breakpoints = set(breakpoints)
    for fkey, vertices in network.face.items():
        faces = []
        faces.append([vertices[0]])
        for i in range(1, len(vertices) - 1):
            key = vertices[i]
            faces[-1].append(key)
            if key in breakpoints:
                faces.append([key])
        faces[-1].append(vertices[-1])
        if len(faces) == 1:
            continue
        if faces[0][0] not in breakpoints and faces[-1][-1] not in breakpoints:
            if faces[0][0] == faces[-1][-1]:
                faces[:] = [faces[-1] + faces[0][1:]] + faces[1:-1]
        if len(faces) == 1:
            continue
        del network.face[fkey]
        for vertices in faces:
            network.add_face(vertices)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg
    from brg.datastructures.network import Network
    from brg.datastructures.network.algorithms import find_network_faces
    from brg.datastructures.network.algorithms import construct_dual_network

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    find_network_faces(network, breakpoints=network.leaves())

    dual = construct_dual_network(network, Network)

    network.plot(
        vertices_on=True,
        vsize=0.075,
        vcolor={key: '#ff0000' for key in network.leaves()},
        ecolor={(u, v): '#cccccc' for u, v in network.edges()},
        points=[{'pos': dual.vertex_coordinates(key, 'xy'), 'facecolor': '#ffffff', 'edgecolor': '#444444', 'textcolor': '#000000', 'size': 0.15, 'text': key} for key in dual],
        lines=[{'start': dual.vertex_coordinates(u, 'xy'), 'end': dual.vertex_coordinates(v, 'xy'), 'color': '#000000'} for u, v in dual.edges()]
    )
