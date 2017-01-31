from __future__ import print_function

from brg.geometry.basics import subtract_vectors
from brg.geometry.basics import add_vectors
from brg.geometry.basics import distance_point_point
from brg.geometry.basics import distance_point_point_sqrd
from brg.geometry.basics import length_vector
from brg.geometry.basics import vector_component
from brg.geometry.basics import cross
from brg.geometry.basics import dot
from brg.geometry.basics import center_of_mass_polygon
from brg.geometry.basics import angles_vectors
from brg.geometry.basics import length_vector_sqrd

from brg.geometry.transformations import normalize_vectors
from brg.geometry.transformations import scale_points



__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'sort_points',
    'bounding_box',
    'bounding_box_2d',
    'closest_point',
    'closest_point_on_line',
    'closest_point_on_segment',
    'closest_point_on_plane',
    'closest_point_on_polyline',
    'is_colinear',
    'is_coplanar',
    'is_convex',
    'is_point_on_plane',
    'is_point_on_line',
    'is_point_on_segment',
    'is_point_on_polyline',
    'is_point_in_triangle',
]


def sort_points(point, cloud):
    """Sorts points of a pointcloud to a point.

    Notes:
        Check kdTree class for an optimized implementation (MR).

    Parameters:
        point (tuple): x,y,z make_blocks point value
        cloud (sequence): A sequence locations in three-dimensional space.

    Returns:
        list (floats): min distances
        list (tuples): sorted points
        list (ints): closest point indices

    Examples:
        >>> sort_points()
    """
    minsq = [distance_point_point_sqrd(p, point) for p in cloud]
    return sorted(zip(minsq, cloud, range(len(cloud))), key=lambda x: x[0])


def bounding_box(points):
    """Computes the bounding box of a list of points.
    """
    x, y, z = zip(*points)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    min_z = min(z)
    max_z = max(z)
    return [(min_x, min_y, min_z),
            (max_x, min_y, min_z),
            (max_x, max_y, min_z),
            (min_x, max_y, min_z),
            (min_x, min_y, max_z),
            (max_x, min_y, max_z),
            (max_x, max_y, max_z),
            (min_x, max_y, max_z)]


def bounding_box_2d(points):
    x, y = zip(*points)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    return [(min_x, min_y),
            (max_x, min_y),
            (max_x, max_y),
            (min_x, max_y)]


def closest_point(point, cloud):
    """Calculates the closest point to a pointcloud.

    Notes:
        Check kdTree class for an optimized implementation (MR).

    Parameters:
        point (tuple): x,y,z make_blocks point value
        cloud (sequence): A sequence locations in three-dimensional space.

    Returns:
        float: min distance
        tuple: closest point
        int: closest point index
    """
    data = sort_points(point, cloud)
    return data[0]


def closest_point_on_line(p1, p2, tp):
    """
    Computes closest point on line (p1, p2) to testpoint.

    Parameters:
        p1, v1 (tuples): two 3d points defining the line
        tp (3-tuple): 3d testpoint

    Returns:
        (3-tuple): closest point on line
    """
    t = subtract_vectors(tp, p1)
    v = subtract_vectors(p2, p1)
    s = vector_component(t, v)
    return (p1[0] + s * v[0],
            p1[1] + s * v[1],
            p1[2] + s * v[2])


def closest_point_on_segment(p1, p2, tp):
    """
    Computes closest point on line segment (p1, p2) to testpoint.

    Parameters:
        p1, p2 (tuples): two 3d points defining the line segment
        tp (3-tuple): 3d testpoint

    Returns:
        (3-tuple): closest point on line segment
    """
    p  = closest_point_on_line(p1, p2, tp)
    d  = distance_point_point_sqrd(p1, p2)
    d1 = distance_point_point_sqrd(p1, p)
    d2 = distance_point_point_sqrd(p2, p)
    if d1 > d or d2 > d:
        if d1 < d2:
            return p1
        return p2
    return p


def closest_point_on_polyline(points, tp):
    # should be straight forward using the closest_point_on_line_segment function
    raise NotImplementedError


