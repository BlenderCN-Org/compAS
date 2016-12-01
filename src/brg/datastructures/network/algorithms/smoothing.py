""""""

from brg.geometry import centroid
from brg.geometry import center_of_mass


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = '<vanmelet@ethz.ch>'


def smooth_network_centroid(network, fixed=None, kmax=1, d=0.5, callback=None):
    """"""
    fixed = fixed or []
    fixed = set(fixed)
    if callback:
        assert callable(callback), 'The callback is not callable.'
    for k in range(kmax):
        key_xyz = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in network:
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
            callback(network, k)


def smooth_network_area(network, fixed=None, kmax=1, d=0.5, callback=None):
    """"""
    fixed  = fixed or []
    fixed  = set(fixed)
    leaves = network.leaves()
    leaves = set(leaves)
    if callback:
        assert callable(callback), 'The callback is not callable.'
    for k in range(kmax):
        fkey_centroid = dict((fkey, network.face_centroid(fkey)) for fkey in network.face)
        fkey_area     = dict((fkey, network.face_area(fkey)) for fkey in network.face)
        key_xyz       = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in network:
            if key in fixed:
                continue
            if key in leaves:
                nbr   = network.neighbours(key)[0]
                fkeys = [network.halfedge[key][nbr], network.halfedge[nbr][key]]
            else:
                fkeys = network.vertex_faces(key)
            A = 0
            x, y, z = 0, 0, 0
            for fkey in fkeys:
                # networks have an outside face...
                if fkey == '0':
                    continue
                a  = fkey_area[fkey]
                c  = fkey_centroid[fkey]
                x += a * c[0]
                y += a * c[1]
                z += a * c[2]
                A += a
            x /= A
            y /= A
            z /= A
            x0, y0, z0 = key_xyz[key]
            attr = network.vertex[key]
            attr['x'] += d * (x - x0)
            attr['y'] += d * (y - y0)
            attr['z'] += d * (z - z0)
        if callback:
            callback(network, k)


def smooth_network_dual_centroid(network, fixed=None, kmax=1, d=0.5, callback=None):
    """"""
    fixed  = fixed or []
    fixed  = set(fixed)
    leaves = network.leaves()
    leaves = set(leaves)
    if callback:
        assert callable(callback), 'The callback is not callable.'
    for k in range(kmax):
        fkey_centroid = dict((fkey, network.face_centroid(fkey)) for fkey in network.face)
        key_xyz       = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in network:
            if key in fixed:
                continue
            if key in leaves:
                nbr   = network.neighbours(key)[0]
                fkeys = [network.halfedge[key][nbr], network.halfedge[nbr][key]]
            else:
                fkeys = network.vertex_faces(key)
            x, y, z = 0, 0, 0
            for fkey in fkeys:
                # networks have an outside face...
                if fkey == '0':
                    continue
                c  = fkey_centroid[fkey]
                x += c[0]
                y += c[1]
                z += c[2]
            f = len(fkeys)
            x /= f
            y /= f
            z /= f
            x0, y0, z0 = key_xyz[key]
            attr = network.vertex[key]
            attr['x'] += d * (x - x0)
            attr['y'] += d * (y - y0)
            attr['z'] += d * (z - z0)
        if callback:
            callback(network, k)


def smooth_network_mass(network, fixed=None, kmax=1, d=0.5, callback=None):
    fixed = fixed or []
    fixed = set(fixed)
    if callback:
        assert callable(callback), 'The callback is not callable.'
    for k in range(kmax):
        key_xyz = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in network:
            if key in fixed:
                continue
            nbrs       = network.neighbours(key, ordered=True)
            points     = [key_xyz[nbr] for nbr in nbrs]
            cx, cy, cz = center_of_mass(points)
            x, y, z    = key_xyz[key]
            attr       = network.vertex[key]
            attr['x'] += d * (cx - x)
            attr['y'] += d * (cy - y)
            attr['z'] += d * (cz - z)
        if callback:
            callback(network, k)


def smooth_network_length(network, lmin, lmax, fixed=None, kmax=1, d=0.5, callback=None):
    fixed = fixed or []
    fixed = set(fixed)
    if callback:
        assert callable(callback), 'The callback is not callable.'
    for k in range(kmax):
        key_xyz = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in network:
            if key in fixed:
                continue
            ep = key_xyz[key]
            points = []
            for nbr in network.neighbours(key):
                sp   = key_xyz[nbr]
                vec  = [ep[i] - sp[i] for i in range(3)]
                lvec = sum(vec[i] ** 2 for i in range(3)) ** 0.5
                uvec = [vec[i] / lvec for i in range(3)]
                lvec = min(lvec, lmax)
                lvec = max(lvec, lmin)
                p    = [sp[i] + lvec * uvec[i] for i in range(3)]
                points.append(p)
            x, y, z = centroid(points)
            attr = network.vertex[key]
            attr['x'] += d * (x - ep[0])
            attr['y'] += d * (y - ep[1])
            attr['z'] += d * (z - ep[2])
        if callback:
            callback(network, k)


def smooth_network_angle(network, fixed=None, kmax=1, d=0.5, callback=None):
    fixed = fixed or []
    fixed = set(fixed)
    if callback:
        assert callable(callback), 'The callback is not callable.'
    for k in range(kmax):
        key_xyz = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in network:
            if key in fixed:
                continue
            nbrs = network.neighbours(key, ordered=True)
            if len(nbrs) < 4:
                continue
            if len(nbrs) > 4:
                # move to centroid
                continue
            o    = key_xyz[key]
            n0   = key_xyz[nbrs[0]]
            n1   = key_xyz[nbrs[1]]
            n2   = key_xyz[nbrs[2]]
            n3   = key_xyz[nbrs[3]]
            on0  = [n0[i] - o[i] for i in range(3)]
            on1  = [n1[i] - o[i] for i in range(3)]
            on2  = [n2[i] - o[i] for i in range(3)]
            on3  = [n3[i] - o[i] for i in range(3)]
            n02  = [0.5 * (on0[i] + on2[i]) for i in range(3)]
            n13  = [0.5 * (on1[i] + on3[i]) for i in range(3)]
            dn   = [n02[i] + n13[i] for i in range(3)]
            attr = network.vertex[key]
            attr['x'] += d * dn[0]
            attr['y'] += d * dn[1]
            attr['z'] += d * dn[2]
        if callback:
            callback(network, k)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
