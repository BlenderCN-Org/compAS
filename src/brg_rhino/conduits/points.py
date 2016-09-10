# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

import Rhino
import scriptcontext as sc

from Rhino.Geometry import Point3d
from Rhino.Display.PointStyle import Simple

from System.Collections.Generic import List
from System.Drawing.Color import FromArgb


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'Apache License, Version 2.0'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 14, 2014'


class PointsConduit(Rhino.Display.DisplayConduit):
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
        pconduit = PointsConduit(points)
        pconduit.Enabled = True

        for i in range(100):
            pconduit.points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]

            sc.doc.Views.Redraw()
            Rhino.RhinoApp.Wait()

            time.sleep(0.1)

    except Exception as e:
        print e

    finally:
        pconduit.Enabled = False
        del pconduit
