# -*- coding: utf-8 -*-
# @Author    : Tom Van Mele (vanmelet@ethz.ch)
# @Copyright : Copyright 2014, BLOCK Research Group - ETH Zurich
# @License   : MIT License
# @Date      : 2015-12-04


def centroid(points):
    p = len(points)
    return [coord / p for coord in map(sum, zip(*points))]


def smooth_network(network, fixed=None, k=1, d=0.5, callback=None):
    """"""
    if not fixed:
        fixed = network.leaves()
    for _ in range(k):
        key_xyz = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in key_xyz:
            if key in fixed:
                continue
            nbrs       = network.neighbours(key)
            points     = [key_xyz[nbr] for nbr in nbrs]
            cx, cy, cz = centroid(points)
            x, y, z    = key_xyz[key]
            tx, ty, tz = d * (cx - x), d * (cy - y), d * (cz - z)
            network.vertex[key]['x'] += tx
            network.vertex[key]['y'] += ty
            network.vertex[key]['z'] += tz
        if callback:
            callback(network)


def smooth_network_area(network, fixed=None, k=1, callback=None):
    """"""
    if not fixed:
        fixed = network.leaves()
    for _ in range(k):
        fkey_centroid = dict((fkey, network.face_centroid(fkey)) for fkey in network.face)
        fkey_area     = dict((fkey, network.face_area(fkey)) for fkey in network.face)
        for key in network:
            if key in fixed:
                continue
            area    = 0
            x, y, z = 0, 0, 0
            for fkey in network.vertex_faces(key):
                a  = fkey_area[fkey]
                c  = fkey_centroid[fkey]
                x += a * c[0]
                y += a * c[1]
                z += a * c[2]
                area += a
            network.vertex[key]['x'] = x / area
            network.vertex[key]['y'] = y / area
            network.vertex[key]['z'] = z / area
        if callback:
            callback(network)


def relax_network(network):
    raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
