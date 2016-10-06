# -*- coding: utf-8 -*-
# @Date    : 2016-03-10 14:51:10
# @Author  : Tom Van Mele (vanmelet@ethz.ch)
# @Version : $Id$


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 7, 2014'


class ToolController(object):
    """"""

    instancename = None

    def __init__(self):
        self.name = None
        self.registry = {}
        self.layers = {}
        self.settings = {}
        self.macrocontrollers = {}

    def init(self):
        raise NotImplementedError

    def reload(self):
        raise NotImplementedError

    def load_workspace(self):
        raise NotImplementedError

    def save_workspace(self):
        raise NotImplementedError

    def run_utility(self, script):
        raise NotImplementedError

    def _cleanup(self):
        raise NotImplementedError

    def _get_setting(self, name, default=None):
        value = self.registry.get(name, self.settings.get(name, default))
        return value

    def _set_setting(self, name, value):
        self.registry[name] = value

    def _update_settings(self, settings):
        self.registry.update(settings)

    def _add_macrocontroller(self, cls):
        c = cls(self)
        self.macrocontrollers[cls.instancename] = c
        setattr(self, cls.instancename, c)


class MacroController(object):
    """"""

    instancename = None

    def __init__(self, tool=None):
        self.tool = tool
