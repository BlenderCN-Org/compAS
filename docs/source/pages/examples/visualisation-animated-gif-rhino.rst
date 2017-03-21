.. _example_visualisation-animated-gif-rhino:

********************************************************************************
Visualisation: export an animated GIF from Rhino
********************************************************************************

.. image:: /_images/examples_gif-from-rhino.*


The following example shows how to export an animated GIF from Rhino, capturing 
a sequence of consecutive steps. E.g. the intermediate steps of an iterative
process.   

This example uses the CPython package imageio. This package (and any other CPython package) 
can be used from inside Rhino (IronPython) through a subprocess using the XFuncIO class. 


.. seealso::

    * :class:`compas_rhino.utilities.XFunc`


.. important::

    This code uses the python package imageio: 
    http://imageio.readthedocs.io/en/latest/installation.html 

    The resulting GIFs tend to have a rather large file size. Many GIF optimization
    tools are available online to post-process the GIFs produced with this method: 
    E.g.: You can use https://ezgif.com/optimize to significantly reduce the file 
    size of your GIFs. 


.. literalinclude:: /../../examples/visualisation-animated-gif-rhino.py
