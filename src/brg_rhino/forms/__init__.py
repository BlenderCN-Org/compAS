# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod

try:
    from System.Windows.Forms import DialogResult
    from System.Windows.Forms import FormBorderStyle
    from System.Windows.Forms import Form as WinForm
    import Rhino

except ImportError as e:

    import platform
    if platform.system() == 'Windows':
        raise e

    class WinForm(object):
        pass


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'


class Form(WinForm):
    """"""

    __metaclass__ = ABCMeta

    def __init__(self, title='RhinoForm', width=None, height=None):
        self.Text = title
        if width:
            self.Width = width
        if height:
            self.Height = height
        self.MaximizeBox = False
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.SuspendLayout()
        self.init()
        self.ResumeLayout()
        self.FormClosed += self.on_form_closed

    @abstractmethod
    def init(self):
        pass

    def show(self):
        if Rhino.UI.Dialogs.ShowSemiModal(self) == DialogResult.OK:
            return True

    def on_form_closed(self, sender, eargs):
        pass
