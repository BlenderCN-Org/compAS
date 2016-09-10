# -*- coding: utf-8 -*-

import System

from System.Windows.Forms import PictureBox
from System.Windows.Forms import PictureBoxSizeMode
from System.Windows.Forms import DockStyle

from System.Drawing import Image

from _form import Form


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'Apache License, Version 2.0'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Sep 26, 2014'


class ImageForm(Form):
    """"""

    def __init__(self, imagepath, title='ImageForm'):
        self.imagepath = imagepath
        super(ImageForm, self).__init__(title)

    def init(self):
        box = PictureBox()
        box.Dock = DockStyle.Fill
        box.SizeMode = PictureBoxSizeMode.AutoSize
        box.Image = Image.FromFile(self.imagepath)
        self.image = box.Image
        self.Controls.Add(box)
        self.ClientSize = box.Size

    def on_form_closed(self, sender, e):
        self.image.Dispose()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    form = ImageForm('./data/image.gif')
    form.show()
