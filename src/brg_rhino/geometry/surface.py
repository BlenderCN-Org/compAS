""""""

from brg_rhino.exceptions import RhinoSurfaceError

try:
    import Rhino
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    from Rhino.Geometry import Point3d

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


class Surface(object):
    """"""

    def __init__(self, guid=None):
        self.guid = guid
        self.surface = find_object(guid)
        self.geometry = self.surface.Geometry
        self.attributes = self.surface.Attributes
        self.otype = self.geometry.ObjectType

    def space(self, density=10):
        """"""
        try:
            du, dv = density
        except TypeError:
            du = density
            dv = density
        du = int(du)
        dv = int(dv)
        uv = []
        rs.EnableRedraw(False)
        if rs.IsPolysurface(self.guid):
            faces = rs.ExplodePolysurfaces(self.guid)
        elif rs.IsSurface(self.guid):
            faces = [self.guid]
        else:
            raise RhinoSurfaceError('object is not a surface')
        for face in faces:
            domainU = rs.SurfaceDomain(face, 0)
            domainV = rs.SurfaceDomain(face, 1)
            u = (domainU[1] - domainU[0]) / (du - 1)
            v = (domainV[1] - domainV[0]) / (dv - 1)
            for i in xrange(du):
                for j in xrange(dv):
                    uv.append((domainU[0] + u * i, domainV[0] + v * j))
        if len(faces) > 2:
            rs.DeleteObjects(faces)
        rs.EnableRedraw(True)
        return uv

    def surface_heightfield(self, density=10, over_space=True):
        """"""
        try:
            du, dv = density
        except TypeError:
            du = density
            dv = density
        du = int(du)
        dv = int(dv)
        xyz = []
        rs.EnableRedraw(False)
        if rs.IsPolysurface(self.guid):
            faces = rs.ExplodePolysurfaces(self.guid)
        elif rs.IsSurface(self.guid):
            faces = [self.guid]
        else:
            raise RhinoSurfaceError('object is not a surface')
        if over_space:
            for guid in faces:
                face = Surface(guid)
                uv = face.space(density)
                for u, v in uv:
                    xyz.append(list(rs.EvaluateSurface(face.guid, u, v)))
        else:
            for guid in faces:
                bbox = rs.BoundingBox(guid)
                xmin = bbox[0][0]
                xmax = bbox[1][0]
                ymin = bbox[0][1]
                ymax = bbox[3][1]
                xstep = 1.0 * (xmax - xmin) / (du - 1)
                ystep = 1.0 * (ymax - ymin) / (dv - 1)
                seeds = []
                for i in xrange(du):
                    for j in xrange(dv):
                        seed = xmin + i * xstep, ymin + j * ystep, 0
                        seeds.append(seed)
                points = map(list, rs.ProjectPointToSurface(seeds, guid, [0, 0, 1]))
                xyz += points
        if len(faces) > 1:
            rs.DeleteObjects(faces)
        rs.EnableRedraw(True)
        return xyz

    def descent(self, points=None):
        """"""
        if not points:
            points = self.heightfield()
        tol = rs.UnitAbsoluteTolerance()
        descent = []
        if rs.IsPolysurface(self.guid):
            rs.EnableRedraw(False)
            faces = {}
            for p0 in points:
                p = p0[:]
                p[2] -= 2 * tol
                bcp = rs.BrepClosestPoint(self.guid, p)
                uv = bcp[1]
                index = bcp[2][1]
                try:
                    face = faces[index]
                except:
                    face = rs.ExtractSurface(self.guid, index, True)
                    faces[index] = face
                p1 = rs.EvaluateSurface(face, uv[0], uv[1])
                vector = [p1[_] - p0[_] for _ in range(3)]
                descent.append((p0, vector))
            rs.DeleteObjects(faces.values())
            rs.EnableRedraw(True)
        elif rs.IsSurface(self.guid):
            for p0 in points:
                p = p0[:]
                p[2] -= 2 * tol
                bcp = rs.BrepClosestPoint(self.guid, p)
                uv = bcp[1]
                p1 = rs.EvaluateSurface(self.guid, uv[0], uv[1])
                vector = [p1[_] - p0[_] for _ in range(3)]
                descent.append((p0, vector))
        else:
            raise RhinoSurfaceError('object is not a surface')
        return descent

    def curvature(self, points=None):
        """"""
        if not points:
            points = self.heightfield()
        curvature = []
        if rs.IsPolysurface(self.guid):
            rs.EnableRedraw(False)
            faces = {}
            for point in points:
                bcp = rs.BrepClosestPoint(self.guid, point)
                uv = bcp[1]
                index = bcp[2][1]
                try:
                    face = faces[index]
                except:
                    face = rs.ExtractSurface(self.guid, index, True)
                    faces[index] = face
                props = rs.SurfaceCurvature(face, uv)
                curvature.append((point, (props[1], props[3], props[5])))
            rs.DeleteObjects(faces.values())
            rs.EnableRedraw(False)
        elif rs.IsSurface(self.guid):
            for point in points:
                bcp = rs.BrepClosestPoint(self.guid, point)
                uv = bcp[1]
                props = rs.SurfaceCurvature(self.guid, uv)
                curvature.append((point, (props[1], props[3], props[5])))
        else:
            raise RhinoSurfaceError('object is not a surface')
        return curvature

    def borders(self):
        """"""
        border = rs.DuplicateSurfaceBorder(self.guid, type=1)
        curves = rs.ExplodeCurves(border, delete_input=True)
        return curves

    def project_points(self, points):
        projections = []
        for point in points:
            ppoints = rs.ProjectPointToSurface(point, self.guid, [0, 0, 1])
            if not ppoints:
                raise RhinoSurfaceError('Could not project point to surface.')
            ppoint = ppoints[0]
            projections.append(list(ppoint))
        return projections

    def closest_point(self, point, maxdist=None):
        rc, u, v = self.geometry.ClosestPoint(Point3d(*point))
        return list(self.geoemtry.PointAt(u, v))

    def closest_points(self, points, maxdist=None):
        return [self.closest_point(point) for point in points]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg_rhino.utilities as rhino

    guid = rhino.get_surface()

    surface = Surface(guid)

    points = []
    for xyz in surface.heightfield():
        points.append({
            'pos'   : xyz,
            'name'  : 'heightfield',
            'color' : (0, 255, 0),
        })

    rhino.xdraw_points(points, layer='Layer 01', clear=True, redraw=True)
