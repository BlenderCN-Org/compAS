import random

from brg.datastructures.mesh import Mesh
from brg.datastructures.mesh.operations import swap_edge_trimesh as swap_edge

from brg.geometry import centroid_points
from brg.geometry import distance_point_point
from brg.geometry import add_vectors
from brg.geometry import bounding_box

from brg.geometry.planar import is_point_in_polygon_2d
from brg.geometry.planar import is_point_in_triangle_2d
from brg.geometry.planar import is_point_in_circle_2d
from brg.geometry.planar import circle_from_points_2d


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'delaunay_from_points',
]


def _super_triangle(coords):
    centpt = centroid_points(coords)
    bbpts  = bounding_box(coords)
    dis    = distance_point_point(bbpts[0], bbpts[2])
    dis    = dis * 300
    v1     = (0 * dis, 2 * dis, 0)
    v2     = (1.73205 * dis, -1.0000000000001 * dis, 0)  # due to numerical issues
    v3     = (-1.73205 * dis, -1 * dis, 0)
    pt1    = add_vectors(centpt, v1)
    pt2    = add_vectors(centpt, v2)
    pt3    = add_vectors(centpt, v3)
    return pt1, pt2, pt3


def delaunay_from_points(points, polygon=None, polygons=None, cls=None):
    """Computes the delaunay triangulation for a list of points.

    Parameters:
        points (sequence of tuple): XYZ coordinates of the original points.
        polygon (sequence of tuples): list of ordered points describing the outer boundary (optional)
        polygons (list of sequences of tuples): list of polygons (ordered points describing internal holes (optional)

    Returns:
        list of lists: list of faces (face = list of vertex indices as integers)

    References:
        Sloan, S. W. (1987) A fast algorithm for constructing Delaunay triangulations in the plane

    Example:

        .. plot::
            :include-source:

            import brg
            from brg.datastructures.mesh import Mesh
            from brg.datastructures.mesh.algorithms import delaunay_from_points

            mesh = Mesh.from_obj(brg.get_data('faces.obj'))

            vertices = [mesh.vertex_coordinates(key) for key in mesh]
            faces = delaunay_from_points(vertices)

            delaunay = Mesh.from_vertices_and_faces(vertices, faces)

            delaunay.plot(
                vertexsize=0.1
            )

    """
    if cls:
        mesh = cls()
    else:
        mesh = Mesh()

    # to avoid numerical issues for perfectly structured point sets
    tiny = 1e-8
    pts  = [(point[0] + random.uniform(-tiny, tiny), point[1] + random.uniform(-tiny, tiny), 0.0) for point in points]

    # create super triangle
    pt1, pt2, pt3 = _super_triangle(points)

    # add super triangle vertices to mesh
    n = len(points)
    super_keys = n, n + 1, n + 2

    mesh.add_vertex(super_keys[0], {'x': pt1[0], 'y': pt1[1], 'z': pt1[2]})
    mesh.add_vertex(super_keys[1], {'x': pt2[0], 'y': pt2[1], 'z': pt2[2]})
    mesh.add_vertex(super_keys[2], {'x': pt3[0], 'y': pt3[1], 'z': pt3[2]})

    mesh.add_face(super_keys)

    # iterate over points
    for i, pt in enumerate(pts):
        key = i

        # draw_light(mesh,temp = False)
        fkeys = mesh.faces()

        # check in which triangle this point falls
        for fkey in fkeys:
            # abc = mesh.face_coordinates(fkey) #This is slower
            # This is faster:
            keya, keyb, keyc = mesh.face_vertices(fkey)

            dicta = mesh.vertex[keya]
            dictb = mesh.vertex[keyb]
            dictc = mesh.vertex[keyc]

            a = [dicta['x'], dicta['y']]
            b = [dictb['x'], dictb['y']]
            c = [dictc['x'], dictc['y']]

            if is_point_in_triangle_2d(pt, [a, b, c]):
                # generate 3 new triangles (faces) and delete surrounding triangle
                newtris = mesh.insert_vertex(fkey, key=key, xyz=pt)
                break

        while newtris:
            fkey = newtris.pop()

            # get opposite_face
            keys  = mesh.face_vertices(fkey)
            s     = list(set(keys) - set([key]))
            u, v  = s[0], s[1]
            fkey1 = mesh.halfedge[u][v]

            if fkey1 != fkey:
                fkey_op, u, v = fkey1, u, v
            else:
                fkey_op, u, v = mesh.halfedge[v][u], u, v

            if fkey_op:
                keya, keyb, keyc = mesh.face_vertices(fkey_op)
                dicta = mesh.vertex[keya]
                a = [dicta['x'], dicta['y']]
                dictb = mesh.vertex[keyb]
                b = [dictb['x'], dictb['y']]
                dictc = mesh.vertex[keyc]
                c = [dictc['x'], dictc['y']]

                circle = circle_from_points_2d(a, b, c)

                if is_point_in_circle_2d(pt, circle):
                    fkey, fkey_op = swap_edge(mesh, u, v)
                    newtris.append(fkey)
                    newtris.append(fkey_op)

    # Delete faces adjacent to supertriangle
    for key in super_keys:
        mesh.remove_vertex(key)

    # Delete faces outside of boundary
    if polygon:
        for fkey in mesh.faces():
            cent = mesh.face_centroid(fkey)
            if not is_point_in_polygon_2d(cent, polygon):
                mesh.delete_face(fkey)

    # Delete faces inside of inside boundaries
    if polygons:
        for polygon in polygons:
            for fkey in mesh.faces():
                cent = mesh.face_centroid(fkey)
                if is_point_in_polygon_2d(cent, polygon):
                    mesh.delete_face(fkey)

    return [[int(key) for key in mesh.face_vertices(fkey, True)] for fkey in mesh.faces()]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import brg

    mesh = Mesh.from_obj(brg.get_data('faces.obj'))

    vertices = [mesh.vertex_coordinates(key) for key in mesh]
    faces = delaunay_from_points(vertices)

    delaunay = Mesh.from_vertices_and_faces(vertices, faces)

    delaunay.plot(
        vertexsize=0.1
    )
