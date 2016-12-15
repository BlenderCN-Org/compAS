""""""

__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


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