def closest_point_on_plane(p0, n, p):
    """
    Computes closest point on plane (p1, v1) to testpoint.

    Warning:
        Not tested!

    Parameters:
        p0 (sequence) : XYZ coordinates of point on plane.
        n (sequence) : XYZ coordinates of normal vecor at point ``p0``.
        p (sequence) : XYZ coordinates of point in space.

    Returns:
        (3-tuple): Closest point on plane to given point in space.

    Examples:
        >>> closest_point_to_plane()

    References:
        `Wikipedia: Distance from a point to a plane <http://en.wikipedia.org/wiki/Distance_from_a_point_to_a_plane>`_

    Todo:
        - check if this is correct (compare to previous implementation).
    """
    n  = normalize_vectors([n])[0]
    d0 = n[0] * p[0] + n[1] * p[1] + n[2] * p[2] - (n[0] * p0[0] + n[1] * p0[1] + n[2] * p0[2])
    d  = d0 / length_vector(n)
    n  = scale_pointds([n], - d)[0]
    return add_vectors(p, n)


# ------------------------------------------------------------------------------
# queries
# ------------------------------------------------------------------------------


def is_colinear(a, b, c):
    """Verify if three points are colinear.

    Parameters:
        a (tuple, list, Point): Point 1.
        b (tuple, list, Point): Point 2.
        c (tuple, list, Point): Point 3.

    Returns:
        bool: True if the points are collinear, False otherwise.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1])  * (c[0] - a[0]) == 0


def is_coplanar(points, tol=0.01):
    """Verify if the points are coplanar.

    Compute the normal vector (cross product) of the vectors formed by the first
    three points. Include one more vector at a time to compute a new normal and
    compare with the original normal. If their cross product is not zero, they
    are not parallel, which means the point are not in the same plane.

    Four points are coplanar if the volume of the tetrahedron defined by them is
    0. Coplanarity is equivalent to the statement that the pair of lines
    determined by the four points are not skew, and can be equivalently stated
    in vector form as (x2 - x0).[(x1 - x0) x (x3 - x2)] = 0.

    Parameters:
        points (sequence): A sequence of locations in three-dimensional space.

    Returns:
        bool: True if the points are coplanar, False otherwise.

    """
    tol2 = tol ** 2
    if len(points) == 4:
        v01 = (points[1][0] - points[0][0], points[1][1] - points[0][1], points[1][2] - points[0][2],)
        v02 = (points[2][0] - points[0][0], points[2][1] - points[0][1], points[2][2] - points[0][2],)
        v23 = (points[3][0] - points[2][0], points[3][1] - points[2][1], points[3][2] - points[2][2],)
        res = dot(v02, cross(v01, v23))
        return res**2 < tol2
    # len(points) > 4
    # compare length of cross product vector to tolerance
    u = [points[1][i] - points[0][i] for i in range(3)]
    v = [points[2][i] - points[1][i] for i in range(3)]
    w = cross(u, v)
    for i in range(1, len(points) - 2):
        u = v
        v = [points[i + 2][j] - points[i + 1][j] for j in range(3)]
        wuv = cross(w, cross(u, v))
        if wuv[0]**2 > tol2 or wuv[1]**2 > tol2 or wuv[2]**2 > tol2:
            return False
    return True


def is_convex(points):
    c = center_of_mass_polygon(points)
    for i in range(-1, len(points) - 1):
        p0 = points[i]
        p1 = points[i - 1]
        p2 = points[i + 1]
        v0 = (c[0] - p0[0], c[1] - p0[1], c[2] - p0[2])
        v1 = (p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2])
        v2 = (p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2])
        a1, _ = angles_vectors(v1, v0)
        a2, _ = angles_vectors(v0, v2)
        if a1 + a2 > 180:
            return False
    return True


def is_point_on_plane(point, plane):
    """Verify if a point lies in a plane.

    Parameters:
        point (Point): A ``Point`` object.
        plane (Plane): A ``Plane`` object.
    """
    pass


def is_point_on_line(p1, v1, tp, tol=0):
    """Verify if a point (tp) is on line (p1, v1) within a tolerance (tol).

    Parameters:
        p1, v1 (tuples): 3d point and 3d vector of line
        tp (3-tuple): 3d make_blocks point
        tol (float): tolerance distance

    Returns:
        (bool): True if the point is in on the line, False otherwise.

    Todo:
        - can be done much simpler by using the algorithm used in is_point_on_line_segment

    """
    pt2 = closest_point_on_line(p1, v1, tp)
    if pt2 is None:
        return
    if distance_point_point(tp, pt2) <= tol:
        return True
    return False


def is_closest_point_on_segment(p1, p2, tp, result=True):
    """
    Verify if the closest point on a line is on line segment (p1, p2) for a testpoint tp.

    Parameters:
        p1, p2 (tuples): two 3d points defining the line segment
        tp (3-tuple): 3d testpoint
        result (bool):  if True the closest point is returned if there is a closest point
                        if False, True is returned if there is a closest point

    Returns:
        (bool/tuple): the point if the point is in on the line, False otherwise.
        (bool): True if the point is in on the line, False otherwise.

    """
    v1 = subtract_vectors(p1, p2)
    d = length_vector_sqrd(v1)
    if d == 0:
        return
    dis = distance_point_point_sqrd(p1, p2)
    u = ((tp[0] - p1[0]) * v1[0] + (tp[1] - p1[1]) * v1[1] + (tp[2] - p1[2]) * v1[2]) / float(d)
    onlinept = (p1[0] + u * v1[0], p1[1] + u * v1[1], p1[2] + u * v1[2])
    disp1 = distance_point_point_sqrd(p1, onlinept)
    disp2 = distance_point_point_sqrd(p2, onlinept)
    if disp1 > dis or disp2 > dis:
        return False
    if result:
        return onlinept
    return True


def is_point_on_segment(p1, p2, tp, tol=0.0001):
    a = distance_point_point(p1, p2)
    b = distance_point_point(p1, tp)
    c = distance_point_point(p2, tp)
    s = 0.5 * (a + b + c)
    if a == 0:
        return False
    ha = abs((2 / a) * (s * (s - a) * (s - b) * (s - c))) ** 0.5
    if ha < tol and (b < a + tol and c < a + tol):
        return True
    return False


def is_point_on_polyline(points, tp, tol=0):
    for i in xrange(len(points) - 1):
        clospt = closest_point_on_segment(points[i], points[i + 1], tp)
        if distance_point_point(clospt, tp) <= tol:
            return True
    return False


def is_point_in_triangle(p, abc):
    """Verify if a point (p) is inside line of the triangle abc.

    Parameters:
        p (tuple): 3d point
        abc (tuples): 3d triangle points

    Returns:
        (bool): True if the point is in inside the triangle, False otherwise.
    """
    def is_on_same_side(p1, p2, a, b):
        v = subtract_vectors(b, a)
        cp1 = cross(v, subtract_vectors(p1, a))
        cp2 = cross(v, subtract_vectors(p2, a))
        if dot(cp1, cp2) >= 0:
            return True
        else:
            return False
    a, b, c = abc
    if is_on_same_side(p, a, b, c) and is_on_same_side(p, b, a, c) and is_on_same_side(p, c, a, b):
        return True
    return False


# def is_point_in_polygon(points,tp):
#     """Verify if a point is in the interior of a polygon.

