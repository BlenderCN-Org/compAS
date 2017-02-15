from brg.geometry import centroid_points
from brg.geometry import center_of_mass_polygon


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = '<vanmelet@ethz.ch>'


__all__ = [
    'smooth_network_mixed',
    'smooth_network_centroid',
    'smooth_network_mass',
    'smooth_network_area',
    'smooth_network_length',
]


def smooth_network_mixed(network, smoothers, lmin=None, lmax=None, fixed=None, kmax=1, d=0.5, callback=None):
    """Smooth a network using mixed criteria.

    Parameters:
        network (brg.datastructures.network.Network): The network object.
        smoothers (list): A list of smoothing algorithms and their weight.
        lmin (float): Optional.
            Minimum length. Default is ``None``.
        lmax (float): Optional.
            Maximum length. Default is ``None``.
        fixed (list): Optional.
            The fixed vertices of the network. Default is ``None``.
        kmax (int): Optional.
            The maximum number of iterations. Default is ``1``.
        d (float): Optional.
            A damping factor. Default is ``0.5``.
        callback (callable): Optional.
            A user-defined callback function to be executed after every iteration.
            Default is ``None``.

    Raises:
        Exception: If a callback is provided, but not callable.

    Example:

        .. plot::
            :include-source:

            import brg
            from brg.datastructures.network import Network
            from brg.datastructures.network.algorithms import smooth_network_mixed
            from brg.datastructures.network.algorithms import find_network_faces

            network = Network.from_obj(brg.get_data('grid_irregular.obj'))

            find_network_faces(network, network.leaves())

            smooth_network_mixed(network,
                                 [('centroid', 0.5), ('area', 0.5)],
                                 fixed=network.leaves(),
                                 kmax=10)

            network.plot()

    """
    w = sum(weight for smoother, weight in smoothers)
    smoothers = [(smoother, weight / w) for smoother, weight in smoothers]
    fixed     = fixed or []
    fixed     = set(fixed)
    leaves    = set(network.leaves())
    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')
    for k in range(kmax):
        key_xyz       = dict((key, network.vertex_coordinates(key)) for key in network)
        fkey_centroid = dict((fkey, network.face_centroid(fkey)) for fkey in network.face)
        fkey_area     = dict((fkey, network.face_area(fkey)) for fkey in network.face)
        for key in network:
            if key in fixed:
                continue
            xyz0 = key_xyz[key]
            xyzN = [0, 0, 0]
            for smoother, weight in smoothers:
                if smoother == 'centroid':
                    nbrs = network.neighbours(key)
                    xyz = centroid_points([key_xyz[nbr] for nbr in nbrs])
                    xyzN[0] += weight * xyz[0]
                    xyzN[1] += weight * xyz[1]
                    xyzN[2] += weight * xyz[2]
                    continue
                if smoother == 'area':
                    if key in leaves:
                        nbr   = network.neighbours(key)[0]
                        fkeys = [network.halfedge[key][nbr], network.halfedge[nbr][key]]
                    else:
                        fkeys = network.vertex_faces(key)
                    A = 0
                    x, y, z = 0, 0, 0
                    for fkey in fkeys:
                        if fkey == 0:
                            continue
                        a = fkey_area[fkey]
                        c = fkey_centroid[fkey]
                        x += a * c[0]
                        y += a * c[1]
                        z += a * c[2]
                        A += a
                    xyzN[0] += weight * x / A
                    xyzN[1] += weight * y / A
                    xyzN[2] += weight * z / A
                    continue
                if smoother == 'length':
                    if lmin and lmax:
                        ep = xyz0
                        ps = []
                        for nbr in network.neighbours(key):
                            sp   = key_xyz[nbr]
                            vec  = [ep[i] - sp[i] for i in range(3)]
                            lvec = sum(vec[i] ** 2 for i in range(3)) ** 0.5
                            uvec = [vec[i] / lvec for i in range(3)]
                            lvec = min(lvec, lmax)
                            lvec = max(lvec, lmin)
                            p    = [sp[i] + lvec * uvec[i] for i in range(3)]
                            ps.append(p)
                        xyz = centroid_points(ps)
                        xyzN[0] += weight * xyz[0]
                        xyzN[1] += weight * xyz[1]
                        xyzN[2] += weight * xyz[2]
                    continue
            attr = network.vertex[key]
            attr['x'] += d * (xyzN[0] - xyz0[0])
            attr['y'] += d * (xyzN[1] - xyz0[1])
            attr['z'] += d * (xyzN[2] - xyz0[2])
        if callback:
            callback(network, k)


