from brg.datastructures import Network

from brg_rhino.datastructures.mixins.attributes import EditAttributes
from brg_rhino.datastructures.mixins.geometry import EditGeometry
from brg_rhino.datastructures.mixins.geometry import DisplayGeometry
from brg_rhino.datastructures.mixins.keys import GetKeys
from brg_rhino.datastructures.mixins.labels import DisplayLabels

import brg_rhino.utilities as rhino


@rhino.add_gui_helpers((EditAttributes, EditGeometry, DisplayGeometry, GetKeys, DisplayLabels))
class RhinoNetwork(Network):

    def __init__(self, **kwargs):
        super(RhinoNetwork, self).__init__(**kwargs)
        self.attributes.update({
            'layer'        : None,
            'color.vertex' : (0, 0, 0),
            'color.edge'   : (53, 53, 53),
        })
        self.attributes.update(kwargs)

    # --------------------------------------------------------------------------
    # descriptors
    #
    # NOTE: some descriptors are inherited from the base Mixin class
    # --------------------------------------------------------------------------

    @property
    def layer(self):
        """:obj:`str` : The layer of the network.

        Any value of appropriate type assigned to this property will be stored in
        the instance's attribute dict.
        """
        return self.attributes.get('layer', None)

    @layer.setter
    def layer(self, value):
        self.attributes['layer'] = value

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # drawing
    # --------------------------------------------------------------------------

    # provide option to use vertex_color dict
    def draw(self,
             name=None,
             layer=None,
             clear=True,
             redraw=True,
             show_vertices=True,
             show_edges=True,
             vertex_color=None,
             edge_color=None):
        """"""
        self.name = name or self.name
        self.layer = layer or self.layer
        points = []
        color  = self.color['vertex']
        vcolor = vertex_color or {}
        for key in self.vertex:
            pos  = self.vertex_coordinates(key)
            name = '{0}.vertex.{1}'.format(self.name, key)
            points.append({
                'pos'   : pos,
                'name'  : name,
                'color' : vcolor.get(key, color),
            })
        lines  = []
        color  = self.color['edge']
        ecolor = edge_color or {}
        for u, v in self.edges_iter():
            start = self.vertex_coordinates(u)
            end   = self.vertex_coordinates(v)
            name  = '{0}.edge.{1}-{2}'.format(self.name, u, v)
            lines.append({
                'start' : start,
                'end'   : end,
                'name'  : name,
                'color' : ecolor.get((u, v), color),
                'arrow' : None,
            })
        rhino.delete_objects(rhino.get_objects('{0}.vertex.*'.format(self.name)))
        rhino.delete_objects(rhino.get_objects('{0}.edge.*'.format(self.name)))
        if show_vertices:
            rhino.xdraw_points(points, layer=self.layer, clear=clear, redraw=False)
        if show_edges:
            rhino.xdraw_lines(lines, layer=self.layer, clear=False, redraw=True)
