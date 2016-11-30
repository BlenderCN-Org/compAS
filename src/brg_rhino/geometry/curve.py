# -*- coding: utf-8 -*-

import brg_rhino.utilities as rhino

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    find_object = sc.doc.Objects.Find

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
__date__       = '29.09.2014'


class Curve(object):
    """"""

    def __init__(self, guid):
        self.guid = guid
        self.curve = find_object(guid)
        self.geometry = self.curve.Geometry

    def hide(self):
        return rs.HideObject(self.guid)

    def show(self):
        return rs.ShowObject(self.guid)

    def select(self):
        return rs.SelectObject(self.guid)

    def unselect(self):
        return rs.UnselectObject(self.guid)

    def delete(self):
        rhino.delete_objects([self.guid])
        self.guid = None

    def is_line(self):
        return (rs.IsLine(self.guid) and
                rs.CurveDegree(self.guid) == 1 and
                len(rs.CurvePoints(self.guid)) == 2)

    def is_polyline(self):
        return (rs.IsPolyline(self.guid) and
                rs.CurveDegree(self.guid) == 1 and
                len(rs.CurvePoints(self.guid)) > 2)

    def space(self, density=10):
        space = []
        density = int(density)
        if rs.IsCurve(self.guid):
            domain = rs.CurveDomain(self.guid)
            u = (domain[1] - domain[0]) / (density - 1)
            for i in range(density):
                space.append(domain[0] + u * i)
        elif rs.IsPolyCurve(self.guid):
            rs.EnableRedraw(False)
            segments = rs.ExplodeCurves(self.guid)
            for segment in segments:
                domain = rs.CurveDomain(segment)
                u = (domain[1] - domain[0]) / (density - 1)
                for i in range(density):
                    space.append(domain[0] + u * i)
            rs.DeleteObjects(segments)
            rs.EnableRedraw(True)
        else:
            raise CurveError('object is not a curve')
        return space

    def heightfield(self, density=10):
        heightfield = []
        space = self.space(density)
        if space:
            xyz = [rs.EvaluateCurve(self.guid, param) for param in space]
            heightfield = map(list, xyz)
        return heightfield

    def curvature(self):
        raise NotImplementedError

    def tangents(self, points=None):
        tangents = []
        if not points:
            points = self.heightfield()
        if rs.IsPolyCurve(self.guid):
            pass
        elif rs.IsCurve(self.guid):
            for point in points:
                param = rs.CurveClosestPoint(self.guid, point)
                vector = list(rs.CurveTangent(self.guid, param))
                tangents.append((point, vector))
        else:
            raise CurveError('object is not a curve')
        return tangents

    def descent(self, points=None):
        tangents = self.tangents(points)
        return [(point, vector) if vector[2] < 0 else (point, [-v for v in vector]) for point, vector in tangents]

    def divide(self, number_of_segments, over_space=False):
        points = []
        rs.EnableRedraw(False)
        if over_space:
            space = self.space(number_of_segments + 1)
            if space:
                points = [list(rs.EvaluateCurve(self.guid, param)) for param in space]
        else:
            temp = rs.DivideCurve(self.guid, number_of_segments, create_points=False, return_points=True)
            points = map(list, temp)
        rs.EnableRedraw(True)
        return points

    def divide_length(self, length_of_segments):
        rs.EnableRedraw(False)
        temp = rs.DivideCurveLength(self.guid, length_of_segments, create_points=False, return_points=True)
        points = map(list, temp)
        rs.EnableRedraw(True)
        return points

    def closest_points(self, points):
        closest = []
        for point in points:
            t = rs.CurveClosestPoint(self.guid, point)
            closest.append(rs.EvaluateCurve(self.guid, t))
        return closest

    def pulled_points(self, points):
        return self.closest_points(points)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    guids = rhino.get_curves()

    curve = Curve(guids[0])

    lines = []
    for point, vector in curve.descent():
        lines.append({
            'start' : point,
            'end'   : [point[i] + vector[i] for i in range(3)],
            'color' : (0, 255, 0),
            'name'  : 'descent',
            'arrow' : 'end',
        })
    rhino.xdraw_lines(lines, layer='Layer 01', clear=True, redraw=True)
