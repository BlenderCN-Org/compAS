""""""

from brg.geometry import centroid
from brg.geometry import center_of_mass


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# @matthias: remind me that while having post-dehydration nightmares
#            i figure out how to do all of this in a linear algebra-style way...
# also, i wrote these for the network class
# if some things don't work out of the box, come get me, because that just means
# some functionality has not yet been duplicated on the mesh
# or works slightly differently...
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# def mesh_smooth(mesh, k=1, d=0.5):
#     """Smoothen the input mesh by moving each vertex to the centroid of its
#     neighbours.

#     Note:
#         This is a node-per-node version of Laplacian smoothing with umbrella weights.

#     Parameters:
#         k (int): The number of smoothing iterations.
#             Defaults to `1`.
#         d (float): Scale factor for (i.e. damping of) the displacement vector.
#             Defaults to `0.5`.

#     Returns:
#         None
#     """
#     def centroid(points):
#         p = len(points)
#         return [coord / p for coord in map(sum, zip(*points))]
#     boundary = set(mesh.vertices_on_boundary())
#     for _ in range(k):
#         key_xyz = dict((key, (attr['x'], attr['y'], attr['z'])) for key, attr in mesh.vertices_iter(True))
#         for key in key_xyz:
#             if key in boundary:
#                 continue
#             nbrs       = mesh.vertex_neighbours(key)
#             points     = [key_xyz[nbr] for nbr in nbrs]
#             cx, cy, cz = centroid(points)
#             x, y, z    = key_xyz[key]
#             tx, ty, tz = d * (cx - x), d * (cy - y), d * (cz - z)
#             mesh.vertex[key]['x'] += tx
#             mesh.vertex[key]['y'] += ty
#             mesh.vertex[key]['z'] += tz


def mesh_smooth_centroid(mesh, fixed=None, kmax=1, d=1.0, ufunc=None):
    fixed = fixed or []
    fixed = set(fixed)
    for k in range(kmax):
        key_xyz = dict((key, mesh.vertex_coordinates(key)) for key in mesh)
        for key in mesh:
            if key in fixed:
                continue
            p = key_xyz[key]
            # replace this by mesh function?
            nbrs = mesh.vertex_neighbours(key)
            c = centroid([key_xyz[nbr] for nbr in nbrs])
            # update
            attr = mesh.vertex[key]
            attr['x'] += d * (c[0] - p[0])
            attr['y'] += d * (c[1] - p[1])
            attr['z'] += d * (c[2] - p[2])
        # in my implementation the ufunc is called before the coordinates
        # are updated
        # don't know which optio makes more sense...
        if ufunc:
            ufunc(mesh, k)


def mesh_smooth_centerofmass(mesh, fixed=None, kmax=1, d=1.0, ufunc=None):
    fixed = fixed or []
    fixed = set(fixed)
    for k in range(kmax):
        key_xyz = dict((key, mesh.vertex_coordinates(key)) for key in mesh)
        for key in mesh:
            if key in fixed:
                continue
            p = key_xyz[key]
            # replace this by mesh function?
            nbrs = mesh.vertex_neighbours(key, ordered=True)
            c = center_of_mass([key_xyz[nbr] for nbr in nbrs])
            # update
            attr = mesh.vertex[key]
            attr['x'] += d * (c[0] - p[0])
            attr['y'] += d * (c[1] - p[1])
            attr['z'] += d * (c[2] - p[2])
        # in my implementation the ufunc is called before the coordinates
        # are updated
        # don't know which optio makes more sense...
        if ufunc:
            ufunc(mesh, k)


def mesh_smooth_dual_centroid(mesh, fixed=None, kmax=1, d=1.0, ufunc=None):
    raise NotImplementedError


def mesh_smooth_dual_centerofmass(mesh, fixed=None, kmax=1, d=1.0, ufunc=None):
    raise NotImplementedError


