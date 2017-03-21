.. _notes_other-python-implementations:

********************************************************************************
Other Python implementations
********************************************************************************

.. contents::


IronPython
==========


Jython
======

Resources
---------

* Jython project (http://www.jython.org/)
* Jython Wiki (https://wiki.python.org/jython)
* JyNI (http://jyni.org/)
* PyPlotter (https://github.com/jecki/PyPlotter)


System variables
----------------

::

    export PATH="/Users/.../jython270/bin:$PATH"

::

    export JYTHONPATH="Users/.../compAS/core/src:$JYTHONPATH"
    export JYTHONPATH="Users/.../compAS/packages/src:$JYTHONPATH"


.. note::

    The Jython bin contains among other things ``pip`` and ``easy_install`` executables.
    By adding the Jython bin to your path, these overwrite the *default* (C)Python
    versions of thos executables. To avoid unexpected results when trying to install
    Python packages, you may wnat to consider renaming the Jython versions, for example
    to ``jy-pip`` and ``jy-easy_install``.


Code editor configuration
-------------------------

::

    {
        "build_systems":
        [
            {
                "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
                "name": "Anaconda Python Builder",
                "selector": "source.python",
                "shell_cmd": "\"python\" -u \"$file\""
            },
            {
                "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
                "name": "Anaconda Jython Builder",
                "selector": "source.python",
                "shell_cmd": "\"jython\" -u \"$file\""
            }
        ],
    }


Examples
--------

.. code-block:: python

    """
    A simple example that shows button event handling

    Greg Moore
    Sept 2007
    """

    from javax.swing import *
    from java.awt import BorderLayout


    class Example:

        def __init__(self):
            frame = JFrame("Jython Example JButton")
            frame.setSize(100, 100)
            frame.setLayout(BorderLayout())
            self.label = JLabel('Hello from Jython')
            frame.add(self.label, BorderLayout.NORTH)
            button = JButton('Click Me', actionPerformed=self.setText)
            frame.add(button, BorderLayout.SOUTH)
            frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
            frame.setVisible(True)

        def setText(self, event):
            self.label.text = 'Button clicked.'


    if __name__ == '__main__':
        Example()


.. code-block:: python

    import math

    from PyPlotter import awtGfx as GfxDriver  # 'awtGfx' for jython, 'tkGfx' for python
    from PyPlotter import Graph, Gfx

    gfx = GfxDriver.Window(title="Function Plotter")
    gr = Graph.Cartesian(gfx, -4.0, -2.0, 4.0, 2.0)

    gr.addPen("sin(x)", Gfx.RED_PEN)

    for x in gr.xaxisSteps(-4.0, 4.0):
        gr.addValue("sin(x)", x, math.sin(x))

    gfx.waitUntilClosed()
