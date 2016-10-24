# -*- coding: utf-8 -*-

from point import Point
from vector import Vector


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'
__date__       = 'Oct 6, 2014'


class Plane(object):
    """"""
    def __init__(self):
        self.point = None
        self.normal = None

    @classmethod
    def from_point_and_normal(cls, point, normal):
        plane = cls()
        plane.point = Point(point)
        plane.normal = Vector(normal).normalize()
        return plane

    @classmethod
    def from_point_and_vectors(cls, point, v1, v2):
        v1 = Vector(v1)
        v2 = Vector(v2)
        n  = v1.cross(v2)
        plane = cls()
        plane.point = Point(point)
        plane.normal = n.normalize()
        return plane

    @classmethod
    def from_points_and_vector(cls, p1, p2, vector):
        p1 = Point(p1)
        p2 = Point(p2)
        v1 = p2 - p1
        n  = v1.cross(vector)
        plane = cls()
        plane.point  = p1
        plane.normal = n.normalize()
        return plane

    @classmethod
    def from_three_points(cls, p1, p2, p3):
        p1 = Point(p1)
        p2 = Point(p2)
        p3 = Point(p3)
        v1 = p2 - p1
        v2 = p3 - p1
        plane = cls()
        plane.point  = p1
        plane.normal = v1.cross(v2)
        return plane

    def dihedral_angle(self, other):
        pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    plane = Plane.from_point_and_vectors([0, 0, 0], [1.0, 0, 0], [0, 1.0, 0])
    print plane.normal

    print plane.normal.x
    print plane.normal.y
    print plane.normal.z
