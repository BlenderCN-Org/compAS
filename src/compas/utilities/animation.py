import os
try:
    import imageio
except:
    pass


__author__    = ['Matthias Rippmann', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'rippmann@arch.ethz.ch'


def gif_from_images(files, gif_path, fps=10, loop=0, reverse=False, pingpong=False, subrectangles=True):
     
    if reverse:
        files.reverse()

    if pingpong:
        rev_files = files[:]
        rev_files.reverse()
        files += rev_files 
     
    with imageio.get_writer(gif_path, 
                            mode = 'I', 
                            fps = fps, 
                            loop = loop, 
                            subrectangles = subrectangles) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)
    