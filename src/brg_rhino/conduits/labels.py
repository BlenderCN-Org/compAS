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


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['LabelsConduit', ]


class LabelsConduit(Conduit):
    """A Rhino display conduit for labels.

    Parameters:
        lines (list): A list of start-end point pairs that define the lines.
        thickness (float): Optional.
            The thickness of the conduit lines.
            Default is ``1.0``.
        color (tuple): Optional.
            RGB color spec for the conduit lines.
            Default is ``None``.

    Example:

        .. code-block:: python

            import random
            import time

            points = [(1.0 * random.ranint(0, 30), 1.0 * random.randint(0, 30), 0.0) for _ in range(100)]
            lines  = [(points[i], points[i + 1]) for i in range(99)]

            conduit = LinesConduit(lines)
            conduit.enable()

            try:
                for i in range(100):
                    points = [(1.0 * random.randint(0, 30), 1.0 * random.randint(0, 30), 0.0) for _ in range(100)]
                    conduit.lines = [(points[i], points[i + 1]) for i in range(99)]
                    conduit.redraw()

                    time.sleep(0.1)
            except:
                raise

            finally:
                conduit.disable()
                del conduit

    """
    def __init__(self, labels, color=None):
        super(LabelsConduit, self).__init__()
        self.labels = labels
        color = color or (255, 255, 255)
        self.color = FromArgb(*color)

    def DrawForeground(self, e):
        for pos, text in self.labels:
            e.Display.DrawDot(Point3d(*pos), text)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from random import randint
    import time

    labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]

    try:
        conduit = LabelsConduit(labels)
        conduit.Enabled = True

        for i in range(100):
            labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]
            conduit.labels = labels

            conduit.redraw()

            time.sleep(0.1)

    except Exception as e:
        print e

    finally:
        conduit.Enabled = False
        del conduit
