import os

try:
    import imageio
except:
    pass


__author__    = ['Matthias Rippmann', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'rippmann@arch.ethz.ch'


def gif_from_images(files,
                    gif_path,
                    fps=10,
                    loop=0,
                    reverse=False,
                    pingpong=False,
                    subrectangles=True,
                    delete_files=False):
    """Create an animated GIF from a series of images.

    Parameters:
        files (list): The image series.
        gif_path (str): The location to svae the- GIF.
        fps (int): Optional. Frames per second. Default is ``10``.
        loop ():
        reverse (bool): Optional. Flag for reversing the image series. Default is ``False``.
        pingpong (bool): Optional. ... Default is ``False``.
        subrectangles (bool): Optional. ... Default is ``True``.
    """
    if reverse:
        files.reverse()

    if pingpong:
        files += files[::-1]

    with imageio.get_writer(gif_path,
                            mode='I',
                            fps=fps,
                            loop=loop,
                            subrectangles=subrectangles) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)

    if delete_files:
        for filename in files:
            os.remove(filename)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas

    base  = 'screenshots/mesh-remeshing-'
    files = [os.path.join(compas.TEMP, base + str(i).zfill(5) + '.png') for i in [0] + range(52, 172) if i % 2 == 0]

    gif_from_images(files, os.path.join(compas.TEMP, 'screenshots/mesh-remeshing.gif'))
