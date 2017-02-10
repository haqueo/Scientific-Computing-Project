## FILE TO BE MODIFIED ONLY WHERE REQUIRED


import numpy as np
import scipy as sp
import sys


# ------------------------------------------------------------------------
# ---------------------    FUNCTIONS USED     ----------------------------
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
def ImportData(filename):
    import csv
    data = []

    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([float(x) for x in row])
    # elementary
    return np.array(data)


# ------------------------------------------------------------------------
def Weights_vals(path, wei):  # you might find this routine useful

    #path = [1,2,3]

    #add the first member of the path, to the end of path
    path.append(path[0])

    #path = [1,2,3,1]

    #path 2 is the reverse of path
    path2 = path[::-1]

    #path = [1,3,2,1]

    #for i in 0,1,2
    #w1 = [wei[path[i],path[i+1]]

    w1 = [wei[path[i], path[i + 1]] for i in range(len(path) - 1)]
    w2 = [wei[path2[i], path2[i + 1]] for i in range(len(path2) - 1)]

    # if w1 == w2, then path is a cycle.

    return w1, w2


# ------------------------------------------------------------------------
def Relaxation_step(wei):  # do not modify this routine to be used as provided
    V = wei.shape[1]

    # step 1: initialization
    Inf = sys.maxint
    d = np.ones((V), float) * np.inf
    p = np.zeros((V), int)
    d[0] = 0

    for i in range(0, V - 1):
        for u in range(0, V):
            for v in range(0, V):
                w = wei[u, v]
                if (w != 0):
                    if (d[u] + w < d[v]):
                        d[v] = d[u] + w
                        p[v] = u
    return p, d


# ------------------------------------------------------------------------
def BellmanFord(wei):  # MODIFY WHERE ASKED!
    # initialize outputs
    print(wei)
    npaths = []

    # step 1: iterative relaxation
    p, d = Relaxation_step(wei)


    # step 3: check for negative-weight cycles (basically doing 1 extra iteration)
    # make a copy of the distances and check it doesnt change
    g = []
    d2 = np.copy(d)
    p2 = np.copy(p)
    V = wei.shape[1]
    for u in range(0, V):
        for v in range(0, V):
            w = wei[u, v]
            if (w != 0):
                if (d2[u] + w < d2[v]):
                    d2[v] = d2[u] + w
                    p2[v] = u
                    if v not in g:
                        g.append(v)
                    #node v is part of a negative cycle.



    print(g)
    print(p)
    print(p2)
    if len(g) == 0:
        val = False
    else:
        val = True
        b = (np.array(d) != np.array(d2))
        g = np.array(range(V))[b]

    ############################################################################
    #    complete here   PART 3 (about 2-4 lines) 
    # step 4: are there negative cycles? 
    #         which vertices are intrested?

    ############################################################################

    # step 5: identify those loops
    if val:
        print 'graph contains a negative-weight cycle'
        for i in g:  # g is a list, contains the vertices of the negative cycle
            print 'this section should identify the loops'
            path = []
            currentNode = i
            nextNode = p[currentNode]

            # while(nextNode!=currentNode):



            ############################################################################
            #   complete here PART 4
            ##########################################################################

    return npaths  # routine can also return other lists


# ------------------------------------------------------------------------



# ------------------------------------------------------------------------
# ---------------------    Main programme     ----------------------------
# ------------------------------------------------------------------------


if __name__ == '__main__':
    # load data
    filename = 'Data2.txt'
    data = ImportData(filename)

    # prepare for the BellmanFord routine

    ###########################################
    #	complete here PART 2 (about 1-2 lines)
    wei = -np.log(data) # modify apporopiately
    ###########################################

    # call bellmanford routine on the data
    paths = BellmanFord(wei)

    # display the paths and profit made
    ###########################################
    #  complete here PART 5 (easy peasy)
    # print 'Display your identified cylces here (make it neat)'
    ###############################################

# ------------------------------------------------------------------------
# ---------------------        The end        ----------------------------
# ------------------------------------------------------------------------
