import numpy as np
import scipy as sp
import math as ma
import sys
import time


def Dijkst(ist, isp, wei):
    # Dijkstra algorithm for shortest path in a graph
    #    ist: index of starting node
    #    isp: index of stopping node
    #    wei: weight matrix

    # exception handling (start = stop)
    if ist == isp:
        shpath = [ist]
        return shpath

    # initialization
    N = len(wei)
    Inf = sys.maxint
    UnVisited = np.ones(N, int)
    cost = np.ones(N) * 1.e6
    par = -np.ones(N, int) * Inf

    # set the source point and get its (unvisited) neighbors
    jj = ist
    cost[jj] = 0
    UnVisited[jj] = 0
    tmp = UnVisited * wei[jj, :]
    ineigh = np.array(tmp.nonzero()).flatten()
    L = np.array(UnVisited.nonzero()).flatten().size

    # start Dijkstra algorithm
    while (L != 0):
        # step 1: update cost of unvisited neighbors,
        #         compare and (maybe) update
        for k in ineigh:
            newcost = cost[jj] + wei[jj, k]
            if (newcost < cost[k]):
                cost[k] = newcost
                par[k] = jj

        # step 2: determine minimum-cost point among UnVisited
        #         vertices and make this point the new point
        icnsdr = np.array(UnVisited.nonzero()).flatten()
        cmin, icmin = cost[icnsdr].min(0), cost[icnsdr].argmin(0)
        jj = icnsdr[icmin]

        # step 3: update "visited"-status and determine neighbors of new point
        UnVisited[jj] = 0
        tmp = UnVisited * wei[jj, :]
        ineigh = np.array(tmp.nonzero()).flatten()
        L = np.array(UnVisited.nonzero()).flatten().size

    # determine the shortest path
    shpath = [isp]
    while par[isp] != ist:
        shpath.append(par[isp])
        isp = par[isp]
    shpath.append(ist)

    return shpath[::-1]