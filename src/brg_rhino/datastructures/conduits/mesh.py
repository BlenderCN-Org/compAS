# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

import System
import Rhino
import scriptcontext as sc

from Rhino.Geometry import Point3d
from Rhino.Geometry import Line

from System.Collections.Generic import List
from System.Drawing.Color import FromArgb

from brg_rhino.conduits import Conduit
from brg_rhino.ui.mouse import Mouse

from brg.geometry import length
from brg.geometry import cross


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'Apache License, Version 2.0'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 14, 2014'


class MeshConduit(Conduit):
    """"""
    def __init__(self, mesh, color=None):
        super(MeshConduit, self).__init__()
        self.mesh = mesh
        color = color or (255, 0, 0)
        self.color = FromArgb(*color)

    def DrawForeground(self, e):
        edges = self.mesh.edges()
        lines = List[Line](len(edges))
        for u, v in edges:
            sp = self.mesh.vertex_coordinates(u)
            ep = self.mesh.vertex_coordinates(v)
            lines.Add(Line(Point3d(*sp), Point3d(*ep)))
        e.Display.DrawLines(lines, self.color)


class MeshVertexInspector(Conduit):
    """"""
    def __init__(self, mesh, tol=0.1, dotcolor=None, textcolor=None):
        super(MeshVertexInspector, self).__init__()
        self.mesh      = mesh
        self.tol       = tol
        dotcolor       = dotcolor or (255, 0, 0)
        textcolor      = textcolor or (0, 0, 0)
        self.dotcolor  = FromArgb(*dotcolor)
        self.textcolor = FromArgb(*textcolor)
        self.mouse     = Mouse()

    def enable(self):
        self.mouse.Enabled = True
        self.Enabled = True

    def disable(self):
        self.mouse.Enabled = False
        self.Enabled = False

    def DrawForeground(self, e):
        p1  = self.mouse.p1
        p2  = self.mouse.p2
        v12 = [p2[i] - p1[i] for i in range(3)]
        l12 = length(v12)
        for key, attr in self.mesh.vertices_iter(True):
            p0   = attr['x'], attr['y'], attr['z']
            text = str(i)
            v01  = [p1[i] - p0[i] for i in range(3)]
            v02  = [p2[i] - p0[i] for i in range(3)]
            l    = length(cross(v01, v02))
            if l12 == 0.0 or (l / l12) < self.tol:
                point = Point3d(*p0)
                e.Display.DrawDot(point, text, self.dotcolor, self.textcolor)
                break


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
