__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


class DXF(object):
    pass


class DXFReader(object):
    """"""

    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        with open(self.filepath, 'rb') as fp:
            for line in fp:
                print line.strip()


class DXFParser(object):
    pass


class DXFComposer(object):
    pass


class DXFWriter(object):
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
