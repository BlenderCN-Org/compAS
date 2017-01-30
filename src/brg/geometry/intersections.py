from brg.geometry.basics import distance_point_point
from brg.geometry.basics import add_vectors
from brg.geometry.basics import subtract_vectors
from brg.geometry.basics import dot
from brg.geometry.basics import cross


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'line_line_intersection',
    'line_line_intersection_2d',
    'lines_intersection',
    'lines_intersection_2d',
    'circle_circle_intersections',
    'circle_circle_intersections_2d',
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

    """
    d = distance_point_point(p1, p2)
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


def is_ray_intersecting_triangle(p1, v1, a, b, c):
     """
     Computes the intersection of a ray (p1,v1) and a triangle (a,b,c)
     based on Moeller Trumbore intersection algorithm

     Parameters:
         p1, v1 (tuples): 3d point and 3d vector of line
         a,b,c (list of 3-tuples): 3d points of triangle

     Returns:
         t if the ray intersects with the triangle, False otherwise.
         the intersection point can be computed using t multiplied by v1 added to p1  
     """
     EPSILON = 0.000000001
     # Find vectors for two edges sharing V1
     e1 = subtract_vectors(b, a)
     e2 = subtract_vectors(c, a)
     # Begin calculating determinant - also used to calculate u parameter
     p = cross(v1, e2)
     # if determinant is near zero, ray lies in plane of triangle
     det = dot(e1, p)
     # NOT CULLING
     if(det > - EPSILON and det < EPSILON):
         return False
     inv_det = 1.0 / det
     # calculate distance from V1 to ray origin
     t = subtract_vectors(p1, a)
     # Calculate u parameter and make_blocks bound
     u = dot(t, p) * inv_det
     # The intersection lies outside of the triangle
     if(u < 0.0 or u > 1.0):
         return False
     # Prepare to make_blocks v parameter
     q = cross(t, e1)
     # Calculate V parameter and make_blocks bound
     v = dot(v1, q) * inv_det
     # The intersection lies outside of the triangle
     if(v < 0.0 or u + v  > 1.0):
         return False
     t = dot(e2, q) * inv_det
     if(t > EPSILON):
         return t
     # No hit
     return False


#to be checked and documented (name? are_boxes_intersecting)
#imports need to be checked
#input two lists of eight points each
#return true or false
def box_box_intersection(box_1,box_2):
    #box = 8 points (bottom: 0,1,2,3 top: 4,5,6,7)
    lines = [(bb1[0],bb1[1]),(bb1[1],bb1[2]),(bb1[2],bb1[3]),(bb1[3],bb1[0])]
    lines += [(bb1[4],bb1[5]),(bb1[5],bb1[6]),(bb1[6],bb1[7]),(bb1[7],bb1[4])]
    lines += [(bb1[0],bb1[4]),(bb1[1],bb1[5]),(bb1[2],bb1[6]),(bb1[3],bb1[7])]
    
    tris = [(bb2[0],bb2[1],bb2[2]),(bb2[0],bb2[2],bb2[3])]#bottom
    tris += [(bb2[4],bb2[5],bb2[6]),(bb2[4],bb2[6],bb2[7])]#top
    tris += [(bb2[0],bb2[4],bb2[7]),(bb2[0],bb2[7],bb2[3])]#side 1
    tris += [(bb2[0],bb2[1],bb2[5]),(bb2[0],bb2[5],bb2[4])]#side 2
    tris += [(bb2[1],bb2[2],bb2[6]),(bb2[1],bb2[6],bb2[5])]#side 3
    tris += [(bb2[2],bb2[3],bb2[7]),(bb2[2],bb2[7],bb2[6])]#side 4
    
    intx = False
    for pt1,pt2 in lines:
        for a,b,c in tris:
            for p1,p2 in [(pt1,pt2),(pt2,pt1)]:
                v1 = subtract_vectors(p2,p1)
                t = is_ray_intersecting_triangle(p1, v1, a, b, c)
                if t:
                    v1 = scale_points(v1, t)
                    test_pt = add_vectors([v1,p1])
                    if is_point_on_segment(p1, p2, test_pt, tol=0.0001):
                        intx = True
                        break
            else:
                continue
            break
        else:
            continue
        break
    return intx


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    
    
    
    import random
    import time
    
    x = random()
    y = random()
    z = random()
    box_a = [(0,0,0),(x,0,0),(x,y,0),(0,y,0)]
    box_a +=  [(0,0,z),(x,0,z),(x,y,z),(0,y,z)]
    
    box_b = [(0.5,0.5,0),(1.5,0.5,0),(1.5,1.5,0),(0.5,1.5,0)]
    box_b += [(0.5,0.5,1),(1.5,0.5,1),(1.5,1.5,1),(0.5,1.5,1)]
    
    
    print box_box_intersection(box_a,box_b)
    
    
    
    