# my local implementation is based on per-edge-defined min/max values
# this is not compatible with smoothing in combination with subdivision though
# therefore, is made the min/max values global
def mesh_smooth_length(mesh, lmin, lmax, fixed=None, kmax=1, d=1.0, ufunc=None):
    for k in range(kmax):
        key_xyz = dict((key, mesh.vertex_coordinates(key)) for key in mesh)
        for key in mesh:
            if key in fixed:
                continue
            ep = key_xyz[key]
            # replace this by mesh function?
            points = []
            for nbr in mesh.vertex_neighbours(key):
                sp   = key_xyz[nbr]
                vec  = [ep[i] - sp[i] for i in range(3)]
                lvec = sum(vec[i] ** 2 for i in range(3)) ** 0.5
                uvec = [vec[i] / lvec for i in range(3)]
                lvec = min(lvec, lmax)
                lvec = max(lvec, lmin)
                points.append([sp[i] + lvec * uvec[i] for i in range(3)])
            c = centroid(points)
            # update
            attr = mesh.vertex[key]
            attr['x'] += d * (c[0] - ep[0])
            attr['y'] += d * (c[1] - ep[1])
            attr['z'] += d * (c[2] - ep[2])
        # in my implementation the ufunc is called before the coordinates
        # are updated
        # don't know which optio makes more sense...
        if ufunc:
            ufunc(mesh, k)


# rename to something involving dual?
def mesh_smooth_area(mesh, fixed=None, kmax=1, d=1.0, ufunc=None):
    fixed = fixed or []
    fixed = set(fixed)
    for k in range(kmax):
        fkey_centroid = dict((fkey, mesh.face_centroid(fkey)) for fkey in mesh.face)
        fkey_area     = dict((fkey, mesh.face_area(fkey)) for fkey in mesh.face)
        key_xyz       = dict((key, mesh.vertex_coordinates(key)) for key in mesh)
        for key in mesh:
            if key in fixed:
                continue
            p = key_xyz[key]
            # replace this by mesh function?
            A = 0
            x, y, z = 0, 0, 0
            for fkey in mesh.vertex_faces(key):
                if fkey:
                    a  = fkey_area[fkey]
                    c  = fkey_centroid[fkey]
                    x += a * c[0]
                    y += a * c[1]
                    z += a * c[2]
                    A += a
            if A:
                x = x / A
                y = y / A
                z = z / A
            # update
            attr = mesh.vertex[key]
            attr['x'] += d * (x - p[0])
            attr['y'] += d * (y - p[0])
            attr['z'] += d * (z - p[0])
        # in my implementation the ufunc is called before the coordinates
        # are updated
        # don't know which optio makes more sense...
        if ufunc:
            ufunc(mesh, k)


# d is used in the algorithm
# so some renaming is required
def mesh_smooth_angle(mesh, fixed=None, kmax=1, ufunc=None):
    fixed = fixed or []
    fixed = set(fixed)
    for k in range(kmax):
        key_xyz = dict((key, mesh.vertex_coordinates(key)) for key in mesh)
        for key in mesh:
            if key in fixed:
                continue
            nbrs = mesh.vertex_neighbours(key, ordered=True)
            if len(nbrs) < 4:
                continue
            if len(nbrs) > 4:
                # move to centroid instead?
                continue
            o = key_xyz[key]
            # replace this by mesh function?
            a = key_xyz[nbrs[0]]
            b = key_xyz[nbrs[1]]
            c = key_xyz[nbrs[2]]
            d = key_xyz[nbrs[3]]
            oa = [a[i] - o[i] for i in range(3)]
            ob = [b[i] - o[i] for i in range(3)]
            oc = [c[i] - o[i] for i in range(3)]
            od = [d[i] - o[i] for i in range(3)]
            ac = [0.5 * (oa[i] + oc[i]) for i in range(3)]
            bd = [0.5 * (ob[i] + od[i]) for i in range(3)]
            do = [ac[i] + bd[i] for i in range(3)]
            # update
            attr = mesh.vertex[key]
            attr['x'] += 0.5 * do[0]
            attr['y'] += 0.5 * do[1]
            attr['z'] += 0.5 * do[2]
        # in my implementation the ufunc is called before the coordinates
        # are updated
        # don't know which optio makes more sense...
        if ufunc:
            ufunc(mesh, k)


def mesh_smooth_forcedensity(mesh, fixed=None, kmax=1, d=1.0, ufunc=None):
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
