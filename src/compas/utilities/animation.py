import os
try:
    import imageio
except:
    pass


__author__    = ['Matthias Rippmann', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'rippmann@arch.ethz.ch'


def test():
    print dir(imageio)


def gif_from_images(path, name):
    filenames = []

    for file in os.listdir(path):
        if file.endswith(".jpg"):
            filenames.append(os.path.join(path, file))

    with imageio.get_writer(os.path.join(path, name, '.gif'), mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
