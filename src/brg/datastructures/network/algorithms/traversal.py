from collections import deque


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'network_dfs',
    'network_bfs',
    'network_bfs2',
    'network_dfs_paths',
    'network_bfs_paths',
    'network_shortest_path'
]


def network_dfs(adjacency, root, callback=None):
    """
    Return all nodes of a connected component containing 'root' of a network
    represented by an adjacency dictionary.

    This implementation uses a 'to visit' stack. The principle of a stack
    is LIFO. In Python, a list is a stack.

    Initially only the root element is on the stack. While there are still
    elements on the stack, the node on top of the stack is 'popped off' and if
    this node was not already visited, its neighbours are added to the stack if
    they hadn't already been visited themselves.

    Since the last element on top of the stack is always popped off, the
    algorithm goes deeper and deeper in the datastructure, until it reaches a
    node without (unvisited) neighbours and then backtracks. Once a new node
    with unvisited neighbours is found, there too it will go as deep as possible
    before backtracking again, and so on. Once there are no more nodes on the
    stack, the entire structure has been traversed.

    Note that this returns a depth-first spanning tree of a connected component
    of the network.

    Parameters:
        adjacency (dict): An adjacency dictionary. Each key represents a vertex
            and maps to a list of neighbouring vertex keys.
        root (str): The vertex to start the depth-first search from.
        callback (callable): Optional. A function that is called on every node
            when it is found. Default is ``None``.

    Returns:
        list: A depth-first ordering of all vertices in the network.

    Raises:
        AssertionError: If the callback is provided, but it is not callable.

    Examples:
        >>> import brg
        >>> network = Network.from_obj(brg.get_data('lines.obj'))
        >>> network_dfs(network)

    Notes:
        ...

    See Also:
        ...

    """
    if callback:
        assert callable(callback), 'The provided callback is not callable: {0}'.format(callback)
    adjacency = dict((key, set(nbrs)) for key, nbrs in adjacency.iteritems())
    tovisit = [root]
    visited = set()
    tree = []
    while tovisit:
        # pop the last added element from the stack
        node = tovisit.pop()
        if node not in visited:
            # mark the node as visited
            visited.add(node)
            tree.append(node)
            # call the callback
            if callback:
                callback(node)
            # add the unvisited nbrs to the stack
            tovisit.extend(adjacency[node] - visited)
    return tree


def network_bfs(adjacency, root, func=None):
    """
    Return all nodes of a connected component containing 'root' of a network
    represented by an adjacency dictionary.

    This implementation uses a queue to keep track of nodes to visit.
    The principle of a queue is FIFO. In Python, a deque (double-ended queue) is
    ideal for removing elements from the beginning, i.e. from the 'left'.
    """
    tovisit = deque([root])
    tree = [root]
    visited = set(tree)
    while tovisit:
        node = tovisit.popleft()
        for nbr in adjacency[node]:
            if nbr not in visited:
                tovisit.append(nbr)
                visited.add(nbr)
                tree.append(nbr)
                if func:
                    func(node, nbr)
    return tree


def network_bfs2(adjacency, root):
    adjacency = dict((key, set(nbrs)) for key, nbrs in adjacency.iteritems())
    tovisit = deque([root])
    visited = set()
    while tovisit:
        node = tovisit.popleft()
        if node not in visited:
            visited.add(node)
            tovisit.extend(adjacency[node] - visited)
    return visited


def network_dfs_tree(adjacency, root):
    pass


def network_dfs_paths(adjacency, root, goal):
    """
    Yield all paths that lead from a root node to a specific goal.

    The implementation is based on
    http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
    """
    adjacency = dict((key, set(nbrs)) for key, nbrs in adjacency.iteritems())
    tovisit = [(root, [root])]
    while tovisit:
        # get the last added node and the path that led to that node
        node, visited = tovisit.pop()
        # add every unvisited nbr
        # and the path that leads to it
        for nbr in adjacency[node] - set(visited):
            # if the nbr is the goal, yield the path that leads to it
            if nbr == goal:
                yield visited + [nbr]
            else:
                tovisit.extend((nbr, visited + [nbr]))


def network_bfs_paths(adjacency, root, goal):
    """
    Return all paths from root to goal.

    Due to the nature of the search, the first path returned is the shortest.
    """
    adjacency = dict((key, set(nbrs)) for key, nbrs in adjacency.iteritems())
    tovisit = deque([(root, [root])])
    while tovisit:
        node, path = tovisit.popleft()
        for nbr in adjacency[node] - set(path):
            if nbr == goal:
                yield path + [nbr]
            else:
                tovisit.append((nbr, path + [nbr]))


def network_shortest_path(adjacency, root, goal):
    try:
        return next(network_bfs_paths(adjacency, root, goal))
    except StopIteration:
        return None


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('lines.obj'))

    print network_dfs(network.adjacency, '0')

    network.plot(vlabel={key: key for key in network})
