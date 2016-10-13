from scipy.spatial import Delaunay

from brg.datastructures import Mesh

from brg.datastructures.mesh.algorithms.orientation import mesh_unify_cycle_directions
from brg.datastructures.mesh.algorithms.optimisation import mesh_smooth


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'GNU - General Public License'
__version__    = '0.0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '27.03.2014'


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
        config = in_dict['config']
        points = in_dict['points']
        # ----------------------------------------------------------------------
        tol       = config.get('tol', 0.001)
        do_smooth = config.get('do_smooth', False)
        dva       = config.get('dva', {})
        dea       = config.get('dea', {})
        dfa       = config.get('dfa', {})
        k         = config.get('k', 10)
        # ----------------------------------------------------------------------
        tri       = Delaunay([point[0:2] for point in points])
        simplices = tri.simplices.tolist()
        # ----------------------------------------------------------------------
        Mesh.default_vertex_attributes = dva
        Mesh.default_edge_attributes = dea
        Mesh.default_face_attributes = dfa
        mesh = Mesh.from_vertices_and_faces(points, simplices)
        mesh_unify_cycle_directions(mesh)
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
