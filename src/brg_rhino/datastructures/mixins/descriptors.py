# -*- coding: utf-8 -*-
# @Date    : 2016-03-21 09:50:20
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$

from brg_rhino.datastructures.mixins import Mixin


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'Apache License, Version 2.0'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Jun 19, 2015'


class Descriptors(Mixin):

    @property
    def layer(self):
        return self.attributes.get('layer')

    @layer.setter
    def layer(self, layer):
        self.attributes['layer'] = layer

