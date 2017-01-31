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


# @todo: rempove the callbacks
# @todo: add specialised bfs to mesh orientation module
# @todo: move to _graph module


# ==============================================================================
# depth-first
# ==============================================================================


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
        root (str): The vertex from which to start the depth-first search.
        callback (callable): Optional. A function that is called on every node
            when it is found. Default is ``None``.

    Returns:
        list: A depth-first ordering of all vertices in the network.

    Raises:
        AssertionError: If the callback is provided, but is not callable.

    Examples:
        >>> import brg
        >>> network = Network.from_obj(brg.get_data('lines.obj'))
        >>> print network_dfs(network, network.get_any_vertex())

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


# def network_dfs_tree(adjacency, root):
#     adjacency = dict((key, set(nbrs)) for key, nbrs in adjacency.iteritems())
#     tovisit = [(root, [root])]
#     visited = {}
#     while tovisit:
#         # a node to visit
#         # and the nodes that have been visited to get there
#         node, path = tovisit.pop()
#         # add every unvisited nbr
#         # and the path that leads to it
#         for nbr in adjacency[node] - set(path):
#             # if the nbr is the goal, yield the path that leads to it
#             tovisit.append((nbr, path + [nbr]))
#         visited[node] = path
#     return visited


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
        node, path = tovisit.pop()
        # add every unvisited nbr
        # and the path that leads to it
        for nbr in adjacency[node] - set(path):
            # if the nbr is the goal, yield the path that leads to it
            if nbr == goal:
                yield path + [nbr]
            else:
                tovisit.append((nbr, path + [nbr]))


# ==============================================================================
# depth-first
# ==============================================================================


def network_bfs(adjacency, root, callback=None):
    """Return all nodes of a connected component containing 'root' of a network
    represented by an adjacency dictionary.

    This implementation uses a queue to keep track of nodes to visit.
    The principle of a queue is FIFO. In Python, a deque (double-ended queue) is
    ideal for removing elements from the beginning, i.e. from the 'left'.

    In a breadth-first search, all unvisited neighbours of a node are visited
    first. When a neighbour is visited, its univisited neighbours are added to
    the list of nodes to visit.

    Parameters:
        adjacency (dict): An adjacency dictionary. Each key represents a vertex
            and maps to a list of neighbouring vertex keys.
        root (str): The vertex from which to start the breadth-first search.
        callback (callable): Optional. A function that is called on every node
            when it is found. Default is ``None``.

    Returns:
        list: A breadth-first ordering of all vertices in the network.

    Raises:
        AssertionError: If the callback is provided, but is not callable.

    Examples:
        >>> import brg
        >>> network = Network.from_obj(brg.get_data('lines.obj'))

    Notes:
        By appending the neighbours to the end of the list of nodes to visit,
        and by visiting the nodes at the start of the list first, the network is
        traversed in *breadth-first* order.

    """
    if callback:
        assert callable(callback), 'The provided callback is not callable: {0}'.format(callback)
    tovisit = deque([root])
    tree = [root]
    visited = set(tree)
    while tovisit:
        node = tovisit.popleft()
        # for nbr in adjacency[node] - visited:
        #     tovisit
        for nbr in adjacency[node]:
            if nbr not in visited:
                tovisit.append(nbr)
                visited.add(nbr)
                tree.append(nbr)
                if callback:
                    callback(node, nbr)
    return tree


def network_bfs2(adjacency, root):
    adjacency = dict((key, set(nbrs)) for key, nbrs in adjacency.iteritems())
    tovisit = deque([root])
    visited = set()
    while tovisit:
        # visit all the neighbours of a node first
        # before moving on to their respective neighbours in the same order
        node = tovisit.popleft()
        if node not in visited:
            visited.add(node)
            # add all the neighbours of the current node that have not yet been visited
            tovisit.extend(adjacency[node] - visited)
    # returning this is pointless
    # since visited is a set
    # and sets have no order
    return visited


def network_bfs_paths(adjacency, root, goal):
    """Return all paths from root to goal.

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
    """"""
    try:
        return next(network_bfs_paths(adjacency, root, goal))
    except StopIteration:
        return None


def network_shortest_path_dijkstra(adjacency, weight, goal):
    """"""
    adjacency = dict((key, set(nbrs)) for key, nbrs in adjacency.items())
    dist = dict((key, 0 if key == goal else 1e17) for key in adjacency)
    visited = set()
    tovisit = set(adjacency.keys())
    while tovisit:
        node = min(tovisit, key=lambda k: dist[k])
        visited.add(node)
        tovisit.remove(node)
        for nbr in adjacency[node]:
            if dist[nbr] > dist[node] + weight[(node, nbr)]:
                dist[nbr] = dist[node] + weight[(node, nbr)]
    return dist


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import brg
    from brg.datastructures.network import Network

    network = Network.from_obj(brg.get_data('lines.obj'))

    # tree = network_dfs_tree(network.adjacency, '0')

    # # start with the longest path
    # # remove all keys from the dictionary that are in this path

    # longest = sorted(tree.items(), key=lambda item: len(item[1]))

    # for node, path in longest:
    #     print node, path

    # spine = {}
    # for i, key in enumerate(longest[-1][1]):
    #     spine[key] = i

    # for key in spine:
    #     try:
    #         del tree[key]
    #     except KeyError:
    #         pass

    # print

    # for node, path in tree.items():
    #     print node, path

    # # while longest:
    # #     node, path = longest.pop()
    # #     if node in tree:
    # #         print node, path
    # #         for key in path:
    # #             try:
    # #                 del tree[key]
    # #             except KeyError:
    # #                 pass

    # edges = []
    # for i in range(len(longest[-1][1]) - 1):
    #     u = longest[-1][1][i]
    #     v = longest[-1][1][i + 1]
    #     if v not in network.edge[u]:
    #         u, v = v, u
    #     edges.append([u, v])

    path = network_shortest_path(network.adjacency, '0', '26')

    weight = dict(((u, v), network.edge_length(u, v)) for u, v in network.edges())
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    dist = network_shortest_path_dijkstra(network.adjacency, weight, '0')

    for key, d in dist.items():
        print key, d

    edges = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if v not in network.edge[u]:
            u, v = v, u
        edges.append([u, v])

    network.plot(
        vlabel={key: key for key in network},
        vcolor={key: (255, 0, 0) for key in (path[0], path[-1])},
        vsize=0.15,
        ecolor={(u, v): (255, 0, 0) for u, v in edges},
        ewidth={(u, v): 2.0 for u, v in edges}
    )
