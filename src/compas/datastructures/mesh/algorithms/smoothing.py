from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'smooth_mesh_centroid',
    'smooth_mesh_centerofmass',
    'smooth_mesh_length',
    'smooth_mesh_area',
    'smooth_mesh_angle',
]


def smooth_mesh_centroid(mesh, fixed=None, kmax=1, d=1.0, ufunc=None):
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
            c = centroid_points([key_xyz[nbr] for nbr in nbrs])
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


def smooth_mesh_centerofmass(mesh, fixed=None, kmax=1, d=1.0, ufunc=None):
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
            c = center_of_mass_polygon([key_xyz[nbr] for nbr in nbrs])
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



# my local implementation is based on per-edge-defined min/max values
# this is not compatible with smoothing in combination with subdivision though
# therefore, is made the min/max values global
def smooth_mesh_length(mesh, lmin, lmax, fixed=None, kmax=1, d=1.0, ufunc=None):
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
            c = centroid_points(points)
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
def smooth_mesh_area(mesh, fixed=None, kmax=1, d=1.0, ufunc=None, ufunc_args=None):
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
            attr['y'] += d * (y - p[1])
            attr['z'] += d * (z - p[2])
        # in my implementation the ufunc is called before the coordinates
        # are updated
        # don't know which option makes more sense...
        if ufunc:
            ufunc(mesh, k, ufunc_args)


# d is used in the algorithm
# so some renaming is required
def smooth_mesh_angle(mesh, fixed=None, kmax=1, ufunc=None):
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


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    pass
