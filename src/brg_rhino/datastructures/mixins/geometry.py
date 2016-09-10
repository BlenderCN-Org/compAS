# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$


import Rhino
from Rhino.Geometry import Point3d

from brg_rhino.datastructures.mixins import Mixin

import brg_rhino.utilities as rhino


TOL = rhino.get_tolerance()


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'Apache License, Version 2.0'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 14, 2014'


# def move_vertices(self, keys):
#     color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
#     guids = []
#     for key in keys:
#         name = '{0}.vertex.{1}'.format(self.name, key)
#         guids += rhino.get_objects(name)
#     if not guids:
#         return
#     lines = []
#     anchored_lines  = []
#     moving_vertices = []
#     moved_vertices  = [None] * len(keys)
#     visited = {}
#     for key in keys:
#         u = len(moving_vertices)
#         moving_vertices.append([self.vertex[key][_] for _ in 'xyz'])
#         nbrs = self.halfedge[key]
#         for nbr in nbrs:
#             if (key, nbr) in visited or (nbr, key) in visited:
#                 continue
#             if nbr in keys:
#                 v = keys.index(nbr)
#                 lines.append((u, v))
#             else:
#                 anchor = [self.vertex[nbr][_] for _ in 'xyz']
#                 anchored_lines.append((anchor, u))
#             if nbr in self.edge[key]:
#                 visited[(key, nbr)] = 1
#             else:
#                 visited[(nbr, key)] = 1
#     to_delete = list(guids)
#     for u, v in visited.iterkeys():
#         to_delete += rhino.get_objects('{0}.edge.{1}-{2}'.format(self.name, u, v))
#     start = rhino.pick_point('Point to move from?')
#     rhino.delete_objects(to_delete)
#     def OnDynamicDraw(sender, eargs):
#         current = list(eargs.CurrentPoint)
#         vec = [current[i] - start[i] for i in range(3)]
#         for i in xrange(len(moving_vertices)):
#             moved_vertices[i] = [moving_vertices[i][_] + vec[_] for _ in range(3)]
#         for anchor, index in iter(anchored_lines):
#             sp = Rhino.Geometry.Point3d(*anchor)
#             ep = Rhino.Geometry.Point3d(*moved_vertices[index])
#             eargs.Display.DrawDottedLine(sp, ep, color)
#         for u, v in iter(lines):
#             sp = Rhino.Geometry.Point3d(*moved_vertices[u])
#             ep = Rhino.Geometry.Point3d(*moved_vertices[v])
#             eargs.Display.DrawDottedLine(sp, ep, color)
#     gp = Rhino.Input.Custom.GetPoint()
#     gp.SetCommandPrompt('Point to move to?')
#     gp.DynamicDraw += OnDynamicDraw
#     gp.Get()
#     if gp.CommandResult() == Rhino.Commands.Result.Success:
#         end = list(gp.Point())
#         vec = [end[i] - start[i] for i in range(3)]
#         for key in keys:
#             self.vertex[key]['x'] += vec[0]
#             self.vertex[key]['y'] += vec[1]
#             self.vertex[key]['z'] += vec[2]
#     self.draw()


class EditGeometry(Mixin):
    """"""

    def move(self):
        color  = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        origin = dict((key, self.vertex_coordinates(key)) for key in self.vertex)
        vertex = dict((key, self.vertex_coordinates(key)) for key in self.vertex)
        edges  = self.edges()
        start  = rhino.pick_point('Point to move from?')
        if not start:
            return
        def OnDynamicDraw(sender, e):
            current = list(e.CurrentPoint)
            vec = [current[i] - start[i] for i in range(3)]
            for key in vertex:
                vertex[key] = [origin[key][i] + vec[i] for i in range(3)]
            for u, v in iter(edges):
                sp = vertex[u]
                ep = vertex[v]
                sp = Point3d(*sp)
                ep = Point3d(*ep)
                e.Display.DrawDottedLine(sp, ep, color)
        rhino.delete_objects(rhino.get_objects(name='{0}.*'.format(self.name)))
        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Point to move to?')
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() == Rhino.Commands.Result.Success:
            end = list(gp.Point())
            vec = [end[i] - start[i] for i in range(3)]
            for key, attr in self.vertices_iter(True):
                attr['x'] += vec[0]
                attr['y'] += vec[1]
                attr['z'] += vec[2]
        self.draw()

    def move_vertex(self, key, constraint=None, allow_off=None):
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs  = [self.vertex_coordinates(nbr) for nbr in self.halfedge[key]]
        nbrs  = [Rhino.Geometry.Point3d(*xyz) for xyz in nbrs]
        def OnDynamicDraw(sender, e):
            for ep in nbrs:
                sp = e.CurrentPoint
                e.Display.DrawDottedLine(sp, ep, color)
        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Point to move to?')
        gp.DynamicDraw += OnDynamicDraw
        if constraint:
            if allow_off is not None:
                gp.Constrain(constraint, allow_off)
            else:
                gp.Constrain(constraint)
        gp.Get()
        if gp.CommandResult() == Rhino.Commands.Result.Success:
            pos = list(gp.Point())
            self.vertex[key]['x'] = pos[0]
            self.vertex[key]['y'] = pos[1]
            self.vertex[key]['z'] = pos[2]
        self.draw()


class DisplayGeometry(Mixin):
    """"""

    def display_vertex_normals(self, display=True, layer=None, scale=1.0, color=None):
        rhino.delete_objects(rhino.get_objects(name='{0}.vertex.normal.*'.format(self.name)))
        if not display:
            return
        lines = []
        layer = layer or self.layer
        color = color or self.color['normal:vertex']
        for key in self.vertex:
            nv   = self.vertex_normal(key)
            sp   = self.vertex_coordinates(key)
            ep   = [sp[axis] + nv[axis] for axis in range(3)]
            name = '{0}.vertex.normal.{1}'.format(self.name, key)
            lines.append({
                'start' : sp,
                'end'   : ep,
                'name'  : name,
                'color' : color,
                'arrow' : 'end',
            })
        rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)

    def display_face_normals(self, display=True, layer=None, scale=1.0, color=None):
        rhino.delete_objects(rhino.get_objects(name='{0}.face.normal.*'.format(self.name)))
        if not display:
            return
        lines = []
        layer = layer or self.layer
        color = color or self.color['normal:face']
        for fkey in self.face:
            nv   = self.face_normal(fkey)
            sp   = self.face_center(fkey)
            ep   = [sp[axis] + nv[axis] for axis in range(3)]
            name = '{0}.face.normal.{1}'.format(self.name, fkey)
            lines.append({
                'start' : sp,
                'end'   : ep,
                'name'  : name,
                'color' : color,
                'arrow' : 'end',
            })
        rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)
