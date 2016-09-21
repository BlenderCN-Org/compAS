# Wikipedia KDTree <http://en.wikipedia.org/wiki/Kd-tree>
# ActiveState KDTree <http://code.activestate.com/recipes/577497-kd-tree-for-nearest-neighbor-search-in-a-k-dimensional-space>

import collections
import math
import time
from random import random


__author__     = ['Matthias Rippmann', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__version__    = '0.1'
__email__      = 'vanmelet@ethz.ch'
__status__     = 'Development'
__date__       = 'Nov 4, 2014'


Node = collections.namedtuple("Node", 'point axis label left right')


def distance_sqrd(p1, p2):
    """computes squared distance bewteen p1, p2

    Parameters:
        p1, p2 (tuple): x,y,z point value

    Returns:
        float: squared distance bewteen p1, p2
    """
    return (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2


class KDTreeError(Exception):
    """"""
    pass


class KDTree(object):
    """A tree for nearest neighbor search in a k-dimensional space.
    """
    def __init__(self, objects=[]):
        # self.root = self.build_tree(list([objects]))
        self.root = self.build_tree(list([(objects[i], i) for i in xrange(len(objects))]))

    def build_tree(self, objects, axis=0):
        if not objects:
            return None
        objects.sort(key=lambda o: o[0][axis])
        median_idx = len(objects) // 2
        median_point, median_label = objects[median_idx]
        next_axis = (axis + 1) % 3
        return Node(median_point, axis, median_label,
                    self.build_tree(objects[:median_idx], next_axis),
                    self.build_tree(objects[median_idx + 1:], next_axis))

    def nearest_neighbor(self, destination, exclude=[]):
        best = [None, None, float('inf')]
        # state of search: best point found, its label,
        # lowest squared distance
        def recursive_search(here):
            if here is None:
                return
            point, axis, label, left, right = here
            here_sd = distance_sqrd(point, destination)
            if here_sd < best[2] and label not in exclude:
                best[:] = point, label, here_sd
            diff = destination[axis] - point[axis]
            close, away = (left, right) if diff <= 0 else (right, left)
            recursive_search(close)
            if diff ** 2 < best[2]:
                recursive_search(away)
        recursive_search(self.root)
        return best[0], best[1], math.sqrt(best[2])


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':
    # define random sample data
    npoints = 500
    points = [(random(), random(), 0) for i in xrange(npoints)]
    # rs.AddPoints(points)
    destination = (random(), random(), 0)

    # --------------------------------------------------------------------------
    # build tree

    start_cpu = time.clock()
    tree = KDTree(points)
    end_cpu = time.clock()
    print "{0} CPU seconds for building tree".format(end_cpu - start_cpu)

    # --------------------------------------------------------------------------
    # sorting (up to n closest neighbors) using the tree.nearest_neighbor search
    # this is the fastest way to do this for points > ~5000

    n = 3
    data = []
    exclude = []
    start_cpu = time.clock()
    for i in range(n):
        data.append(tree.nearest_neighbor(destination, exclude))
        # point, label, distance = t.nearest_neighbor(destination, exclude)
        exclude.append(data[-1][1])
    end_cpu = time.clock()
    print "{0} CPU seconds for {1} nearest neighbor(s)".format(end_cpu - start_cpu, n)

    # --------------------------------------------------------------------------
    # sorting using the python inbuilt functions (no initial KDTree necessary)

    start_cpu = time.clock()
    minsq = [distance_sqrd(p, destination) for p in points]
    list1, list2, list3 = zip(*sorted(zip(minsq, points, range(len(points)))))
    end_cpu = time.clock()
    print "{0} CPU seconds for Built-in Functions sorting".format(end_cpu - start_cpu)

    # --------------------------------------------------------------------------
    # sorting using the python inbuilt functions (no initial KDTree necessary)
    # this is the fastest for points < ~5000

    def SortPointListByDistance(refPt, ptList, revSort):
        distList = [(pt.DistanceTo(refPt), pt, i) for i, pt in enumerate(ptList)]
        distList.sort()
        if revSort:
            distList.reverse()
        return zip(*distList)

    # ptobjs = rs.coerce3dpointlist(zip(*points)[0])
    # start_cpu = time.clock()
    # temp = SortPointListByDistance(rs.coerce3dpoint(destination),ptobjs,False)
    # end_cpu = time.clock()
    # print "{0} CPU seconds for rhino common sorting".format(end_cpu-start_cpu)

    for datum in data:
        # rs.AddLine(datum[0], destination)
        print "Distance: {0}".format(datum[2])
