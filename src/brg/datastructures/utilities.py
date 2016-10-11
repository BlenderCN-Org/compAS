#

__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Oct 25, 2014'


__all__ = []


def identify_edge_chain(graph, points, tol):
    tol2 = tol**2
    keys = []
    for x, y, z in points:
        for key, attr in graph.vertices_iter(True):
            if (x - attr['x'])**2 < tol2 and (y - attr['y'])**2 < tol2 and (z - attr['z'])**2 < tol2:
                keys.append(key)
                break
    chain = []
    for i in range(len(keys) - 1):
        k1 = keys[i]
        k2 = keys[i + 1]
        if k2 in graph.edge[k1]:
            u, v = k1, k2
        else:
            u, v = k2, k1
        chain.append((u, v))
    if chain[0][1] in chain[1]:
        start = chain[0][0]
    else:
        start = chain[0][1]
    if chain[-1][0] in chain[-2]:
        end = chain[-1][1]
    else:
        end = chain[-1][0]
    return chain, start, end


def geometric_key(xyz, precision='3f', sanitize=True):
    if sanitize:
        if xyz[0]**2 < 1e-9:
            xyz[0] = 0.0
        if xyz[1]**2 < 1e-9:
            xyz[1] = 0.0
        if xyz[2]**2 < 1e-9:
            xyz[2] = 0.0
    return '{0[0]:.{1}},{0[1]:.{1}},{0[2]:.{1}}'.format(xyz, precision)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    pass
