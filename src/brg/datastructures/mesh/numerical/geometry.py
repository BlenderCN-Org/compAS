
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
    """Compute the contours of the mesh.

    The contours are defined as the isolines of the z-coordinates of the vertices
    of the mesh.

    Parameters:
        mesh (:class:`brg.datastructures.mesh.Mesh`): The mesh object.
        N (int): Optional. The density of the contours. Default is ``50``.

    Returns:
        tuple: A tuple of a list of levels and a list of contours.

        The list of levels contains the z-values at each of the contours.
        Each contour is a list of paths, and each path is a list polygons.

    Examples:
        >>> mesh = Mesh.from_obj('saddle.obj', sample=True)
        >>> levels, contours = mesh_contours(mesh)
        >>> for level, contour in zip(levels, contours):
        ...     print level, contour
        ...

    See Also:
        :func:`brg.numerical.geometry.contours_scalarfield`

    """
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh]
    z = [mesh.vertex_coordinates(key, 'z') for key in mesh]
    return contours_scalarfield(xy, z, N)


def plot_mesh_contours(mesh, N=50):
    """Plot the contours of a mesh.

    Parameters:
        mesh (:class:`brg.datastructures.mesh.Mesh`): The mesh object.
        N (int): The density of the plot.

    Examples:
        >>> mesh = Mesh.from_obj('saddle.obj', sample=True)
        >>> plot_mesh_contours(mesh)

    .. plot::

        import brg
        from brg.datastructures.mesh import Mesh
        mesh = Mesh.from_obj(brg.get_data('saddle.obj'))
        plot_mesh_contours(mesh)

    See Also:
        :func:`brg.numerical.geometry.plot_contours_scalarfield`

    """
    xy = [mesh.vertex_coordinates(key, 'xy') for key in mesh]
    z = [mesh.vertex_coordinates(key, 'z') for key in mesh]
    plot_contours_scalarfield(xy, z, N)


def mesh_isolines(mesh, attr_name, N=50):
    """Compute the isolines of a specified attribute of the mesh.

    Parameters:
        mesh
        attr_name
        N

    Returns:
        tuple: A tuple of a list of levels and a list of isolines.

        The list of levels contains the z-values at each of the isolines.
        Each isoline is a list of paths, and each path is a list polygons.

    Examples:
        >>>

    See Also:
        :func:`brg.numerical.geometry.isolines_scalarfield`

    """
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
