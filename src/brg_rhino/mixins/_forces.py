from brg_rhino.mixins import Mixin
import brg_rhino.utilities as rhino


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['DisplayForces', ]


class DisplayForces(Mixin):
    """"""

    def display_axial_forces(self,
                             display=True,
                             layer=None,
                             scale=1.0,
                             color_tension=None,
                             color_compression=None):
        tol = rhino.get_tolerance()
        objects = rhino.get_objects(name='{0}.force:axial.*'.format(self.name))
        rhino.delete_objects(objects)
        if not display:
            return
        lines = []
        layer = layer or self.layer
        color_tension = color_tension or self.color['force:tension']
        color_compression = color_compression or self.color['force:compression']
        for u, v, attr in self.edges_iter(True):
            sp     = self.vertex_coordinates(u)
            ep     = self.vertex_coordinates(v)
            force  = attr['f']
            color  = color_tension if force > 0.0 else color_compression
            radius = scale * ((force ** 2) ** 0.5 / 3.14159) ** 0.5
            name   = '{0}.force:axial.{1}-{2}'.format(self.name, u, v)
            if radius < tol:
                continue
            lines.append({
                'start'  : sp,
                'end'    : ep,
                'name'   : name,
                'color'  : color,
                'radius' : radius,
            })
        rhino.xdraw_cylinders(lines, layer=layer, clear=False, redraw=True)

    def display_reaction_forces(self,
                                display=True,
                                layer=None,
                                scale=1.0,
                                color=None):
        tol = rhino.get_tolerance()
        objects = rhino.get_objects(name='{0}.force:reaction.*'.format(self.name))
        rhino.delete_objects(objects)
        if not display:
            return
        lines = []
        layer = layer or self.layer
        color = color or self.color['force:reaction']
        for key, attr in self.vertices_iter(True):
            if not attr['is_support']:
                continue
            r     = attr['rx'], attr['ry'], attr['rz']
            sp    = self.vertex_coordinates(key)
            ep    = [sp[i] + scale * r[i] for i in range(3)]
            l     = sum((ep[i] - sp[i]) ** 2 for i in range(3)) ** 0.5
            arrow = 'start'
            name  = '{0}.force:reaction.{1}'.format(self.name, key)
            if l < tol:
                continue
            lines.append({
                'start' : sp,
                'end'   : ep,
                'name'  : name,
                'color' : color,
                'arrow' : arrow,
            })
        rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)

    def display_residual_forces(self,
                                display=True,
                                layer=None,
                                scale=1.0,
                                color=None):
        tol = rhino.get_tolerance()
        objects = rhino.get_objects(name='{0}.force:residual.*'.format(self.name))
        rhino.delete_objects(objects)
        if not display:
            return
        lines = []
        layer = layer or self.layer
        color = color or self.color['force:residual']
        for key, attr in self.vertices_iter(True):
            if attr['is_support']:
                continue
            r     = attr['rx'], attr['ry'], attr['rz']
            sp    = self.vertex_coordinates(key)
            ep    = [sp[i] + scale * r[i] for i in range(3)]
            l     = sum((ep[i] - sp[i]) ** 2 for i in range(3)) ** 0.5
            arrow = 'end'
            name  = '{0}.force:residual.{1}'.format(self.name, key)
            if l < tol:
                continue
            lines.append({'start' : sp,
                          'end'   : ep,
                          'name'  : name,
                          'color' : color,
                          'arrow' : arrow, })
        rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=True)

    def display_selfweight(self,
                           display=True,
                           layer=None,
                           scale=None,
                           color=None):
        objects = rhino.get_objects(name='{0}.force:selfweight.*'.format(self.name))
        rhino.delete_objects(objects)
        if not display:
            return
        lines = []
        layer = layer or self.layer
        color = color or self.color['force:selfweight']
        scale = scale or self.scale['force:selfweight']
        for key, attr in self.vertices_iter(True):
            load  = 0, 0, attr['sw']
            start = self.vertex_coordinates(key)
            end   = [start[i] + scale * load[i] for i in range(3)]
            name  = '{0}.force:selfweight.{1}'.format(self.name, key)
            arrow = 'start'
            lines.append({'start': start,
                          'end'  : end,
                          'name' : name,
                          'color': color,
                          'arrow': arrow, })
        rhino.xdraw_lines(lines, layer=layer, clear=False)

    def display_resultant(self,
                          keys,
                          display=True,
                          layer=None,
                          scale=None,
                          color=None):
        objects = rhino.get_objects(name='{0}.force:resultant.*'.format(self.name))
        rhino.delete_objects(objects)
        if not display:
            return
        lines = []
        layer = layer or self.layer
        color = color or self.color['force:reaction']
        scale = scale or self.scale['force:reaction']
        x, y, z = 0, 0, 0
        rx, ry, rz = 0, 0, 0
        count = 0
        for key in keys:
            attr = self.vertex[key]
            if not attr['is_anchor'] and not attr['is_fixed']:
                continue
            x     += attr['x']
            y     += attr['y']
            rx    += attr['rx']
            ry    += attr['ry']
            rz    += attr['rz']
            count += 1
        x  = x / count
        y  = y / count
        z  = z / count
        start = x, y, z
        end   = x + scale * rx, y + scale * ry, z + scale * rz
        name  = '{0}.force:resultant.{1}'.format(self.name, keys)
        arrow = 'start'
        lines.append({'start': start,
                      'end'  : end,
                      'name' : name,
                      'color': color,
                      'arrow': arrow, })
        rhino.xdraw_lines(lines, layer=layer, clear=False)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
