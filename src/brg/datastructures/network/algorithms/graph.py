# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

from math import cos
from math import sin

from brg.geometry.functions import is_intersecting
from brg.geometry.functions import angle

try:
    import planarity
except ImportError as e:
    print """Planarity is not installed.
Some functionality of this module will not be available.
Get Planarity at https://github.com/hagberg/planarity.
"""

import networkx as nx


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Dec 15, 2014'


# TODO: "inner leaves" check!


def is_network_crossed(network):
    for u1, v1 in network.edges_iter():
        for u2, v2 in network.edges_iter():
            if u1 == u2 or v1 == v2 or u1 == v2 or u2 == v1:
                continue
            else:
                a = network.vertex[u1]['x'], network.vertex[u1]['y']
                b = network.vertex[v1]['x'], network.vertex[v1]['y']
                c = network.vertex[u2]['x'], network.vertex[u2]['y']
                d = network.vertex[v2]['x'], network.vertex[v2]['y']
                if is_intersecting(a, b, c, d):
                    return True
    return False


def are_edges_crossed(edges, vertices):
    for u1, v1 in edges:
        for u2, v2 in edges:
            if u1 == u2 or v1 == v2 or u1 == v2 or u2 == v1:
                continue
            else:
                a = vertices[u1]
                b = vertices[v1]
                c = vertices[u2]
                d = vertices[v2]
                if is_intersecting(a, b, c, d):
                    return True
    return False


def count_network_crossings(network):
    count = 0
    for u1, v1 in network.edges_iter():
        for u2, v2 in network.edges_iter():
            if u1 == u2 or v1 == v2 or u1 == v2 or u2 == v1:
                continue
            else:
                a = network.vertex[u1]['x'], network.vertex[u1]['y']
                b = network.vertex[v1]['x'], network.vertex[v1]['y']
                c = network.vertex[u2]['x'], network.vertex[u2]['y']
                d = network.vertex[v2]['x'], network.vertex[v2]['y']
                if is_intersecting(a, b, c, d):
                    count += 1
    return count


def is_network_2d(network):
    z = None
    for key in network:
        if z is None:
            z = network[key].get('z', 0.0)
        else:
            if z != network[key].get('z', 0.0):
                return False
    return True


# if the graph of a network is planar
# - an embedding of the network in the plane exists
# - a planar straight-line embedding of the network in the plane exists
def is_network_planar(network):
    return planarity.is_planar(network.edges())


# is it embedded in the plane without crossing (curved) edges
def is_network_planar_embedding(network):
    return (is_network_planar(network) and
            is_network_2d(network) and not
            is_network_crossed(network))


# # is it embedded in the plane with straight lines only
# def is_network_straightline_embedding(network):
#     raise NotImplementedError


# # is it embedded in the plane with only straight lines between the nodes
# # and without crossings
# def is_network_planar_straightline_embedding(network):
#     return (is_network_planar_embedding(network) and
#             is_network_straightline_embedding(network))


def embed_network_in_plane(network, fix=None, straightline=True):
    count = 100
    is_embedded = False
    edges = network.edges()
    while count:
        graph = nx.Graph(edges)
        pos = nx.spring_layout(graph)
        if not are_edges_crossed(edges, pos):
            is_embedded = True
            break
        count -= 1
    if not is_embedded:
        return False
    if fix:
        vec0 = [network[fix[1]][axis] - network[fix[0]][axis] for axis in 'xy']
        vec1 = [pos[fix[1]][axis] - pos[fix[0]][axis] for axis in 0, 1]
        # rotate
        a    = -angle(vec0, vec1, rad=True)
        cosa = cos(a)
        sina = sin(a)
        for key in pos:
            x, y = pos[key]
            pos[key][0] = cosa * x - sina * y
            pos[key][1] = sina * x + cosa * y
        # scale
        l0 = (vec0[0] ** 2 + vec0[1] ** 2) ** 0.5
        l1 = (vec1[0] ** 2 + vec1[1] ** 2) ** 0.5
        scale = l0 / l1
        for key in pos:
            pos[key][0] *= scale
            pos[key][1] *= scale
        # translate
        t = network[fix[0]]['x'] - pos[fix[0]][0], network[fix[0]]['y'] - pos[fix[0]][1]
        for key in pos:
            pos[key][0] += t[0]
            pos[key][1] += t[1]
    # update network vertex coordinates
    for key in network:
        network[key]['x'] = pos[key][0]
        network[key]['y'] = pos[key][1]
    return True


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

    # print is_network_crossed(network)
    # print count_network_crossings(network)
    print is_network_planar(network)

    t1 = time.time()

    print t1 - t0

    draw_network(network, vsize=0.1)
