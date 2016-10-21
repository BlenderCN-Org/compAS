# -*- coding: utf-8 -*-
# @Author    : Tom Van Mele (vanmelet@ethz.ch)
# @Copyright : Copyright 2014, BLOCK Research Group - ETH Zurich
# @License   : MIT License
# @Date      : 2015-12-04


def smooth_network(network, fixed=None, k=1, d=0.5, callback=None):
    """"""
    def centroid(points):
        p = len(points)
        return [coord / p for coord in map(sum, zip(*points))]
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


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
