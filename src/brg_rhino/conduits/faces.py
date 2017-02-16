from brg_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from System.Drawing.Color import FromArgb
    from System.Collections.Generic import List

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['FacesConduit', ]


class FacesConduit(Conduit):
    """A Rhino display conduit for labels.

    Parameters:
        labels (list): A list of label tuples. Each tuple contains a position and text for the label.
        color (tuple): Optional.
            RGB color spec for the dots.
            Default is ``None``.

    Example:

        .. code-block:: python

            import time
            from brg.geometry.elements import Polyhedron

            polyhedron = Polyhedron.generate(6)

            faces = polyhedron.faces
            vertices = polyhedron.vertices

            polygons = [[vertices[index] for index in face] for face in faces]

            try:
                conduit = FacesConduit(polygons)
                conduit.enable()
                conduit.redraw()
                time.sleep(5.0)

            except Exception as e:
                print e

            finally:
                conduit.disable()
                del conduit

    """
    def __init__(self, faces):
        super(FacesConduit, self).__init__()
        self.faces = faces
        self.color = FromArgb(255, 0, 0)

    def DrawForeground(self, e):
        for points in self.faces:
            points = [Point3d(*point) for point in points]
            e.Display.DrawPolygon(points, self.color, True)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import time
    from brg.geometry.elements import Polyhedron

    polyhedron = Polyhedron.generate(6)

    faces = polyhedron.faces
    vertices = polyhedron.vertices

    polygons = [[vertices[index] for index in face] for face in faces]

    try:
        conduit = FacesConduit(polygons)
        conduit.enable()
        conduit.redraw()
        time.sleep(5.0)

    except Exception as e:
        print e

    finally:
        conduit.disable()
        del conduit
