"""A Toolbar providing an interface to common mesh tools."""

from compas.geometry.elements.polyhedron import Polyhedron

from compas.datastructures.mesh.mesh import Mesh

from compas.datastructures.mesh.algorithms.tri.subdivision import loop_subdivision

from compas.datastructures.mesh.algorithms.subdivision import quad_subdivision
from compas.datastructures.mesh.algorithms.subdivision import doosabin_subdivision
from compas.datastructures.mesh.algorithms.subdivision import _catmullclark_subdivision

from compas_rhino.datastructures.mesh import RhinoMesh

# from compas_rhino.datastructures.mixins.keys import SelectComponents
# from compas_rhino.datastructures.mixins.attributes import EditAttributes
# from compas_rhino.datastructures.mixins.geometry import EditGeometry
# from compas_rhino.datastructures.mixins.geometry import DisplayGeometry
# from compas_rhino.datastructures.mixins.labels import DisplayLabels

import compas_rhino.utilities as rhino

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


class ControlMesh(Mesh):
    """"""

    def __init__(self, **kwargs):
        super(ControlMesh, self).__init__(**kwargs)
        self.attributes.update({
            'layer'               : None,
            'color.vertex'        : None,
            'color.edge'          : None,
            'color.face'          : None,
            'color.normal:vertex' : None,
            'color.normal:face'   : None,
        })
        self.dva.update({
            'is_fixed' : False,
        })
        self.dea.update({
            'weight' : 1.0,
            'q' : 1.0,
        })


