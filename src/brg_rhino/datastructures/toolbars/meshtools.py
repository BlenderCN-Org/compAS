"""A Toolbar providing an interface to common mesh tools."""

from brg_rhino.datastructures.mesh import RhinoMesh
import brg_rhino.utilities as rhino

try:
    import rhinoscriptsyntax as rs
except ImportError as e:
    import platform
    if platform.system() == 'Windows':
        raise e


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


class MeshTools(object):
    """"""

    def __init__(self):
        self.mesh = None
        self.settings = {}
        self.layers = []

    def init(self):
        pass

    def from_xxx(self):
        options = ['mesh', 'surface', 'obj', 'json']
        option = rs.GetString('', options[0], options)
        if option not in options:
            return
        if option == 'mesh':
            guid = rhino.select_mesh()
            if guid:
                self.mesh = RhinoMesh.from_guid(guid)
                self.mesh.draw()
        if option == 'surface':
            guid = rhino.select_surface()
            if guid:
                self.mesh = RhinoMesh.from_surface(guid)
                self.mesh.draw()
        if option == 'obj':
            raise NotImplementedError
        if option == 'json':
            raise NotImplementedError

    def to_xxx(self):
        options = ['obj', 'json']
        option = rs.GetString('', options[0], options)
        if option not in options:
            return
        if option == 'obj':
            raise NotImplementedError
        if option == 'json':
            raise NotImplementedError

    def modify(self):
        options = ['split', 'swap', 'collapse']
        option = rs.GetString('', options[0], options)
        if option not in options:
            return
        if option == 'split':
            raise NotImplementedError
        if option == 'swap':
            raise NotImplementedError
        if option == 'collapse':
            raise NotImplementedError

    def subdivide(self):
        options = []
        option = rs.GetString('', options[0], options)
        if option not in options:
            return

    def smooth(self):
        options = ['umbrella', 'cotangent', 'area', 'forcedensity']
        option = rs.GetString('', options[0], options)
        if option not in options:
            return

    def relax(self):
        options = []
        option = rs.GetString('', options[0], options)
        if option not in options:
            return


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from brg.files.rui import Rui
    from brg.files.rui import get_macros

    toolbars = [{'name' : 'MeshTools', 'items' : []}]
    toolbargroups = [{'name' : 'MeshTools', 'toolbars' : ['MeshTools', ]}]

    rui = Rui('./nest.rui')

    rui.init()

    macros = get_macros(MeshTools, 'mtools')

    rui.add_macros(macros)
    rui.add_toolbars(toolbars)
    rui.add_toolbargroups(toolbargroups)

    rui.write()
