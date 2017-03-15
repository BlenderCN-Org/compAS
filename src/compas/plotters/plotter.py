import matplotlib.pyplot as plt


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


class Plotter(object):
    """"""

    def __init__(self):
        self.subplots = None

    def draw_points(self, points, subplot=None):
        pass

    def show(self):
        plt.show()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
