from brg_rhino.mixins import Mixin


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Descriptors', ]


class Descriptors(Mixin):

    @property
    def layer(self):
        """:obj:`str` : The layer of the network.

        Any value of appropriate type assigned to this property will be stored in
        the instance's attribute dict.
        """
        return self.attributes.get('layer')

    @layer.setter
    def layer(self, layer):
        self.attributes['layer'] = layer


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