#     Note:
#         This test only makes sense in the x/y plane

#     Parameters:
#         points (Polygon): list of ordered points.
#         tp (3-tuple): 3d test point

#         not implemented:
#             include_boundary (bool): Should the boundary be included in the test?
#                 Defaults to False.
#             A tolerance value would be nice too... float errors are problematic
#             points which are located on the boundary are not always uniquely defines as inside/outside

#     Returns:
#         bool: True if the point is in the polygon, False otherwise.
#     """
#     x,y = tp[0],tp[1]

#     points = [(pt[0],pt[1]) for pt in points]# make 2D

#     n = len(points)
#     inside =False
#     p1x,p1y = points[0]
#     for i in range(n+1):
#         p2x,p2y = points[i % n]
#         if y > min(p1y,p2y):
#             if y <= max(p1y,p2y):
#                 if x <= max(p1x,p2x):
#                     if p1y != p2y:
#                         xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
#                     if p1x == p2x or x <= xinters:
#                         inside = not inside
#         p1x,p1y = p2x,p2y
#     return inside


# def is_point_in_circle(pt1,pt2,pt3, tp):
#     centPt, radius = circle_from_points_2d(pt1,pt2,pt3)
#     #    if not temp:
#     #        return False
#     #    centPt, radius = temp
#     #    rs.AddCircle((centPt[0],centPt[1],0),radius)

#     if is_point_in_rectangle(centPt, radius, tp):
#         dx = centPt[0] - tp[0]
#         dy = centPt[1] - tp[1]
#         dx *= dx
#         dy *= dy
#         distanceSquared = dx + dy
#         radiusSquared = radius * radius
#         return distanceSquared <= radiusSquared
#     return False


