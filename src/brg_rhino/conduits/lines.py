# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

from brg_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Line

    from System.Collections.Generic import List
    from System.Drawing.Color import FromArgb

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 14, 2014'


__all__ = [
    'LinesConduit',
]


class LinesConduit(Conduit):
    """"""
    def __init__(self, points, lines, thickness=3, color=None):
        super(LinesConduit, self).__init__()
        self.points = points
        self.lines = lines
        self.n = len(lines)
        self.thickness = thickness
        color = color or (255, 0, 0)
        self.color = FromArgb(*color)

    def DrawForeground(self, e):
        lines = List[Line](self.n)
        for i, j in self.lines:
            sp = self.points[i]
            ep = self.points[j]
            lines.Add(Line(Point3d(*sp), Point3d(*ep)))
        e.Display.DrawLines(lines, self.color, self.thickness)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from random import randint
    import time

    points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
    lines  = [(i, i + 1) for i in range(99)]

    try:
        conduit = LinesConduit(points, lines)
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
