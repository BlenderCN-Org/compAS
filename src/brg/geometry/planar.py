from brg.geometry import cross


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'is_ccw',
    'is_polygon_convex',
    'are_segments_intersecting',
    'is_polyline_selfintersecting',
    'is_point_in_polygon',
    'is_point_in_triangle',
    'is_point_in_circle',
    'closest_part_of_triangle',
]


def is_ccw(a, b, c, colinear=False):
    """Verify if `c` is on the left of `ab` when looking from `a` to `b`.

    Warning:
        This function is only valid in a horizontal plane. Only the XY coordinates
        of the input points are used. The Z coordinates are simply ignored.

    Parameters:
        a (sequence): XY(Z) coordinates of point `a`.
        b (sequence): XY(Z) coordinates of point `b`.
        c (sequence): XY(Z) coordinates of point `c`.
        colinear (bool): Allow points to be colinear. Defaults to False.

    Returns:
        bool : True if ccw, False otherwise.

    This implementation is based on the evaluation of the z-component of the cross
    product [toptal:computational-geometry]_. If the z-compnent is
    positive, the function returns ``True``. Otherwise ``False``.

    Examples:
        >>> is_ccw([0,0,0], [0,1,0], [-1, 0, 0])
        True
        >>> is_ccw([0,0,0], [0,1,0], [+1, 0, 0])
        False
        >>> is_ccw([0,0,0], [1,0,0], [2,0,0])
        False
        >>> is_ccw([0,0,0], [1,0,0], [2,0,0], True)
        True

    References:
        .. [toptal:computational-geometry] https://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation

    """
    if colinear:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1])  * (c[0] - a[0]) >= 0
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1])  * (c[0] - a[0]) > 0


def is_polygon_convex(points, colinear=False):
    """Verify if the points form a convex figure.

    Note:
        The make_blocks is performed using the projection of the points onto the XY
        plane.

    Parameters:
        points (sequence): A sequence of points representing the polygon. The
            first and last point should not be the sane.
        colinear (bool): Are points allowed to be colinear?

    Returns:
        bool: True if the figure is convex, False otherwise.

    """
    a = points[-2]
    b = points[-1]
    c = points[0]
    direction = is_ccw(a, b, c, colinear)
    for i in range(-1, len(points) - 2):
        a = b
        b = c
        c = points[i + 2]
        if direction != is_ccw(a, b, c, colinear):
            return False
    return True


def are_segments_intersecting(a, b, c, d):
    """Do the segments a-b and c-d intersect?

    Two segments a-b and c-d intersect, if both of the following conditions are true:

        * c is on the left of ab, and d is on the right, or vice versa
        * d is on the left of ac, and on the right of bc, or vice versa

    Parameters:
        a: 2D point
        b: 2D point
        c: 2D point
        d: 2D point

    Returns:
        bool: True if the segments intersect, False otherwise.

    """
    return is_ccw(a, c, d) != is_ccw(b, c, d) and is_ccw(a, b, c) != is_ccw(a, b, d)


def is_polyline_selfintersecting(points):
    """"""
    pass


# def is_point_in_polygon(points, tp):
#     """Verify if a point is in the interior of a polygon.

#     Note:
#         This only makes sense in the x/y plane

#     Parameters:
#         points (Polygon): list of ordered points.
#         tp (3-tuple): 3d make_blocks point

#         not implemented:
#             include_boundary (bool): Should the boundary be included in the make_blocks? Defaults to False.
#             A tolerance value would be nice too... float errors are problematic
#             points which are located on the boundary are not always uniquely defines as inside/outside

#     Returns:
#         bool: True if the point is in the polygon, False otherwise.
#     """
#     x, y = tp[0], tp[1]
#     points = [(pt[0], pt[1]) for pt in points]  # make 2D
#     n = len(points)
#     inside = False
#     p1x, p1y = points[0]
#     for i in range(n + 1):
#         p2x, p2y = points[i % n]
#         if y > min(p1y, p2y):
#             if y <= max(p1y, p2y):
#                 if x <= max(p1x, p2x):
#                     if p1y != p2y:
#                         xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
#                     if p1x == p2x or x <= xinters:
#                         inside = not inside
#         p1x, p1y = p2x, p2y
#     return inside