# #needed in is_point_in_circle
# def circle_from_points_2d(pt1,pt2,pt3):
#     ax =pt1[0]
#     ay = pt1[1]  #first Point X and Y
#     bx =pt2[0]
#     by = pt2[1]   #Second Point X and Y
#     cx =pt3[0]
#     cy =pt3[1]   #Third Point X and Y
#     #****************Following are Basic Procedure**********************///
#     x1 = (bx + ax) / 2
#     y11 = (by + ay) / 2
#     dy1 = bx - ax
#     dx1 = -(by - ay)
#     #***********************
#     x2 = (cx + bx) / 2
#     y2 = (cy + by) / 2
#     dy2 = cx - bx
#     dx2 = -(cy - by)
#     #****************************
#     try:
#         ox = (y11 * dx1 * dx2 + x2 * dx1 * dy2 - x1 * dy1 * dx2 - y2 * dx1 * dx2)/ (dx1 * dy2 - dy1 * dx2)
#         oy = (ox - x1) * dy1 / dx1 + y11
#     except:
#         return None,None
#     #***********************************
#     dx = ox - ax
#     dy = oy - ay
#     radius = (dx * dx + dy * dy)**0.5
#     return (ox,oy,0),radius


# #needed in is_point_in_circle
# def is_point_in_rectangle(centPt, radius, testPt):
#     return testPt[0] >= centPt[0] - radius and testPt[0] <= centPt[0] + radius and testPt[1] >= centPt[1] - radius and testPt[1] <= centPt[1] + radius


# def is_ray_intersecting_triangle(p1, v1, a, b, c):
#     """
#     Computes the intersection of a ray (p1,v1) and a triangle (a,b,c)
#     based on Moeller Trumbore intersection algorithm

#     Parameters:
#         p1, v1 (tuples): 3d point and 3d vector of line
#         a,b,c (list of 3-tuples): 3d points of triangle

#     Returns:
#         (bool): True if the ray intersects with the triangle, False otherwise.
#     """
#     EPSILON = 0.000000001
#     # Find vectors for two edges sharing V1
#     e1 = subtract_vectors(b, a)
#     e2 = subtract_vectors(c, a)
#     # Begin calculating determinant - also used to calculate u parameter
#     p = cross(v1, e2)
#     # if determinant is near zero, ray lies in plane of triangle
#     det = dot(e1, p)
#     # NOT CULLING
#     if(det > - EPSILON and det < EPSILON):
#         return False
#     inv_det = 1.0 / det
#     # calculate distance from V1 to ray origin
#     t = subtract_vectors(p1, a)
#     # Calculate u parameter and make_blocks bound
#     u = dot(t, p) * inv_det
#     # The intersection lies outside of the triangle
#     if(u < 0.0 or u > 1.0):
#         return False
#     # Prepare to make_blocks v parameter
#     q = cross(t, e1)
#     # Calculate V parameter and make_blocks bound
#     v = dot(v1, q) * inv_det
#     # The intersection lies outside of the triangle
#     if(v < 0.0 or u + v  > 1.0):
#         return False
#     t = dot(e2, q) * inv_det
#     if(t > EPSILON):
#         return True
#     # No hit, no win
#     return False


# def is_line_line_intersection_2d(p1, v1, p2, v2, points=False):
#     """Verify if two lines intersect in 2d on the xy plane.

#     Parameters:
#         p1, v1 (tuples): 3d point and 3d vector of line A
#         p2, v2 (tuples): 3d point and 3d vector of line B
#         points (bool): if True v1,v2 will be interpreted as end points of the lines
#     Returns:
#         (bool): True if there is a intersection, False otherwise.

#     """
#     if points:
#         p1b = v1
#         p2b = v2
#     else:
#         p1b = add_vectors(p1, v1)
#         p2b = add_vectors(p2, v2)
#     d = (p2b[1] - p2[1]) * (p1b[0] - p1[0]) - (p2b[0] - p2[0]) * (p1b[1] - p1[1])
#     if d == 0:
#         return False
#     return True


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from random import randint

    cloud = [[float(randint(0, 1000)), float(randint(0, 1000)), 0.0] for x in range(100)]

    s = sort_points([0, 0, 0], cloud)

    print(s)
