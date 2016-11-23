""""""

__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


# add the nest algorithms
# callback vs. ufunc?
# rename to network_xxx?
# revert to empty list if fixed not provided?


def centroid(points):
    p = len(points)
    return [coord / p for coord in map(sum, zip(*points))]


def smooth_network(network, fixed=None, k=1, d=0.5, callback=None):
    """"""
    if not fixed:
        fixed = network.leaves()
    fixed = set(fixed)
    for _ in range(k):
        key_xyz = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in key_xyz:
            if key in fixed:
                continue
            nbrs       = network.neighbours(key)
            points     = [key_xyz[nbr] for nbr in nbrs]
            cx, cy, cz = centroid(points)
            x, y, z    = key_xyz[key]
            attr       = network.vertex[key]
            attr['x'] += d * (cx - x)
            attr['y'] += d * (cy - y)
            attr['z'] += d * (cz - z)
        if callback:
            callback(network)


def smooth_network_area(network, fixed=None, k=1, callback=None):
    """"""
    if not fixed:
        fixed = network.leaves()
    fixed = set(fixed)
    for _ in range(k):
        fkey_centroid = dict((fkey, network.face_centroid(fkey)) for fkey in network.face)
        fkey_area     = dict((fkey, network.face_area(fkey)) for fkey in network.face)
        for key in network:
            if key in fixed:
                continue
            A = 0
            x, y, z = 0, 0, 0
            for fkey in network.vertex_faces(key):
                a  = fkey_area[fkey]
                c  = fkey_centroid[fkey]
                x += a * c[0]
                y += a * c[1]
                z += a * c[2]
                A += a
            attr = network.vertex[key]
            attr['x'] = x / A
            attr['y'] = y / A
            attr['z'] = z / A
        if callback:
            callback(network)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