def smooth_network_centroid(network, fixed=None, kmax=1, d=0.5, callback=None):
    """Smooth a network using per vertex the centroid of its neighbours.

    Parameters:
        network (brg.datastructures.network.Network): The network object.
        fixed (list): Optional.
            The fixed vertices of the network. Default is ``None``.
        kmax (int): Optional.
            The maximum number of iterations. Default is ``1``.
        d (float): Optional.
            The damping factor. Default is ``0.5``.
        callback (callable): Optional.
            A user-defined callback function to be executed after every iteration.
            Default is ``None``.

    Raises:
        Exception: If a callback is provided, but not callable.

    Example:

        .. plot::
            :include-source:

            import brg
            from brg.datastructures.network import Network
            from brg.datastructures.network.algorithms import smooth_network_centroid

            network  = Network.from_obj(brg.get_data('grid_irregular.obj'))

            smooth_network_centroid(network, fixed=network.leaves(), kmax=10)

            network.plot()

    """
    fixed = fixed or []
    fixed = set(fixed)
    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')
    for k in range(kmax):
        key_xyz = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in network:
            if key in fixed:
                continue
            nbrs       = network.neighbours(key)
            points     = [key_xyz[nbr] for nbr in nbrs]
            cx, cy, cz = centroid_points(points)
            x, y, z    = key_xyz[key]
            attr       = network.vertex[key]
            attr['x'] += d * (cx - x)
            attr['y'] += d * (cy - y)
            attr['z'] += d * (cz - z)
        if callback:
            callback(network, k)


def smooth_network_area(network, fixed=None, kmax=1, d=0.5, callback=None):
    """Smooth a network using per vertex the centroid of the neighbouring faces, weighted by their respective areas.

    Parameters:
        network (brg.datastructures.network.Network): The network object.
        fixed (list): Optional.
            The fixed vertices of the network. Default is ``None``.
        kmax (int): Optional.
            The maximum number of iterations. Default is ``1``.
        d (float): Optional.
            The damping factor. Default is ``0.5``.
        callback (callable): Optional.
            A user-defined callback function to be executed after every iteration.
            Default is ``None``.

    Raises:
        Exception: If a callback is provided, but not callable.

    Example:

        .. plot::
            :include-source:

            import brg
            from brg.datastructures.network import Network
            from brg.datastructures.network.algorithms import find_network_faces
            from brg.datastructures.network.algorithms import smooth_network_area

            network  = Network.from_obj(brg.get_data('grid_irregular.obj'))

            find_network_faces(network, network.leaves())
            smooth_network_area(network, fixed=network.leaves(), kmax=10)

            network.plot()

    """
    fixed  = fixed or []
    fixed  = set(fixed)
    leaves = network.leaves()
    leaves = set(leaves)
    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')
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
                if fkey == 0:
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


def smooth_network_mass(network, fixed=None, kmax=1, d=0.5, callback=None):
    """Smooth a network using per vertex the center of mass of the polygon formed by the neighbouring vertices.

    Parameters:
        network (brg.datastructures.network.Network): The network object.
        fixed (list): Optional.
            The fixed vertices of the network. Default is ``None``.
        kmax (int): Optional.
            The maximum number of iterations. Default is ``1``.
        d (float): Optional.
            The damping factor. Default is ``0.5``.
        callback (callable): Optional.
            A user-defined callback function to be executed after every iteration.
            Default is ``None``.

    Raises:
        Exception: If a callback is provided, but not callable.

    Example:

        .. plot::
            :include-source:

            import brg
            from brg.datastructures.network import Network
            from brg.datastructures.network.algorithms import find_network_faces
            from brg.datastructures.network.algorithms import smooth_network_mass

            network  = Network.from_obj(brg.get_data('grid_irregular.obj'))

            find_network_faces(network, network.leaves())
            smooth_network_mass(network, fixed=network.leaves(), kmax=10)

            network.plot()

    """
    fixed = fixed or []
    fixed = set(fixed)
    if callback:
        if not callable(callback):
            raise Exception('The callback is not callable.')
    for k in range(kmax):
        key_xyz = dict((key, network.vertex_coordinates(key)) for key in network)
        for key in network:
            if key in fixed:
                continue
            nbrs       = network.neighbours(key, ordered=True)
            points     = [key_xyz[nbr] for nbr in nbrs]
            cx, cy, cz = center_of_mass_polygon(points)
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
        if not callable(callback):
            raise Exception('The callback is not callable.')
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
            x, y, z = centroid_points(points)
            attr = network.vertex[key]
            attr['x'] += d * (x - ep[0])
            attr['y'] += d * (y - ep[1])
            attr['z'] += d * (z - ep[2])
        if callback:
            callback(network, k)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg

    from brg.datastructures.network import Network
    from brg.datastructures.network.algorithms import find_network_faces

    network = Network.from_obj(brg.get_data('grid_irregular.obj'))

    find_network_faces(network, network.leaves())
    smooth_network_mass(network, fixed=network.leaves(), kmax=10)

    network.plot()
