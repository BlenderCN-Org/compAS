'''
Created on 04.07.2012

@author: vanmelet
@todo: use numpy arrays for all internal network calculations.
@todo: use @property to make sure that external calculators retrieve matrices
'''

################################################################################
# IMPORTS
################################################################################

from math import pi

from scipy import array, asarray, zeros, ones, eye
from scipy import dot, where, sum, absolute, diag, nonzero, vstack, hstack
#from scipy.weave import converters
from scipy.sparse import coo_matrix, lil_matrix, csr_matrix, spdiags

from vector import angle

import networkx as nx
import matplotlib.pyplot as plt

################################################################################
# FUNCTION  DEFINITIONS
################################################################################
def dfs(A, s):
    '''Perform a recursive Depth-first Search to number the vertices 
    in a connected graph and transform the graph into a palm tree P.'''
    path = []
    numbers = {}
    palm = []
    is_frond = {}
    n = [0]
    lowpt1 = {}
    lowpt2 = {}
    #############################
    # the recursive algorithm
    def recurse(v,u):
        path.append(v)
        n[0] = n[0] + 1
        numbers[v] = n[0]
        lowpt1[v] = n[0]
        lowpt2[v] = n[0]
        for w in A[v]:
            try:
                if (numbers[w] < numbers[v]) and (w != u):
                    palm.append((v,w))
                    is_frond[(v,w)] = 1
                    if numbers[w] < lowpt1[v]:
                        lowpt2[v] = lowpt1[v]
                        lowpt1[v] = numbers[w]
                    elif numbers[w] > lowpt1[v]:
                        lowpt2[v] = min(lowpt2[v],numbers[w])
            except KeyError:
                palm.append((v,w))
                is_frond[(v,w)] = 0
                recurse(w,v)
                if lowpt1[w] < lowpt1[v]:
                    lowpt2[v] = min(lowpt1[v],lowpt2[w])
                    lowpt1[v] = lowpt1[w]
                elif lowpt1[w] == lowpt1[v]:
                    lowpt2[v] = min(lowpt2[v],lowpt2[w])
                else:
                    lowpt2[v] = min(lowpt2[v],lowpt1[w])
    recurse(s,0)
    return path,numbers,palm,is_frond,lowpt1,lowpt2

################################################################################
################################################################################
################################################################################
# GRAPH BASECLASS DEFINITION
################################################################################
################################################################################
################################################################################

