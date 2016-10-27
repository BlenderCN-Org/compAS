"""This module defines a ``Polygon`` object

..  Copyright 2014 BLOCK Research Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        `http://www.apache.org/licenses/LICENSE-2.0`_

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

from brg.geometry.point import Point
from brg.geometry.vector import Vector
from brg.geometry.line import Line

from brg.geometry.functions import centroid
from brg.geometry.functions import center_of_mass
from brg.geometry.functions import is_convex
from brg.geometry.functions import is_coplanar
from brg.geometry.functions import area
from brg.geometry.functions import cross


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '29.09.2014'
__contact__    = """ETH Zurich,
Institute for Technology in Architecture,
BLOCK Research Group,
Stefano-Franscini-Platz 5,
HIL H 47,
8093 Zurich, Switzerland
"""


class PolygonException(Exception):
    pass


class Polygon(object):
    """An object representing ...

    A ``Polygon`` has a closed boundary that separates its interior from the
    exterior. The boundary does not intersect itself, and is described by an
    ordered set of of points.

    Note:
        All ``Polygon`` objects are considered closed. Therefore the first and
        last element in the list of points are not the same. The existence of the
        closing edge is implied.

    Parameters:
        points (sequence): A sequence of XYZ coordinates.

    Attributes:
        points (list): A list of ``Point`` objects.
        lines (list): A list of ``Line`` objects.
        length (float): The total length of the boundary.
        centroid (Point): A ``Point`` object at the location of the centroid.
        area (float): The size of the area enclosed by the boundary.

    Examples:
        >>> polygon = Polygon([[0,0,0], [1,0,0], [1,1,0], [0,1,0]])
        >>> polygon.centroid
        [0.5, 0.5, 0.0]
        >>> polygon.area
        1.0

    """
    def __init__(self, points):
        self._lines = None
        self.points = points

    @property
    def points(self):
        """The points of the polygon.

        Parameters:
            points (sequence): A sequence of XYZ coordinates.

        Returns:
            list: A list of ``Point`` objects.
        """
        return self._points

    @points.setter
    def points(self, points):
        if points[-1] == points[0]:
            del points[-1]
        self._points = [Point(xyz) for xyz in points]
        self._lines  = [Line(self._points[i], self._points[i + 1]) for i in range(-1, len(points) - 1)]

    @property
    def lines(self):
        """The lines of the polygon."""
        return self._lines

    @property
    def length(self):
        """The length of the boundary."""
        return sum([line.length for line in self._lines])

    @property
    def centroid(self):
        """The centroid of the polygon."""
        return Point(centroid(self.points))

    @property
    def normal(self):
        """The (average) normal of the polygon."""
        o = self.center
        points = self.points
        a2 = 0
        normals = []
        for i in range(-1, len(points) - 1):
            p1  = points[i]
            p2  = points[i + 1]
            u   = [p1[_] - o[_] for _ in range(3)]
            v   = [p2[_] - o[_] for _ in range(3)]
            w   = cross(u, v)
            a2 += sum(w[_] ** 2 for _ in range(3)) ** 0.5
            normals.append(w)
        n = [sum(axis) / a2 for axis in zip(*normals)]
        n = Vector(n)
        return n

    @property
    def tangent(self):
        """The (average) tangent plane."""
        o = self.center
        a, b, c = self.normal
        d = - (a * o.x + b * o.y + c * o.z)
        return a, b, c, d

    @property
    def frame(self):
        """The local coordinate frame."""
        o = self.center
        w = self.normal
        p = self.points[0]
        u = Vector(p, o)
        u.normalize()
        v = w.cross(u)
        return o, u, v, w

    @property
    def center(self):
        """The center (of mass) of the polygon."""
        return Point(center_of_mass(self.points))

    @property
    def area(self):
        """The area of the polygon.

        The area is computed as the sum of the areas of the triangles formed
        by each of the lines of the boundary and the centroid.
        """
        return area(self.points)

    def is_convex(self):
        return is_convex(self.points)

    def is_coplanar(self):
        return is_coplanar(self.points)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    polygon = Polygon([[1, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0]])

    print polygon.centroid
    print polygon.center
    print polygon.area
    print polygon.length
    print polygon.normal
    print polygon.frame

    print polygon.is_convex()
    print polygon.is_coplanar()
