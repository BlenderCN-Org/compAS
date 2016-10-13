# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

from brg_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from Rhino.Display.PointStyle import Simple

    from System.Collections.Generic import List
    from System.Drawing.Color import FromArgb

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Oct 14, 2014'


docs = [
    'PointsConduit',
]


class PointsConduit(Conduit):
    """"""
    def __init__(self, points, radius=3, color=None):
        super(PointsConduit, self).__init__()
        self.points = points
        self.n = len(points)
        self.radius = radius
        color = color or (255, 0, 0)
        self.color = FromArgb(*color)

    def DrawForeground(self, e):
        points = List[Point3d](self.n)
        for xyz in self.points:
            points.Add(Point3d(*xyz))
        e.Display.DrawPoints(points, Simple, self.radius, self.color)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from random import randint
    import time

    points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]

    try:
        conduit = PointsConduit(points)
        conduit.Enabled = True

        for i in range(100):
            conduit.points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]

            conduit.redraw()

            time.sleep(0.1)

    except Exception as e:
        print e

    finally:
        conduit.Enabled = False
        del conduit
