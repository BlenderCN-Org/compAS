"""
.. compas_rhino.conduits:

********************************************************************************
conduits
********************************************************************************

.. module:: compas_rhino.conduits


Definition of display conduits.


.. autosummary::
    :toctree: generated/

    FacesConduit
    LabelsConduit
    LinesConduit
    MeshConduit
    MeshVertexInspector
    PointPairsConduit
    PointsConduit
    SplinesConduit

"""

try:
    import Rhino
    import scriptcontext as sc
    from Rhino.Display import DisplayConduit

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e

    class DisplayConduit(object):
        pass


class Conduit(DisplayConduit):

    def __init__(self):
        super(Conduit, self).__init__()

    def enable(self):
        self.Enabled = True

    def disable(self):
        self.Enabled = False

    def redraw(self):
        sc.doc.Views.Redraw()
        Rhino.RhinoApp.Wait()


from .faces import *
from .labels import *
from .lines import *
from .mesh import *
from .pointpairs import *
from .points import *
from .splines import *