class MeshTools(object):
    """"""

    def __init__(self):
        self.mesh = None
        self.layers = {'MeshTools' : {'layers': {
            'Mesh': {'layers': {}},
            'Subd': {'layers': {
                'LoopMesh' : {'layers' : {}},
                'QuadMesh' : {'layers' : {}},
                'DooSabinMesh' : {'layers' : {}},
                'CatmullClarkMesh' : {'layers' : {}},
            }},
        }}}

    def init(self):
        rhino.create_layers(self.layers)
        rhino.clear_layers(self.layers)

    def from_xxx(self):
        options = ['mesh', 'surface', 'surface_uv', 'polyhedron', 'obj', 'json']
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
        if option == 'surface_uv':
            guid = rhino.select_surface()
            if guid:
                self.mesh = RhinoMesh.from_surface_uv(guid)
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

    def edit(self):
        """Edit mesh attributes."""
        # select a mesh by clicking on it
        # provide support for fixed vertices
        # provide support for edge weights
        # provide support for force densities
        mesh = self.mesh
        options = ['vertices', 'edges', 'faces']
        option = rs.GetString('Edit attributes of ...', options[0], options)
        if option not in options:
            return
        if option == 'vertices':
            keys = mesh.select_vertices()
            if not keys:
                return
            names = sorted(mesh.dva.keys())
            mesh.edit_vertex_attributes(keys, names)
        if option == 'edges':
            keys = mesh.select_edges()
            if not keys:
                return
            names = sorted(mesh.dea.keys())
            mesh.edit_edge_attributes(keys, names)
        if option == 'faces':
            keys = mesh.select_faces()
            if not keys:
                return
            names = sorted(mesh.dfa.keys())
            mesh.edit_face_attributes(keys, names)

    def modify(self):
        """Modfy geometry and/or topology of a mesh."""
        # select a mesh by clicking on it
        mesh = self.mesh
        options = ['Move', 'MoveVertex', 'MoveFace', 'MoveEdge', 'SplitEdge', 'SwapEdge', 'CollapseEdge']
        option = rs.GetString('Mesh Operation ...', options[0], options)
        if option not in options:
            return
        if option == 'Move':
            raise NotImplementedError
        if option == 'MoveVertex':
            raise NotImplementedError
        if option == 'MoveFace':
            raise NotImplementedError
        if option == 'MoveEdge':
            raise NotImplementedError
        if option == 'SplitEdge':
            raise NotImplementedError
        if option == 'SwapEdge':
            raise NotImplementedError
        if option == 'CollapseEdge':
            raise NotImplementedError

    def modify_tri(self):
        """Modfy geometry and/or topology of a triangle mesh.

        The avaialable operations are specific to triangle meshes, because they
        use the properties of the triangular geometry and topology to simplify
        and speed up the operations. The effect of the operations is also slightly
        different, because they preserve the triangular nature of the mesh.

        Raises:
            Exception :
                If the selected mesh is not a triangle mesh.
        """
        mesh = self.mesh
        if not mesh.is_trimesh():
            raise Exception('TriMesh operations are only available for trianlge meshes.')
        options = ['SplitEdge', 'SwapEdge', 'CollapseEdge']
        option = rs.GetString('TriMesh Operation ...', options[0], options)
        if option not in options:
            return
        if option == 'SplitEdge':
            raise NotImplementedError
        if option == 'SwapEdge':
            raise NotImplementedError
        if option == 'CollapseEdge':
            raise NotImplementedError

    def subd(self):
        """Subdivide the control mesh and draw as separate subd mesh."""
        options = ['Quad', 'DooSabin', 'CatmullClark']
        option = rs.GetString('Subdivision scheme ...', options[0], options)
        if option not in options:
            return
        loops = ['k1', 'k2', 'k3', 'k4', 'k5']
        k = rs.GetString('Subd level ...', loops[0], loops)
        if k not in loops:
            return
        k = int(k[1:])
        if option == 'Quad':
            # Quad subdivision.
            # Interpolation
            # This should be removed
            raise NotImplementedError  # properly :)
            subd = quad_subdivision(self.mesh, k=k)
            subd.name = 'QuadMesh'
            subd.layer = 'MeshTools::Subd::QuadMesh'
            subd.draw(show_vertices=False, show_edges=False)
        if option == 'DooSabin':
            # Doo-Sabin scheme for quad subdivision.
            # Approximation
            subd = doosabin_subdivision(self.mesh, k=k)
            subd.name = 'DooSabinMesh'
            subd.layer = 'MeshTools::Subd::DooSabinMesh'
            subd.draw(show_vertices=False, show_edges=False)
        if option == 'CatmullClark':
            # Catmull-Clark scheme for quad subdivision.
            # Approximation
            subd = _catmullclark_subdivision(self.mesh, k=k)
            subd.name = 'CatmullClarkMesh'
            subd.layer = 'MeshTools::Subd::CatmullClarkMesh'
            subd.draw(show_vertices=False, show_edges=False)

    def subd_tri(self):
        """Apply subdivision algorithms that are specific to trianlge meshes.

        Raises:
            Exception :
                If the selected mesh is not a tiangle mesh.
        """
        if not self.mesh.is_trimesh():
            raise Exception('TriSubdivision schemes are only available for trianlge meshes.')
        options = ['Loop']
        option = rs.GetString('TriSubdivision scheme ...', options[0], options)
        if option not in options:
            return
        loops = ['k1', 'k2', 'k3', 'k4', 'k5']
        k = rs.GetString('Subd level ...', loops[0], loops)
        if k not in loops:
            return
        k = int(k[1:])
        if option == 'Loop':
            # Loop subdivision.
            # Approximation
            subd = loop_subdivision(self.mesh, k=k)
            subd.name = 'LoopMesh'
            subd.layer = 'MeshTools::Subd::LoopMesh'
            subd.draw(show_vertices=False, show_edges=False)

    def smooth(self):
        options = ['umbrella', 'area', 'forcedensity']
        option = rs.GetString('Weighting scheme...', options[0], options)
        if option not in options:
            return
        if option == 'umbrella':
            raise NotImplementedError
        if option == 'area':
            raise NotImplementedError
        if option == 'forcedensity':
            raise NotImplementedError

    def smooth_tri(self):
        options = ['cotangent']
        option = rs.GetString('Tri Weighting scheme...', options[0], options)
        if option not in options:
            return
        if option == 'cotangent':
            raise NotImplementedError

    def relax(self):
        raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas_rhino.ui.rui import Rui
    from compas_rhino.ui.rui import get_macros
    from compas_rhino.ui.rui import update_macro

    toolbars = [{'name' : 'MeshTools', 'items' : [
        {'type': 'normal', 'left_macro' : 'init', },
        {'type': 'normal', 'left_macro' : 'from_xxx', },
        {'type': 'normal', 'left_macro' : 'to_xxx', },
        {'type': 'separator', },
        {'type': 'normal', 'left_macro' : 'edit', },
        {'type': 'normal', 'left_macro' : 'modify', },
        {'type': 'normal', 'left_macro' : 'subd', },
        {'type': 'normal', 'left_macro' : 'smooth', },
        {'type': 'normal', 'left_macro' : 'relax', },
        {'type': 'separator', },
        {'type': 'normal', 'left_macro' : 'modify_tri', },
        {'type': 'normal', 'left_macro' : 'subd_tri', },
    ]}]

    toolbargroups = [{'name' : 'MeshTools', 'toolbars' : ['MeshTools', ]}]

    macros = get_macros(MeshTools, 'mtools')

    init_script = [
        '-_RunPythonScript ResetEngine (',
        'from compas_rhino.datastructures.toolbars.meshtools import MeshTools;',
        'mtools = MeshTools();',
        'mtools.init()',
        ')',
    ]

    update_macro(macros, 'init', 'script', ''.join(init_script))

    rui = Rui('./mtools.rui')

    rui.init()
    rui.add_macros(macros)
    rui.add_toolbars(toolbars)
    rui.add_toolbargroups(toolbargroups)
    rui.write()
