# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

from brg_rhino.datastructures.mixins import Mixin


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__date__       = 'Jun 19, 2015'


docs = [
    'Descriptors',
]


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
