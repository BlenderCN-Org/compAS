from __future__ import print_function

import os
import math

from compas_rhino.utilities import XFunc
from compas_rhino.utilities import screenshot_current_view

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
    delta = math.sin(i / frames * math.pi) * d - math.sin((max(0, i - 1)) / frames * math.pi) * d
    sphere = rs.MoveObject(sphere, (0, 0, delta))
    # take a screenshot of the current view and save it in the temp folder
    files.append(temp_path + str(i).zfill(5) + ".png")
    screenshot_current_view(files[-1], width, height, scale=0.5, draw_grid=True)

try:
    # use XFuncIO to run a external process in CPython to compute the gif (imageio is required)
    print("Computing gif...")

    xrun = XFunc()
    fname = 'compas.utilities.animation.gif_from_images'
    xrun(fname, files, gif_path, fps , loop=0, reverse=True, pingpong=False, subrectangles=True)

    if xrun.error:
        print(xrun.error)
    else:
        print("Gif saved: {0}".format(gif_path))

except:
    pass

finally:
    # remove the individual screenshots PNGs and the temp folder
    for file in files:
        os.remove(file)
    os.rmdir(temp_path)
