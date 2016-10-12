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


docs = [
    'lines',
    'points',
    'splines',
]