class Graph(object):
    ''''''
    def __init__(self, edges = None, vertices = None, anchors = None):
        '''Constructor'''
        # private lists
        self._edges      = None
        self._vertices   = None
        self._anchors    = None
        self._cycles     = None
        self._centroids  = None
        self._degree     = None
        self._indegree   = None
        self._outdegree  = None
        self._adjacency  = None
        self._incidence  = None
        self._attributes = None
        # belong to helper functions
        # should (may)be not be declared here
        self._traverses  = None
        self._ocycle     = None
        self._ocycles    = None
        self._icycles    = None
        # numpy arrays
        self._V = None
        self._E = None
        self._I = None
        self._L = None
        self._A = None
        self._D = None
        # scalars
        self._v = None
        self._e = None
        self._c = None
        # initialise if edge vertex pairs are provided
        
        
    ############################################################################
    # API for numerical calculations
    ############################################################################
    
    def V(self):
        ''''''
        if self._V is None:
            vertices = self.vertices()
            self._V = array(vertices)
        return self._V 

    def I(self):
        '''Directed incidence matrix I as a [n x m] numpy array.
        -1 if vertex is start of edge.
        +1 if vertex is end of edge.
        edges are directed from lower to higher vertex indices.'''
        if self._I is None:
            try :
                v = self.v()
                e = self.e()
                self._I = zeros((v,e))
                edges = self.edges()
                for i,edge in enumerate(edges):
                    self._I[edge[0],i] = -1
                    self._I[edge[1],i] = +1
            except:
                self._I = None
        return self._I
            
    def L(self):
        '''Laplacian matrix L as a [n x n] numpy array.
        L = D-A 
        L = dot(I,I.T)'''
        if self._L is None:
            try:
                I = self.I()
                self._L = dot(I,I.T)
            except:
                self._L = None
        return self._L
    
    def A(self):
        '''Adjacency matrix A as a [n x n] numpy array.
        A = abs(L) - diag(diag(L))'''
        if self._A is None:
            try:
                L = self.L()
                # self._A = np.fill_diagonal(absolute(self.L),0)
                self._A = absolute(L) - diag(diag(L))
            except:
                self._A = None
        return self._A

    def D(self):
        '''Degree matrix D as a [n x x] numpy array.
        D = diag(sum(A, axis=1))
        D = (I != 0).sum(1)'''
        if self._D is None:
            try:
                A = self.A()
                # self._D = (I != 0).sum(1)
                self._D = diag(sum(A, axis=1))
            except:
                self._D = None
        return self._D
    
    ############################################################################
    # API for general properties
    ############################################################################

    def v(self):
        ''''''
        if self._v is None:
            try:
                vertices = self.vertices()
                self._v = len(vertices)
            except:
                self._v = None
        return self._v
    
    def e(self):
        ''''''
        if self._e is None:
            try:
                edges = self.edges()
                self._e = len(edges)
            except:
                self._e = None
        return self._e

    def c(self):
        ''''''
        if self._c is None:
            try:
                cycles = self.cycles()
                self._c = len(cycles)
            except:
                self._c = None
        return self._c
    
    def edges(self, edges = None):
        ''''''
        if edges is None:
            return self._edges
        else:
            self._edges = edges

    def vertices(self, vertices = None):
        ''''''
        if vertices is None:
            return self._vertices
        else:
            self._vertices = vertices
        
    def anchors(self, anchors = None):
        ''''''
        if anchors is None:
            return self._anchors
        else:
            self._anchors = anchors

    ############################################################################
    # API for graph properties
    ############################################################################

    def incidence(self, n):
        ''''''
        pass

    def neighbours(self, n):
        ''''''
        '''Returns an dictionary with node numbers as keys and arrays of 
        adjacent nodes as values.
        If a list of nodes is provided, only the adjacency dictionary for these
        nodes is returned.'''
        A = self.A()
        if self._adjacency is None:
            self._adjacency = dict([(i,nonzero(row)[0]) for i,row in enumerate(A)])
        return dict([(i,self._adjacency[i]) for i in n])

    def adjacency(self):
        '''Calculates and returns the adjacency list of the graph 
        as a dictionary.'''
        A = self.A()
        if self._adjacency is None:
            self._adjacency = dict([(i,nonzero(row)[0]) for i,row in enumerate(A)])
        return self._adjacency
        
    def degree(self, n = None):
        '''Returns a dictionary with vertex numbers as keys and vertex degrees
        as values.
        If a list of vertex numbers is provided, only the degree dictionary for
        these vertices is returned.'''
        D = self.D()
        if self._degree is None:
            self._degree = dict([(i,d) for i,d in enumerate(diag(D))])
        if n is None:
            return self._degree
        else:
            return dict([(i,self._degree[i]) for i in n])
        
    def paths(self):
        ''''''
        pass
    
    def cycle_basis(self):
        ''''''
        pass
        
    def cycles(self):
        ''''''
        if self._cycles is not None:
            return self._cycles
        edges = self.edges()
        self._traverses = {}
        cycles = []
        ocycles = []
        # find the outer cycle
        sp = self.bottom_left()
        ep = self.first_neighbour(sp)
        ocycle = self.edge_cycle(sp, ep)
        # find the inner cycles
        for sp,ep in edges:
            try:
                self._traverses[(sp,ep)]
            except KeyError:
                cycle = self.edge_cycle(sp,ep)
                cycles.append(cycle)
        # break all cycles
        breakpoints = self.anchors()
        breakpoint_indices = [i for i,n in enumerate(ocycle) if n in breakpoints]
        for i in range(len(breakpoint_indices) - 1) :
            ocycles.append(ocycle[breakpoint_indices[i] : breakpoint_indices[i+1] + 1])
        self._cycles = cycles + ocycles
        return self._cycles
        
    def centroids(self):
        ''''''
        V = self.V()
        if self._centroids is not None:
            return self._centroids
        self._centroids = []
        cycles = self.cycles()
        for c in cycles:
            vertices = list(set(c))
            coords = V[vertices,:]
            centroid = (sum(coords, axis=0) / len(vertices)).tolist()
            self._centroids.append(centroid) 
        return self._centroids
    
    def barycenters(self):
        ''''''
        pass
    
    ############################################################################
    # ????
    # some of these should (may)be moved out of the class 
    # and added as module helpers 
    ############################################################################

    def init(self):
        '''This method should be called to initialise the graph 
        if it was created without edge information.'''
        edges = self.edges()
        # create the adjacency list
        # this will produce a 'directed' adjacency list
        adjacency = {}
        adjacency_out = {}
        for e in edges:
            try:
                adjacency[e[0]].append(e[1])
            except:
                adjacency[e[0]] = []
                adjacency[e[0]].append(e[1])
            try:
                adjacency[e[1]].append(e[0])
            except:
                adjacency[e[1]] = []
                adjacency[e[1]].append(e[0])
            try:
                adjacency_out[e[0]].append(e[1])
            except:
                adjacency_out[e[0]] = []
                adjacency_out[e[0]].append(e[1])
        # degree
        degree = dict([(a,len(adjacency[a])) for a in adjacency])
        v = len(degree)
        # incidence matrix
        # degree metrix
        D = spdiags([degree[n] for n in range(v)], 0, v,v, 'csr')
        # adjacency matrix
        A = zeros((v,v))
        for n in range(v):
            A[n,adjacency[n]] = 1
        A = lil_matrix(A).tocsr()
        # laplacian matrix
        L = D - A
        
        
    def analyse(self):
        '''Convenience function that returns'''
        self.v()
        self.e()
        self.c()
    
    ############################################################################
    # planarity 
    ############################################################################

    def is_planar(self):
        ''''''
        # Step 1: check the number of edges
        e = self.e()
        v = self.v()
        if e > 3*v - 3:
            return False
        # Step 2: decompose graph in biconnected components
        G = nx.Graph(self.edges())
        BICOMPS = nx.biconnected_component_subgraphs(G)
        # Step 3: check each component
        for B in BICOMPS:
            B_adjacency = dict(zip(B.nodes(),B.adjacency_list()))
            # explore component C to number its vertices and transform it into 
            # a palm tree P => dfs on adjacency list of component
            path,numbers,palm,frond,lowpt1,lowpt2 = dfs(B_adjacency, B_adjacency.keys()[0])
            print 'path    : {0}'.format(path)
            print 'numbers : {0}'.format(numbers)
            print 'palm    : {0}'.format(palm)
            print 'frond   : {0}'.format(frond)
            # determine edge values of palm based on is_frond and LOWPT2(w) value
            # create sorted adjacency list
            # renumber fronds
            A = self.sorted_adjacency_list(palm, len(path), numbers, frond, lowpt1, lowpt2)
