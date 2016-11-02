from functions import distance
from arithmetic import add_vectors


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 3, 2014'


docs = [
    'line_line_intersection',
    'lines_intersection',
    'circle_circle_intersections',
]


def line_line_intersection():
    raise NotImplementedError


def line_line_intersection_2d(p1, v1, p2, v2, points=False):
    """Calculates the intersection point of line A and line B in 2d on the xy plane.

    Parameters:
        p1, v1 (tuples): 3d point and 3d vector of line A
        p2, v2 (tuples): 3d point and 3d vector of line B
        points (bool): if True v1,v2 will be interpreted as end points of the lines
    Returns:
        point (tuple): the intersection point if there is any
        None: if there is no intersection point
    """
    if points:
        p1b = v1
        p2b = v2
    else:
        p1b = add_vectors(p1, v1)
        p2b = add_vectors(p2, v2)
    d = (p2b[1] - p2[1]) * (p1b[0] - p1[0]) - (p2b[0] - p2[0]) * (p1b[1] - p1[1])
    if d == 0:
        return None
    n_a = (p2b[0] - p2[0]) * (p1[1] - p2[1]) - (p2b[1] - p2[1]) * (p1[0] - p2[0])
    ua = n_a / d
    return (p1[0] + (ua * (p1b[0] - p1[0])), p1[1] + (ua * (p1b[1] - p1[1])), 0)


def lines_intersection():
    raise NotImplementedError


def lines_intersection_2d():
    raise NotImplementedError


def circle_circle_intersections():
    raise NotImplementedError


def circle_circle_intersections_2d(p1, r1, p2, r2):
    """Calculates the intersection points of two circles in 2d on the xy plane.

    Parameters:
        p1 (tuples): 3d point of circle A
        r1 (float): radius of circle A
        p2 (tuples): 3d point of circle B
        r2 (float): radius of circle B

    Returns:
        points (list of tuples): the intersection points if there are any
        None: if there are no intersection points

    Examples:
        >>> circle_circle_intersections_2d
    """
    d = distance(p1, p2)
    if (d > r1 + r2):
        print 'No solutions, the circles are too far apart'
        return None
    if (d < abs(r1 - r2)):
        print 'No solutions, one circle contains the other'
        return None
    if ((d == 0) and (r1 == r2)):
        print 'No solutions, the circles coincide'
        return None
    a   = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h   = (r1 * r1 - a * a) ** 0.5
    cx2 = p1[0] + a * (p2[0] - p1[0]) / d
    cy2 = p1[1] + a * (p2[1] - p1[1]) / d
    i1  = ((cx2 + h * (p2[1] - p1[1]) / d), (cy2 - h * (p2[0] - p1[0]) / d), 0)
    i2  = ((cx2 - h * (p2[1] - p1[1]) / d), (cy2 + h * (p2[0] - p1[0]) / d), 0)
    return i1, i2


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
