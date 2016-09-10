from Rhino.Display import DisplayConduit


class Conduit(DisplayConduit):

    def __init__(self):
        super(Conduit, self).__init__()

    def enable(self):
        self.Enabled = True

    def disable(self):
        self.Enabled = False


# from lines import LinesConduit
# from points import PointsConduit
# from splines import SplinesConduit


__all__ = []
