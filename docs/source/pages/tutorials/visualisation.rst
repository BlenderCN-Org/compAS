.. _tutorials-visualisation:

********************************************************************************
Visualisation
********************************************************************************

.. plotters => simple 2D/3D viewing
.. viewers => (very) simple interaction
.. modellers? => advanced modelling capabilities


.. contents::


Plotters
========

.. plot::
    :include-source:

    import random
    import compas
    from compas.datastructures.network import Network

    network = Network.from_obj(compas.get_data('grid_irregular.obj'))

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

    for key, attr in network.vertices_iter(True):
        attr['color'] = random.choice(colors)

    network.plot(
        vsize=0.2,
        vcolor={key: attr['color'] for key, attr in network.vertices_iter(True)}
    )


Viewers
=======

.. code-block:: python

    


Rhinoceros 3D
=============

Exporting an animated GIF from Rhino
---------------------------------------- 

.. warning::

    This section is still under construction.

The following example shows how to export an animated GIF from Rhino, capturing 
a sequence of consecutive steps. E.g. the intermediate steps of an iterative
process.   

This example uses the CPython package imageio. This package (and any other CPython package) 
can be used from inside Rhino (IronPython) through a subprocess using the XFuncIO class. 


.. seealso::

    * :class:`compas.utilities.XFuncIO`


.. important::

    This code uses the python package imageio: 
    http://imageio.readthedocs.io/en/latest/installation.html 

    The resulting GIFs tend to have a rather large file size. Many GIF optimization
    tools are available online to post-process the GIFs produced with this method: 
    E.g.: You can use https://ezgif.com/optimize to significantly reduce the file 
    size of your GIFs. 

.. code-block:: python

    import os
    import math
    
    from compas.utilities.xfunc import XFunc
    from compas.geometry.spatial import subtract_vectors
    
    from compas_rhino.utilities.misc import screenshot_current_view
    
    import rhinoscriptsyntax as rs
    
    
    width = 1024    # width of gif
    height = 720    # height of gif
    
    frames = 45     # total number of frames
    fps = 25        # frames per second
    
    r = 5           # radius of bouncing ball
    d = 15          # height of bouncing ball
    
    # Select folder for the animated gif to be saved
    gif_path = rs.SaveFileName("Save", "Text Files (*.gif)|*.gif||")
    
    # create a temp folder to temporarily store the individual screenshots
    temp_path = os.path.dirname(os.path.abspath(gif_path)) + "\\temp\\"
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    
    sphere = rs.AddSphere((0, 0, r), r)
    
    files = []
    for i in range(frames):
        # make the sphere bounce
        delta = math.sin(i / frames * math.pi) * d - math.sin((max(0, i-1)) / frames * math.pi) * d
        sphere = rs.MoveObject(sphere,(0, 0, delta))
        # take a screenshot of the current view and sve it in the temp folder
        files.append(temp_path + str(i).zfill(5) + ".png")
        screenshot_current_view(files[-1], width, height, scale=0.5, draw_grid=True)
    
    try:
        # use XFuncIO to run a external process in CPython to compute the gif (imageio is required)
        print "Computing gif..."
        xrun = XFunc()
        fname = 'compas.utilities.animation.gif_from_images'
        xrun(fname, files, gif_path, fps , loop=0, reverse=True, pingpong=False, subrectangles=True)
    
        if xrun.error:
            print xrun.error
        else:
            print "Gif saved: {0}".format(gif_path)
    
    except:
        pass
    finally:
        # remove the individual screenshots PNGs and the temp folder
        for file in files:
            os.remove(file)
        os.rmdir(temp_path)


An example of an animated GIF created using the code above:

.. image:: /_images/gif_from_rhino.*


Grasshopper
===========


Blender
=======

