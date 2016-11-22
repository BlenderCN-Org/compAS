"""This module defines a Spline as a composition of Bezier segments.


.. rubric:: References

.. [#wiki:binomial] `Binomial coefficient <http://en.wikipedia.org/wiki/Binomial_coefficient>`_
.. [#wiki:bernstein] `Bernstein polynomial <http://en.wikipedia.org/wiki/Bernstein_polynomial>`_
.. [#gist:bezdraw] `Draw Bezier curves using Python and PyQt <https://gist.github.com/Alquimista/1274149>`_
.. [#gist:bezier_curves] `Interactive Bezier curves with Python using just matplotlib <https://gist.github.com/Juanlu001/7284462>`_


..  Copyright 2014 Block Research Group
    
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

import os, sys
from math import factorial
from point import Point


__author__     = ['Tom Van Mele',]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 1, 2014'
__contact__    = """ETH Zurich, 
Institute for Technology in Architecture, 
Block Research Group, 
Stefano-Franscini-Platz 5, 
HIL H 47, 
8093 Zurich, Switzerland
"""


def binomial(n, k):
    """Returns the binomial coefficient of the :math:`x^k` term in the 
    polynomial expansion of the binmoial power :math:`(1 + x)^n`.
    
    Note:
        Arranging binomial coefficients into rows for successive values of `n`, 
        and in which `k` ranges from 0 to `n`, gives a triangular array known as 
        Pascal's triangle [#wiki:binomial]_
    
    Parameters:
        n (int): The number of terms.
        k (int): The index of the coefficient.
    
    Returns:
        int: The coefficient.
    """
    return factorial(n) / float(factorial(k) * factorial(n-k))

def bernstein(n, k, t):
    """k:sup:`th` of `n` + 1 Bernstein basis polynomials of degree `n`. A 
    weighted linear combination of these basis polynomials is called a Bernstein
    polynomial [#wiki:bernstein]_.
    
    Note:
        When constructing Bezier curves, the weights are simply the coordinates 
        of the control points of the curve.
        
    Parameters:
        n (int): The degree of the polynomial.
        k (int): The number of the basis polynomial.
        t (float): The variable.
    
    Returns:
        float: The value of the Bernstein basis polynomial at `t`.
    """
    return binomial(n, k) * t ** k * (1 - t) ** (n - k) 
   

class BezierException(Exception):
    pass


class Bezier(object):
    """A Bezier curve.
    
    A Bezier curve of degree `n` is a linear combination of `n` + 1 Bernstein 
    basis polynomials of degree `n`.
    
    Parameters:
        points (sequence): A sequence of control points, represented by their 
            location in 3D space.
    
    Attributes:
        points (list): The control points.
        degree (int): The degree of the curve.
    """  
    def __init__(self, points):
        self._points = []
        self.points = points
    
    @property
    def points(self):
        """The control points.
        
        Parameters:
            points (sequence): A sequence of control point locations in 3d space.
        
        Returns:
            list: A list of ``Point`` objects.
        """
        return self._points
    
    @points.setter
    def points(self, points):
        if points:
            self._points = [Point(point) for point in points]
    
    @property 
    def degree(self):
        """The degree of the curve."""
        return len(self.points) - 1
    
    def compute_point(self, t):
        """Compute a point on the curve.
        
        Parameters:
            t (float): The value of the curve parameter. Must be between 0 and 1.
        
        Returns:
            Point: the corresponding point on the curve.
        """
        n = self.degree
        point = Point([0, 0, 0])
        for i, p in enumerate(self.points):
            b = bernstein(n, i, t)
            point += p * b 
        return point
    
    def compute_locus(self, resolution=100):
        """Compute the locus of all points on the curve.
        
        Parameters:
            resolution (int): The number of intervals at which a point on the 
                curve should be computed. Defaults to 100.
        
        Returns:
            list: 
        """
        locus = []
        divisor = float(resolution - 1)
        for i in range(resolution):
            t = i/divisor
            locus.append(self.compute_point(t))
        return locus
    
    def draw(self):
        import matplotlib.pyplot as plt
        locus = self.compute_locus()
        x, y, _ = zip(*locus)
        plt.plot(x, y)
        ax = plt.gca()
        ax.set_aspect('equal')
        plt.show()
        

class SplineException(Exception):
    pass


class Spline(object):
    """"""
    def __init__(self):
        self.segments = []
        

class NURBSException(Exception):
    pass


class NURBS(object):
    """"""
    pass
    

#===============================================================================
# Debugging
#===============================================================================

if __name__ == '__main__':
    spline = Bezier([[0,0,0], [1,-3,0], [2,+3,0], [3,0,0]])
    spline.draw()

