# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$


from brg.geometry.functions import angle_smallest as angle
from brg.geometry.planar import is_ccw

import warnings


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Dec 15, 2014'


def construct_network_dual(network, cls, find_faces=True):
    warnings.warn("This function is deprecated. Use 'construct_dual_network' instead.", DeprecationWarning)
    # end of deprecation control
    if find_faces:
        find_network_faces(network)
    dual = cls()
    fkey_centroid = dict((fkey, network.face_centroid(fkey)) for fkey in network.face)
    fkey_key = {}
    for u, v in network.edges_iter():
        fkey = network.halfedge[u][v]
        if fkey not in fkey_key:
            x, y, z = fkey_centroid[fkey]
            dual.add_vertex(fkey, x=x, y=y, z=z)
            fkey_key[fkey] = 1
        k1 = fkey
        fkey = network.halfedge[v][u]
        if fkey not in fkey_key:
            x, y, z = fkey_centroid[fkey]
            dual.add_vertex(fkey, x=x, y=y, z=z)
            fkey_key[fkey] = 1
        k2 = fkey
        dual.add_edge(k1, k2, primal=(u, v))
        network.edge[u][v]['dual'] = (k1, k2)
    return dual


def construct_dual_network(network, cls=None, find_faces=True):
    if not cls:
        cls = type(network)
    if find_faces:
        find_network_faces(network)
    fkey_center = dict((fkey, network.face_center(fkey)) for fkey in network.face)
    inner = list(set(network) - set(network.leaves()))
    dual = cls()
    for key in inner:
        fkeys = network.vertex_faces(key, ordered=True)
        for fkey in fkeys:
            if fkey not in dual:
                x, y, z = fkey_center[fkey]
                dual.add_vertex(fkey, x=x, y=y, z=z)
    for u, v in network.edges_iter():
        f1 = network.halfedge[u][v]
        f2 = network.halfedge[v][u]
        dual.add_edge(f1, f2)
    return dual


def find_network_faces(network, breakpoints=None):
    del network.face
    network.face = {}
    network.face_count = 0
    del network.halfedge
    network.halfedge = dict((key, {}) for key in network.vertex)
    for u, v in network.edges_iter():
        network.halfedge[u][v] = None
        network.halfedge[v][u] = None
    _sort_neighbours(network)
    leaves = network.leaves()
    if leaves:
        u = sorted([(key, network.vertex[key]) for key in leaves], key=lambda x: (x[1]['y'], x[1]['x']))[0][0]
    else:
        u = sorted(network.vertices_iter(data=True), key=lambda x: (x[1]['y'], x[1]['x']))[0][0]
    v = _find_first_neighbour(u, network)
    _find_edge_face(u, v, network)
    for u, v in network.edges_iter():
        if not network.halfedge[u][v]:
            _find_edge_face(u, v, network)
        if not network.halfedge[v][u]:
            _find_edge_face(v, u, network)
    _break_faces(network, breakpoints)
    return network.face


def _find_first_neighbour(key, network):
    angles = []
    nbrs = network.halfedge[key].keys()
    vu = [-1, -1, 0]
    for nbr in nbrs:
        w = [network.vertex[nbr][_] for _ in 'xyz']
        v = [network.vertex[key][_] for _ in 'xyz']
        vw = [w[0] - v[0], w[1] - v[1], 0]
        angles.append(angle(vu, vw))
    return nbrs[angles.index(min(angles))]


def _sort_neighbours(network, ccw=True):
    sorted_neighbours = {}
    xyz = dict((key, [attr[_] for _ in 'xyz']) for key, attr in network.vertices_iter(True))
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
            while not is_ccw(a, b, c):
                pos += 1
                if pos > i:
                    break
                b = xyz[ordered[pos]]
            if pos == 0:
                pos = -1
                b = xyz[ordered[pos]]
                while is_ccw(a, b, c):
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


def _break_faces(network, breakpoints=None):
    if breakpoints is None:
        breakpoints = network.breakpoints()
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

    import time

    import brg

    from brg.datastructures.network.network import Network
    from brg.datastructures.network.drawing import draw_network

    t0 = time.time()

    network = Network.from_obj(brg.get_data('lines.obj'))
    dual    = construct_network_dual(network, Network)

    t1 = time.time()

    print t1 - t0

    draw_network(dual, vsize=0.1)
