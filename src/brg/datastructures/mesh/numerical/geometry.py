
from brg.numerical.geometry import contours_scalarfield
from brg.numerical.geometry import plot_contours_scalarfield


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_contours',
    'plot_mesh_contours',
    'mesh_isolines',
    'plot_mesh_isolines',
]


def mesh_contours(mesh, N=50):
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh]
    z = [mesh.vertex_coordinates(key, 'z') for key in mesh]
    return contours_scalarfield(xy, z, N)


def plot_mesh_contours(mesh, N=50):
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh]
    z = [mesh.vertex_coordinates(key, 'z') for key in mesh]
    plot_contours_scalarfield(xy, z, N)


def mesh_isolines(mesh, attr_name, N=50):
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh]
    s = [mesh.vertex[key][attr_name] for key in mesh]
    return contours_scalarfield(xy, s, N)


def plot_mesh_isolines(mesh, attr_name, N=50):
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh]
    s = [mesh.vertex[key][attr_name] for key in mesh]
    plot_contours_scalarfield(xy, s, N)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg
    from brg.datastructures.mesh import Mesh
    from brg.geometry import centroid_points
    from brg.geometry import distance_point_point

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    points = [mesh.vertex_coordinates(key) for key in mesh]
    centroid = centroid_points(points)

    for key, attr in mesh.vertices_iter(True):
        xyz = mesh.vertex_coordinates(key)
        attr['d'] = distance_point_point(xyz, centroid)

    mesh.plot()

    plot_mesh_isolines(mesh, 'd')
