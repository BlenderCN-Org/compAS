from numpy import array
from numpy import hstack
from numpy import linspace
from numpy import meshgrid

from scipy.spatial import Delaunay

from shapely.geometry import Polygon
from shapely.geometry import Point

from brg.geometry.polyline import align_polylines
from brg.geometry.polyline import join_polylines

from brg.datastructures import Mesh

from brg.datastructures.mesh.algorithms.orientation import mesh_unify_cycle_directions
from brg.datastructures.mesh.algorithms.optimisation import mesh_smooth


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'GNU - General Public License'
__version__    = '0.0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '27.03.2014'


def simplex_centroids(simplices, seeds):
    return [
        [axis / 3 for axis in map(sum, zip(*[seeds[index] for index in simplex]))]
        for simplex in simplices
    ]


################################################################################
################################################################################
################################################################################
################################################################################
################################################################################


if __name__ == '__main__':

    import sys
    import json
    import cStringIO
    import cProfile
    import pstats
    import traceback

    out_dict = {
        'data': {},
        'error': None,
        'iterations': None,
        'profile': None,
    }

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    with open(in_path, 'rb') as f:
        in_dict = json.load(f)

    try:
        profile = cProfile.Profile()
        profile.enable()
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        config   = in_dict['config']
        boundary = in_dict['boundary']
        holes    = in_dict['holes']
        spacing  = in_dict['spacing']
        # ----------------------------------------------------------------------
        tol       = config.get('tol', 0.001)
        do_smooth = config.get('do_smooth', False)
        dva       = config.get('dva', {})
        dea       = config.get('dea', {})
        dfa       = config.get('dfa', {})
        k         = config.get('k', 10)
        # ----------------------------------------------------------------------
        boundary = align_polylines(boundary, tol)
        boundary = join_polylines(boundary)
        boundary = [point[0:2] for point in boundary]
        # ----------------------------------------------------------------------
        if not holes:
            holes = []
        holes = [[point[0:2] for point in hole] for hole in holes]
        # ----------------------------------------------------------------------
        bpoly = Polygon(boundary)
        # ----------------------------------------------------------------------
        xy    = array(boundary, dtype=float)
        x     = linspace(xy[:, 0].min(), xy[:, 0].max(), xy[:, 0].ptp() / spacing)
        y     = linspace(xy[:, 1].min(), xy[:, 1].max(), xy[:, 1].ptp() / spacing)
        X, Y  = meshgrid(x, y)
        seeds = hstack((X.reshape((-1, 1), order='C'), Y.reshape((-1, 1), order='C')))
        seeds = seeds.tolist()
        # ----------------------------------------------------------------------
        # filter out seeds outside of boundary
        # ----------------------------------------------------------------------
        seeds = [seed for seed in seeds if bpoly.contains(Point(seed))]
        # ----------------------------------------------------------------------
        # filter out points too close to boundary points
        # ----------------------------------------------------------------------
        selected = []
        for p in iter(seeds):
            farenough = True
            for i in range(-1, len(boundary) - 1):
                b0 = boundary[i]
                b1 = boundary[i + 1]
                d  = 0.5 * ((b0[0] - b1[0]) ** 2 + (b0[1] - b1[1]) ** 2) ** 0.5
                if d > ((b0[0] - p[0]) ** 2 + (b0[1] - p[1]) ** 2) ** 0.5:
                    farenough = False
                    break
            if farenough:
                selected.append(p)
        seeds = boundary + selected
        # ----------------------------------------------------------------------
        # filter out points in holes
        # ----------------------------------------------------------------------
        for hole in holes:
            poly     = Polygon(hole)
            seeds    = [seed for seed in seeds if not poly.contains(Point(seed))]
            selected = []
            for p in iter(seeds):
                farenough = True
                for i in range(-1, len(hole) - 1):
                    h0 = hole[i]
                    h1 = hole[i + 1]
                    d  = 0.5 * ((h0[0] - h1[0]) ** 2 + (h0[1] - h1[1]) ** 2) ** 0.5
                    if d > ((h0[0] - p[0]) ** 2 + (h0[1] - p[1]) ** 2) ** 0.5:
                        farenough = False
                        break
                if farenough:
                    selected.append(p)
            seeds = hole + selected
        # ----------------------------------------------------------------------
        # make a Delaunay triangulation
        # ----------------------------------------------------------------------
        tri       = Delaunay(seeds)
        simplices = tri.simplices.tolist()
        # ----------------------------------------------------------------------
        # filter out simplices outside of the boundary
        # ----------------------------------------------------------------------
        centroids = simplex_centroids(simplices, seeds)
        simplices = [simplices[i] for i in range(len(simplices)) if bpoly.contains(Point(centroids[i]))]
        # ----------------------------------------------------------------------
        # filter out simplices in the holes
        # ----------------------------------------------------------------------
        for hole in holes:
            centroids = simplex_centroids(simplices, seeds)
            poly      = Polygon(hole)
            simplices = [simplices[i] for i in range(len(simplices)) if not poly.contains(Point(centroids[i]))]
        # ----------------------------------------------------------------------
        # make the seeds 3D
        # ----------------------------------------------------------------------
        seeds = [seed if len(seed) == 3 else [seed[0], seed[1], 0] for seed in seeds]
        # ----------------------------------------------------------------------
        # make a mesh
        # ----------------------------------------------------------------------
        Mesh.default_vertex_attributes = dva
        Mesh.default_edge_attributes = dea
        Mesh.default_face_attributes = dfa
        mesh = Mesh.from_vertices_and_faces(seeds, simplices)
        # ----------------------------------------------------------------------
        # unify the cycle directions of the mesh
        # ----------------------------------------------------------------------
        mesh_unify_cycle_directions(mesh)
        # ----------------------------------------------------------------------
        # unify the cycle directions of the mesh
        # ----------------------------------------------------------------------
        if do_smooth:
            mesh_smooth(mesh, k=k)
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        profile.disable()
        stream = cStringIO.StringIO()
        stats = pstats.Stats(profile, stream=stream)
        stats.strip_dirs()
        stats.sort_stats(1)
        stats.print_stats(20)
        out_dict['profile'] = stream.getvalue()
        out_dict['data'] = {'data': mesh.to_data()}
    except:
        out_dict['data'] = None
        out_dict['error'] = traceback.format_exc()
        out_dict['iterations'] = None
        out_dict['profile'] = None

    with open(out_path, 'wb+') as f:
        json.dump(out_dict, f)
