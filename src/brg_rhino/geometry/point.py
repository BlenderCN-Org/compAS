""""""

from brg_rhino.exceptions import RhinoPointError
import brg_rhino.utilities as rhino

try:
    from Rhino.Geometry import Point3d
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    find_object = sc.doc.Objects.Find

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


class Point(object):
    """"""

    def __init__(self, guid):
        self.guid = guid
        self.point = find_object(guid)
        self.geometry = self.point.Geometry
        self.attributes = self.point.Attributes
        self.otype = self.geometry.ObjectType

    def closest_point(self, point, maxdist=None):
        return (self.geometry.X, self.geometry.Y, self.geometry.Z)

    def closest_points(self, points, maxdist=None):
        return [self.closest_point(point, maxdist) for point in points]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
