
# 1) construct a list of odd numbers below 20 and then reverse the list in place
#
# - don't use 'reverse' or 'reversed'

a = range(1, 20, 2)
a[:] = a[::-1]


# 2) given a list of 3D points (xyz coordinates),
#    construct a map that links 3D locations to items in the list,
#
# - the tolerance of the map is 1e-3
# - i.e. points closer together than the tolerance should map to the same point

points = []
lookup = dict(('{0[0]:.3f},{0[1]:.3f},{0[2]:.3f}'.format(xyz), i) for i, xyz in enumerate(points))


# 3) define a (dummy) function that takes:
#
# - two positional arguments
# - 1 optional argument with default value None
# - an unknown number of additional keyword arguments

def f(arg1, arg2, arg3=None, **kwargs):
    pass


# 4) demonstrate the principle of a cyclic list.
#
# - given a list of length n
# - allow for indexing by m >= n, and -m <= -n

a = [0, 1, 2]
item = a[5 % len(a)]


# 5) construct a list 'c' with all elements in 'b' that are not in 'a'

a = [1, 4, 7, 9, 12, 19, 13, 3, 2]
b = range(20)
c = list(set(b) - set(a))


# 6) construct a list 'c' with all elements in 'b' that are not in 'a',
#    but while preserving the order of elements in 'b'

a = set(a)
c = [x for x in b if x not in a]


# 7) construct a list of 1000 random integers between 1 and 1000000.
#    then find the index of the item with the highest value.
#
# - looping over the entire list while comparing values is not the answer i am looking for.

from random import randint

a = dict((randint(1, 1000000), i) for i in range(1000))
k, v = sorted(a.items(), key=lambda x: x[1])[-1]


# 8) define a class with a method that behaves as if it is abstract

class MyAbstractClass(object):
    def method(self):
        raise NotImplementedError


# 9) define a class with alternative constructors that can be called explicitly
#
# o = MyClass()
# o = MyClass.from_xxx()
# o = MyClass.from_yyy()

class MyClass(object):
    def __init__(self):
        pass

    @classmethod
    def from_xxx(cls):
        return cls()

    @classmethod
    def from_yyy(cls):
        return cls()


# 10) define a vector object that supports the following operations:
#
# v1 = Vector(1, 2, 3)
# v2 = Vector(1, 2, 3)
# v3 = v1 + v2
# v3 * 2

class Vector(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)

    def __mul__(self, n):
        self.x *= n
        self.y *= n
        self.z *= n


# 11) write a function that does a counter-clockwise check of 3 points A, B, C.
#
# - A, B, C are in the xy-plane (i.e. z=0)
# - the function should return True if the rotation from vector AB onto AC is counter-clockwise.

def ccw_(A, B, C):
    return (B[0] - A[0]) * (C[1] - A[1]) > (B[1] - A[1]) * (C[0] - A[0])


# 12) write a (memoized) recursive fibonacci function.

def rfib(n, memo={}):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n not in memo:
        memo[n] = rfib(n - 2) + rfib(n - 1)
    return memo[n]


# 13) write a function that does a breadth-first seach of a given network starting at a given root element.
#
# - the network is given as a dictionary of adjacencies: nbrs = adjacency[node].
# - signature: def bfs(root, adjacency): ...
# - return a list of nodes in breadth-first order


# 14) write a simple bubble sort function

