__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = '2015-12-03 13:43:05'


def cycle_face(face, count=1000):
    start = iter(face).next()
    v = face[start]
    vertices = [start]
    while count:
        if v == start:
            break
        vertices.append(v)
        v = face[v]
        count -= 1
    return vertices