#            is_frond = dict(((numbers[k[0]],numbers[k[1]]),frond[k]) for k in frond)
#            # run embedding algorithm with integrated pathfinder 
#            print ''
#            self.embed(A, is_frond)
            # make palm graph
            # plot palm tree
            P = nx.DiGraph(B_adjacency)
            nx.draw_shell(P)
            plt.show()
#            break

    def embed(self, A, is_frond):
        ''''''
        # recursion vars
        paths = []
        path = []
        s = [0]
        p = [0]
        # stacks
        NEXT = {'-1':0, 0:0}
        STACK = {0:0}
        B = []
        f = {}
        PATH = {1:1}
        FREE = [len(STACK)]
        # the recursive pathfinder function
        def pathfinder(v):
            ''''''
            global path
            for w in A[v]:
                if not is_frond[(v,w)]:
                    if s[0] == 0:
                        s[0] = v
                        p[0] = p[0] + 1
                        path = []
                    path.append((v,w))
                    PATH[w] = p[0]
                    pathfinder(w)
                    # Delete stack entries and blocks corresponding to vertices no smaller than v.
                    while len(B) and (((STACK[B[-1][0]] >= v) or (B[-1][0] == 0)) and ((STACK[B[-1][1]] >= v) or (B[-1][1] == 0))):
                        print 'delete from B : {0}'.format(B[-1])
                        del B[-1]
                    if len(B):
                        if STACK[B[-1][0]] >= v:
                            B[-1][0] = 0
                        if STACK[B[-1][1]] >= v:
                            B[-1][1] = 0
                    while (NEXT['-1'] != 0) and (STACK[NEXT['-1']] >= v):
                        NEXT['-1'] = NEXT[NEXT['-1']]
                    while (NEXT[0] != 0) and (STACK[NEXT[0]] >= v):
                        NEXT[0] = NEXT[NEXT[0]]
                    if PATH[w] != PATH[v]:
                        # All of segment with first edge (v,w) has been embedded.
                        # New blocks must be moved from right to left
                        L = 0
                        while len(B) and ((STACK[B[-1][0]] > f[PATH[w]]) or ((STACK[B[-1][1]] > f[PATH[w]]) and (STACK[NEXT['-1']] != 0))):
                            x = B[-1][0]
                            y = B[-1][1]
                            if STACK[x] > f[PATH[w]]:
                                if STACK[y] > f[PATH[w]]:
                                    print 'non-planar'
                                    return False
                                L = x
                            else:
                                # STACK[B[-1][1]] > f[PATH[w]]
                                temp = NEXT[L]
                                NEXT[L] = NEXT['-1']
                                NEXT['1'] = NEXT[y]
                                NEXT[y] = temp
                                L = y
                            print 'delete from B : {0}'.format(B[-1])
                            del B[-1]
                        # Current top block on B must be combined with new blocks just deleted.
                        if len(B):
                            x = B[-1][0]
                            y = B[-1][1]
                            print 'delete from B : {0}'.format(B[-1])
                            del B[-1]
                        else:
                            x = 0
                            y = 0
                        if x != 0:
                            print 'append to B   : {0} = ({1},{2})'.format((x,y),STACK[x],STACK[y])
                            B.append([x,y])
                        elif (L != 0) or (y != 0):
                            # x == 0
                            print 'append to B   : {0} = ({1},{2})'.format((L,y),STACK[L],STACK[y])
                            B.append([L,y])
                        # Delete end-of-stack marker on right stack.
                        NEXT['-1'] = NEXT[NEXT['-1']]
                else:
                    # Current path is complete.
                    # Path is normal if f[PATH[s]] < w
                    if s[0] == 0:
                        s[0] = v
                        p[0] = p[0] + 1
                        path = []
                    path.append((v,w))
                    paths.append(path)
                    f[p[0]] = w
                    # Switch blocks from left to right so that p may be embedded on the left.
                    L = 0
                    R = '-1' # instead of R = '-1'
                    while ((STACK[NEXT[L]] != 0) and (STACK[NEXT[L]] > w)) or ((STACK[NEXT[R]] != 0) and (STACK[NEXT[R]] > w)):
                        if len(B):
                            x = B[-1][0]
                            y = B[-1][1]
                            if (x != 0) and (y != 0) :
                                if STACK[NEXT[L]] > w:
                                    if STACK[NEXT[R]] > w:
                                        print 'non-planar'
                                        return False
                                    temp = NEXT[R]
                                    NEXT[R] = NEXT[L]
                                    NEXT[L] = temp
                                    temp = NEXT[x]
                                    NEXT[x] = y
                                    NEXT[y] = temp
                                    L = y
                                    R = x
                                else :
                                    # STACK[NEXT[R]] > w
                                    L = x
                                    R = y
                            elif x != 0 :
                                temp = NEXT[x]
                                NEXT[x] = NEXT[R]
                                NEXT[R] = NEXT[L]
                                NEXT[L] = temp
                                R = x
                            elif y != 0 :
                                R = y
                            print 'delete from B : {0}'.format(B[-1])
                            del B[-1]
                        # END OF IF
                    # END OF WHILE
                    # Add P to left stack if p is normal.
                    if f[PATH[s[0]]] < w:
                        if L == 0 :
                            L = FREE[0]
                        STACK[FREE[0]] = w # instead of STACK[FREE[0]] = f[PATH[s[0]]]
                        NEXT[FREE[0]] = NEXT[0]
                        NEXT[0] = FREE[0]
                        FREE[0] = FREE[0] + 1
                    # Add new block corresponding to combined old blocks.
                    # New block may be empty if segment containing current path
                    # is not a single frond.
                    if R == '-1' :
                        R = 0
                    if (L != 0) or (R != 0) or (v != s[0]) :
                        print 'append to B   : {0} = ({1},{2})'.format((L,R),STACK[L],STACK[R])
                        B.append([L,R])
                    # If segment containing current path is not a single frond
                    # add an end-of-stack marker to the right stack. 
                    if v != s[0] :
                        STACK[FREE[0]] = 0
                        NEXT[FREE[0]] = NEXT['-1']
                        NEXT['-1'] = FREE[0]
                        FREE[0] = FREE[0] + 1
                    s[0] = 0 
                # END OF IF
            # END OF FOR
            return True
        ################
        # execute the recursive algorithm
        pathfinder(1)
        print ''
        print 'PATHS (with palm numbering!) :'
        for p in paths:
            print p 
        print ''
        print 'STACK : {0}'.format(STACK)
        print 'NEXT  : {0}'.format(NEXT)
        print 'B     : {0}'.format(B)

    def sorted_adjacency_list(self, palm, V, numbers, is_frond, lowpt1, lowpt2):
        ''''''
        # a local helper function
        def edge_value(e):
            if is_frond[e]:
                value = 2*numbers[e[1]]
            else:
                if lowpt2[e[1]] >= e[0]:
                    value = 2*lowpt1[e[1]]
                else:
                    value = 2*lowpt1[e[1]] + 1
            return value
        # the actual sorting
        bucket = {}
        A = {}
        for i in range(1,2*V+2):
            bucket[i] = []
        for e in palm:
            pev = edge_value(e)
            bucket[pev].append(e)
        for i in range(1,V+1):
            A[i] = []
        for i in range(1,2*V+2):
            for e in bucket[i]:
                A[numbers[e[0]]].append(numbers[e[1]])
        return A
    
    ############################################################################
    # drawing stuff 
    ############################################################################

    def draw(self):
        ''''''
        G = nx.DiGraph(self.edges())
        coords = dict([(i,v[0:2]) for i,v in enumerate(self.vertices())])
        labels = dict([((uvd[0],uvd[1]),i) for i,uvd in enumerate(G.edges(data=True))])
        nx.draw(G, pos = coords, hold = True)
        nx.draw_networkx_edge_labels(G, pos = coords, edge_labels = labels)
        plt.axis('equal')
        plt.show()
        
    def draw_palm(self):
        ''''''
        pass
    
    def draw_dfs(self):
        ''''''
        pass
        
    def draw_embedding(self):
        ''''''
        pass

    ############################################################################
    # Helper functions
    # maybe make these private
    # maybe make the parameters used local
    ############################################################################

    def edge_cycle(self, sp,ep):
        ''''''
        cycle = []
        cycle.append(sp)
        while ep != cycle[0]:
            self._traverses[(sp,ep)] = 0
            cycle.append(ep)
            ngb = self.leftmost_neighbour(sp,ep)
            sp,ep = ep,ngb
        cycle.append(ep)
        self._traverses[(cycle[-2],cycle[-1])] = 0
        return cycle

    def first_neighbour(self, ep):
        ''''''
        xyz = self.V()
        ngb_angles = []
        neighbours = self.neighbours([ep])
        ngb_ids = neighbours[ep]
        v0 = [-1,-1,0]
        for ngb_id in ngb_ids:
            vN = (xyz[ngb_id] - xyz[ep]).tolist()
            a = 2*pi - angle(v0,vN)
            ngb_angles.append(round(a,3))
        return ngb_ids[ngb_angles.index(min(ngb_angles))]

    def leftmost_neighbour(self, sp,ep):
        ''''''
        xyz = self.V()
        ngb_angles = []
        neighbours = self.neighbours([ep])
        ngb_ids = neighbours[ep]
        v0 = (xyz[sp] - xyz[ep]).tolist()
        for ngb_id in ngb_ids:
            if ngb_id == sp:
                a = 2*pi
            else :
                vN = (xyz[ngb_id] - xyz[ep]).tolist()
                a = 2*pi - angle(v0,vN)
            ngb_angles.append(round(a,3))
        return ngb_ids[ngb_angles.index(min(ngb_angles))]
    
    def bottom_left(self):
        ''''''
        V = self.V()
        bottom = where(V[:,1] == min(V[:,1]))[0]
        left = where(V[bottom,0] == min(V[bottom,0]))
        return bottom[left[0][0]]    
    
