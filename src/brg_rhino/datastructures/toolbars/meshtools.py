"""A Toolbar providing an interface to common mesh tools."""

from brg.geometry.elements.polyhedron import Polyhedron
from brg_rhino.datastructures.mesh import RhinoMesh

from brg.datastructures.mesh.algorithms.subdivision import _catmullclark_subdivision
from brg.datastructures.mesh.algorithms.subdivision import doosabin_subdivision
from brg.datastructures.mesh.algorithms.tri.subdivision import loop_subdivision

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
        self.layers = {'MeshTools' : {'layers': {
            'Mesh': {'layers': {}},
            'Subd': {'layers': {}},
        }}}

    # script => -_RunPythonScript ResetEngine (from brg_rhino.datastructures.toolbars.meshtools import MeshTools;mtools = MeshTools();mtools.init())
    def init(self):
        rhino.create_layers(self.layers)
        rhino.clear_layers(self.layers)

    def from_xxx(self):
        options = ['mesh', 'surface', 'polyhedron', 'obj', 'json']
        option = rs.GetString('From what ...', options[0], options)
        if option not in options:
            return
        if option == 'mesh':
            guid = rhino.select_mesh()
            if guid:
                self.mesh = RhinoMesh.from_guid(guid)
                self.mesh.name = 'Mesh'
                self.mesh.layer = 'MeshTools::Mesh'
                self.mesh.draw(show_faces=False)
        if option == 'surface':
            guid = rhino.select_surface()
            if guid:
                self.mesh = RhinoMesh.from_surface(guid)
                self.mesh.name = 'Mesh'
                self.mesh.layer = 'MeshTools::Mesh'
                self.mesh.draw(show_faces=False)
        if option == 'polyhedron':
            faces = ['f4', 'f6', 'f8', 'f12', 'f20']
            f = rs.GetString('Number of faces ...', faces[0], faces)
            if f not in faces:
                return
            f = int(f[1:])
            tet = Polyhedron.generate(f)
            if tet:
                self.mesh = RhinoMesh.from_vertices_and_faces(tet.vertices, tet.faces)
                self.mesh.name = 'Mesh'
                self.mesh.layer = 'MeshTools::Mesh'
                self.mesh.draw(show_faces=False)
        if option == 'obj':
            raise NotImplementedError
        if option == 'json':
            raise NotImplementedError

    def to_xxx(self):
        options = ['obj', 'json']
        option = rs.GetString('Export format ...', options[0], options)
        if option not in options:
            return
        if option == 'obj':
            raise NotImplementedError
        if option == 'json':
            raise NotImplementedError

    def modify(self):
        options = ['split', 'swap', 'collapse']
        option = rs.GetString('Operation ...', options[0], options)
        if option not in options:
            return
        if option == 'split':
            raise NotImplementedError
        if option == 'swap':
            raise NotImplementedError
        if option == 'collapse':
            raise NotImplementedError

    def subdivide(self):
        options = ['loop', 'doosabin', 'catmullclark']
        option = rs.GetString('Subdivision scheme ...', options[0], options)
        if option not in options:
            return
        loops = ['k1', 'k2', 'k3', 'k4', 'k5']
        k = rs.GetString('Subd level ...', loops[0], loops)
        if k not in loops:
            return
        k = int(k[1:])
        if option == 'loop':
            if not self.mesh.is_trimesh():
                raise Exception('Loop subd is only available for trianlge meshes.')
            subd = loop_subdivision(self.mesh, k=k)
            subd.name = 'SubdMesh'
            subd.layer = 'MeshTools::Subd'
            subd.draw(show_vertices=False, show_edges=False)
        if option == 'doosabin':
            subd = doosabin_subdivision(self.mesh, k=k)
            subd.name = 'SubdMesh'
            subd.layer = 'MeshTools::Subd'
            subd.draw(show_vertices=False, show_edges=False)
        if option == 'catmullclark':
            subd = _catmullclark_subdivision(self.mesh, k=k)
            subd.name = 'SubdMesh'
            subd.layer = 'MeshTools::Subd'
            subd.draw(show_vertices=False, show_edges=False)

    def smooth(self):
        options = ['umbrella', 'cotangent', 'area', 'forcedensity']
        option = rs.GetString('Weighting scheme...', options[0], options)
        if option not in options:
            return
        if option == 'umbrella':
            raise NotImplementedError
        if option == 'cotangent':
            raise NotImplementedError
        if option == 'area':
            raise NotImplementedError
        if option == 'forcedensity':
            raise NotImplementedError

    def relax(self):
        raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from brg.files.rui import Rui
    from brg.files.rui import get_macros

    toolbars = [{'name' : 'MeshTools', 'items' : [
        {'type': 'normal', 'left_macro' : 'init', 'right_macro' : None},
        {'type': 'normal', 'left_macro' : 'from_xxx', 'right_macro' : None},
        {'type': 'normal', 'left_macro' : 'to_xxx', 'right_macro' : None},
        {'type': 'normal', 'left_macro' : 'modify', 'right_macro' : None},
        {'type': 'normal', 'left_macro' : 'subdivide', 'right_macro' : None},
        {'type': 'normal', 'left_macro' : 'smooth', 'right_macro' : None},
        {'type': 'normal', 'left_macro' : 'relax', 'right_macro' : None},
    ]}]
    toolbargroups = [{'name' : 'MeshTools', 'toolbars' : ['MeshTools', ]}]

    rui = Rui('./mtools.rui')

    rui.init()

    macros = get_macros(MeshTools, 'mtools')

    rui.add_macros(macros)
    rui.add_toolbars(toolbars)
    rui.add_toolbargroups(toolbargroups)

    rui.write()