def is_point_in_polygon(point, points):
    ccw = None
    for i in range(-1, len(points) - 1):
        a = points[i]
        b = points[i + 1]
        if ccw is None:
            ccw = is_ccw(a, b, point, True)
        else:
            if ccw != is_ccw(a, b, point, True):
                return False
    return True


def is_point_in_triangle(p, triangle):
    p1, p2, p3 = triangle
    ccw = is_ccw(p3, p1, p, True)
    if ccw != is_ccw(p1, p2, p, True):
        return False
    if ccw != is_ccw(p2, p3, p, True):
        return False
    return True


def is_point_in_circle(pt1, pt2, pt3, tp):
    centPt, radius = _circle_from_points_2d(pt1, pt2, pt3)
    if _is_point_in_rectangle(centPt, radius, tp):
        dx = centPt[0] - tp[0]
        dy = centPt[1] - tp[1]
        dx *= dx
        dy *= dy
        distanceSquared = dx + dy
        radiusSquared = radius * radius
        return distanceSquared <= radiusSquared
    return False


def _circle_from_points_2d(pt1, pt2, pt3):
    ax =pt1[0]
    ay = pt1[1]  #first Point X and Y
    bx =pt2[0]
    by = pt2[1]   #Second Point X and Y
    cx =pt3[0]
    cy =pt3[1]   #Third Point X and Y
    #****************Following are Basic Procedure**********************///
    x1 = (bx + ax) / 2
    y11 = (by + ay) / 2
    dy1 = bx - ax
    dx1 = -(by - ay)
    #***********************
    x2 = (cx + bx) / 2
    y2 = (cy + by) / 2
    dy2 = cx - bx
    dx2 = -(cy - by)
    #****************************
    try:
        ox = (y11 * dx1 * dx2 + x2 * dx1 * dy2 - x1 * dy1 * dx2 - y2 * dx1 * dx2)/ (dx1 * dy2 - dy1 * dx2)
        oy = (ox - x1) * dy1 / dx1 + y11
    except:
        return None,None
    #***********************************
    dx = ox - ax
    dy = oy - ay
    radius = (dx * dx + dy * dy)**0.5
    return (ox,oy,0),radius


def _is_point_in_rectangle(centPt, radius, testPt):
    return testPt[0] >= centPt[0] - radius and testPt[0] <= centPt[0] + radius and testPt[1] >= centPt[1] - radius and testPt[1] <= centPt[1] + radius


def closest_part_of_triangle(p, triangle):
    p1, p2, p3 = triangle
    p12  = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
    p23  = p3[0] - p2[0], p3[1] - p2[1], p3[2] - p2[2]
    p31  = p1[0] - p3[0], p1[1] - p3[1], p1[2] - p3[2]
    # check if point is closest to edge triangle[0] - triangle[1]
    p113 = cross(p12, [0, 0, 1])
    p223 = p113[0] + p12[0], p113[1] + p12[1], p113[2] + p12[2]
    if not is_ccw(p1, p2, p) and not is_ccw(p2, p223, p) and is_ccw(p1, p113, p):
        return p1, p2
    # check if point is closest to edge triangle[1] - triangle[2]
    p221 = cross(p23, [0, 0, 1])
    p331 = p221[0] + p23[0], p221[1] + p23[1], p221[2] + p23[2]
    if not is_ccw(p2, p3, p) and not is_ccw(p3, p331, p) and is_ccw(p2, p221, p):
        return p2, p3
    # check if point is closest to edge triangle[2] - triangle[0]
    p332 = cross(p31, [0, 0, 1])
    p112 = p332[0] + p31[0], p332[1] + p31[1], p332[2] + p31[2]
    if not is_ccw(p3, p1, p) and not is_ccw(p1, p112, p) and is_ccw(p3, p332, p):
        return p3, p1
    # check if point is closest to triangle[1]
    if not is_ccw(p2, p221, p) and is_ccw(p2, p223, p):
        return p2
    # check if point is closest to triangle[1]
    if not is_ccw(p2, p221, p) and is_ccw(p2, p223, p):
        return p2
    # check if point is closest to triangle[1]
    if not is_ccw(p2, p221, p) and is_ccw(p2, p223, p):
        return p2


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