################################################################################
################################################################################
################################################################################
# DUALGRAPH CLASS DEFINITION
################################################################################
################################################################################
################################################################################

# treat this completely different than a normal graph
# it is always constructed from another graph
# therefore, extend (still to be made) base graph class
# and require/allow other graph as input

class DualGraph(Graph):
    ''''''
    def __init__(self, Primal):
        '''Constructor'''
        super(DualGraph, self).__init__()
        self.Primal = Primal
        
    def vertices(self):
        ''''''
        return self.Primal.centroids()
    
    def edges(self):
        ''''''
        if self._edges is not None:
            return self._edges
        self._edges = []
        I = self.I()
        for column in I.T:
            nz = nonzero(column)[0].tolist()
            self._edges.append(nz)
        return self._edges           
    
    def V(self):
        ''''''
        if self._V is None:
            try:
                centroids = self.Primal.centroids()
                self._V = array(centroids)
            except:
                self._V = None
        return self._V 
        
    def I(self):
        ''''''
        if self._I is not None:
            return self._I
        v = self.Primal.c()
        e = self.Primal.e()
        self._I = zeros((v,e))
        # make more efficient look up tables
        edges = self.Primal.edges()
        cycles = self.Primal.cycles()
        edgedict = dict([((e[0],e[1]),i) for i,e in enumerate(edges)])
        # loop over the cycles of the primal
        for i in range(len(cycles)):
            cycle = cycles[i]
            for j in range(len(cycle) - 1):
                try:
                    k = edgedict[(cycle[j],cycle[j+1])]
                    self._I[i,k] = +1
                except KeyError:
                    k = edgedict[(cycle[j+1], cycle[j])]
                    self._I[i,k] = -1
        return self._I
    
    def analyse(self):
        ''''''
        self.I()
  
#################################################################################
#################################################################################
#################################################################################
## RECIPROCAL CLASS DEFINITION
#################################################################################
#################################################################################
#################################################################################
#
#class Reciprocal(Graph):
#    ''''''
#    def __init__(self, dual):
#        ''''''
#        super(Reciprocal, self).__init__()
#        # reference to the dual
#        self.Dual = dual
#        # matrices
#        self.V = None
#        # private scalars
#        self._n = None
#        self._m = None
#        # private lists
#        self._vertices = None
#        self._edges    = None
#        self._weights  = None
#
#    @property
#    def n(self):
#        ''''''
#        return self.Dual.n
#
#    @property
#    def m(self):
#        ''''''
#        return self.Dual.m
#
#    @property
#    def vertices(self):
#        ''''''
#        return array(self.V).tolist()
#
#    @property
#    def edges(self):
#        ''''''
#        return self.Dual.edges
#
#    @property
#    def weights(self):
#        '''Get the weights of the vertices of the network as a list.
#        If there are no weights yet, return 1 for anchors and 0 for all other vertices.
#        '''
#        if self._weights is None:
#            weights = [0]*self.n
#        else :
#            weights = self._weights
#        return weights
#    
#    
    