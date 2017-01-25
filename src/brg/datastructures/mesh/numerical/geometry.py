from numpy import array
from numpy import meshgrid
from numpy import linspace
from numpy import amax
from numpy import amin

from scipy.interpolate import griddata

import matplotlib.pyplot as plt


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


def mesh_contours(mesh, N=50):
    xyz = array([mesh.vertex_coordinates(key) for key in mesh])
    x = xyz[:, 0]
    y = xyz[:, 1]
    z = xyz[:, 2]
    X, Y = meshgrid(
        linspace(amin(x), amax(x), N),
        linspace(amin(y), amax(y), N)
    )
    Z = griddata((x, y), z, (X, Y), method='cubic')
    ax = plt.figure(aspect='equal').add_subplot(111)
    c = ax.contour(X, Y, Z, N)
    plt.show()
    # contours = [0] * len(c.collections)
    # for i, collection in enumerate(iter(c.collections)):
    #     paths = collection.get_paths()
    #     contours[i] = [0] * len(paths)
    #     for j, path in enumerate(iter(paths)):
    #         polygons = path.to_polygons()
    #         contours[i][j] = [0] * len(polygons)
    #         for k, polygon in enumerate(iter(polygons)):
    #             contours[i][j][k] = polygon.tolist()


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

    distances = [distance_point_point(point, centroid) for point in points]

    print distances

    mesh.plot()
