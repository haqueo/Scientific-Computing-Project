# Imports
import numpy as np
import csv
import sys
import math as ma

# This import is needed for the last question
from solution_accident_occurs import max_index_tracker_no30


# ------------------------------------------------------------------------
# ---------------------    FUNCTIONS USED     ----------------------------
# ------------------------------------------------------------------------

def calcWei(RX, RY, RA, RB, RV):
    """
    This function is taken from Tutorials. It calculates the weight matrix
    given information about each node in the system.
    :param RX: The x coordinates of each node in the system
    :param RY: The y coordinates of each node in the system
    :param RA: the connectivity of each node in the system
    :param RB: the connectivity of each node in the system
    :param RV: the speed limits across each edge in the system
    :return: usable weight matrix
    """

    n = len(RX)
    wei = np.zeros((n, n), dtype=float)
    m = len(RA)
    for i in range(m):
        xa = RX[RA[i] - 1]
        ya = RY[RA[i] - 1]
        xb = RX[RB[i] - 1]
        yb = RY[RB[i] - 1]
        dd = ma.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)
        tt = dd / RV[i]
        wei[RA[i] - 1, RB[i] - 1] = tt
    return wei


def Dijkst(ist, isp, wei):
    """
    This Dijkstra's algorithm implementation is taken from tutorials.

    :param ist: the index of the starting node
    :param isp: the index of the node to reach
    :param wei: the assosciated weight matrix
    :return:
    """

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


def next_node(path):
    """ Returns the next index (after the node itself) in the path.
        If the path contains only one node, returns the node itself.
    """
    if len(path) == 1:
        return path[0]
    else:
        return path[1]


def update_weight_matrix(epsilon, c, original_weight_matrix, noNodes=58):
    """
    This function updates the weight matrix according to step 5 of the
    Project. Note the added fix - the weight matrix is not changed if
    the original entry was 0.



    :param epsilon: given in question
    :param c: the vector containing number of cars at each node
    :param original_weight_matrix: the weight matrix given by RomeEdges
    :param noNodes: number of nodes in the system
    :return: the updated weight matrix
    """
    new_weight_matrix = np.zeros((noNodes, noNodes))
    for i in range(noNodes):
        for j in range(noNodes):
            if original_weight_matrix[i, j] != float(0):
                new_weight_matrix[i, j] = original_weight_matrix[i, j] + \
                                          (epsilon * (float(c[i]) +
                                                      float(c[j]))) / float(2)
    return new_weight_matrix


def extract_data():
    """
    This function opens the RomeVertices and RomeEdges files, and creates
    global variables RomeX, RomeY, RomeA, RomeB and RomeV. These are variables
    used to create the original weight matrix.

    """
    global RomeX, RomeY, RomeA, RomeB, RomeV
    RomeX = np.empty(0, dtype=float)
    RomeY = np.empty(0, dtype=float)
    with open('./data/RomeVertices', 'r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeX = np.concatenate((RomeX, [float(row[1])]))
            RomeY = np.concatenate((RomeY, [float(row[2])]))
    file.close()
    RomeA = np.empty(0, dtype=int)
    RomeB = np.empty(0, dtype=int)
    RomeV = np.empty(0, dtype=float)
    with open('./data/RomeEdges2', 'r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeA = np.concatenate((RomeA, [int(row[0])]))
            RomeB = np.concatenate((RomeB, [int(row[1])]))
            RomeV = np.concatenate((RomeV, [float(row[2])]))
    file.close()

    # ----------------------------------------------------------------------
    # ---------------------    Main program     ----------------------------
    # ----------------------------------------------------------------------


def away_from_52(edge):
    """
    Tells you whether a given edge is pointing completely away from
    node 52, in both the x and y directions.
    :param edge: an edge of the form [a,b]
    :return: boolean whether or not this points to or away from 52
    """

    # extract data for access to global variables
    extract_data()

    # the edge is of the form [a,b]
    a = edge[0]
    b = edge[1]

    # use RomeX and RomeY to find the coordinates for a,b and node 52.
    a_coord = [RomeX[a - 1], RomeY[a - 1]]
    b_coord = [RomeX[b - 1], RomeY[b - 1]]
    coord52 = [RomeX[51], RomeY[51]]

    # find the change in x/y from a -> b
    x_change = b_coord[0] - a_coord[0]
    y_change = b_coord[1] - a_coord[1]

    # find the change in x/y from a -> 52
    x_changeTo52 = coord52[0] - a_coord[0]
    y_changeto52 = coord52[1] - a_coord[1]

    # if we're at 52 we're moving away from it
    if a == 52:
        return True

    # if both point in same direction, false.
    if (x_changeTo52 > 0) and (x_change > 0):
        return False
    elif (x_changeTo52 < 0) and (x_change < 0):
        return False

    # if both point in same direction, false.
    if (y_changeto52 > 0) and (y_change > 0):
        return False
    elif (y_changeto52 < 0) and (y_change < 0):
        return False

    # all other tests have passed, so must be True.
    return True


if __name__ == '__main__':

    # Import the rome edges file
    extract_data()
    print(RomeX.shape)

    # Use the calcWei function from tutorials, along with the data set given
    # to calculate the weight matrix. Also create a copy which is the
    # temporary weight matrix.
    weight_matrix = calcWei(RomeX, RomeY, RomeA, RomeB, RomeV)
    temp_wei = weight_matrix.copy()

    # Initialise minutes and number of nodes
    minutes = 200
    total_nodes = weight_matrix.shape[0]

    # Need a vector carNumbers which stores the number of cars at each vertex
    # in the graph.
    cars_at_node = np.zeros(total_nodes, dtype=int)
    cars_at_node_updated = cars_at_node.copy()  # cars_at_node updated is similar
    max_cars_at_node = cars_at_node.copy()  # max_cars_at_node is similar

    # To find the edges utilised, we need a 58x58 matrix of
    # False's. We will set each element to True if we move
    # cars from node i to node j.
    edge_utilised = np.zeros((total_nodes, total_nodes), dtype=bool)

    # Iterate through the 200 minutes
    for i in range(minutes):

        # Apply Dijkstra's algorithm to find the fastest path to node 52 in
        # the system. Then use next_node to find the next node in the given
        # path. (step 1)
        next_nodes = [next_node(Dijkst(node, 51, temp_wei))
                      for node in range(total_nodes)]

        # Move all cars as in steps 2,3. Iterate through every node in the
        # system to do this.
        for j_node in range(total_nodes):

            if j_node == 51:
                # We remove 40% of cars from node 52.
                cars_at_node_updated[51] += int(round(cars_at_node[51] * 0.6))
            else:

                # Initialise the number of cars at node j_node.
                number_of_cars = cars_at_node[j_node]

                # Initialise the next node to move to.
                node_to_move_to = next_nodes[j_node]

                # 70% of cars will move. to keep the total conserved, the amount
                # staying is just number_of_cars - amount_moving
                amount_moving = int(round(0.7 * number_of_cars))
                amount_staying = number_of_cars - amount_moving

                # We now update cars_at_node.
                cars_at_node_updated[j_node] += amount_staying
                cars_at_node_updated[node_to_move_to] += amount_moving

                if amount_moving > 0:
                    # Update edges_utilised matrix
                    edge_utilised[j_node, node_to_move_to] = True

        # Now all cars have moved where they need to, we set cars_at_node
        # to this updated vector, and empty the updated vector for the next
        # iteration.
        cars_at_node = cars_at_node_updated.copy()
        cars_at_node_updated = np.zeros(total_nodes, dtype=int)

        # For the first 180 minutes, 20 cars are injected into node 13.
        if i <= 179:
            cars_at_node[12] += 20

        # The temporary weight matrix is updated.
        temp_wei = update_weight_matrix(0.01, cars_at_node, weight_matrix)

        # We have finished an iteration.

        # Now we calculate the maximum number of cars at each node in the system.
        max_cars_at_node = [max(cars_at_node[node], max_cars_at_node[node])
                            for node in range(total_nodes)]

    # ------------------------------------------------------------------------
    # ---------------------    Analytics/questions ---------------------------
    # ------------------------------------------------------------------------

    # Question: Determine for each node the maximum load (maximum number of cars)
    # over the 200 iterations.

    max_index_tracker = [[node + 1, max_cars_at_node[node]]
                         for node in range(total_nodes)]
    # print('max_index_tracker is')
    # print(max_index_tracker[0:10])
    # print(max_index_tracker[10:20])
    # print(max_index_tracker[20:30])
    # print(max_index_tracker[30:40])
    # print(max_index_tracker[40:50])
    # print(max_index_tracker[50:(len(max_index_tracker)+1)])

    # Question: Which are the five most congested nodes?

    top_five = sorted(max_index_tracker,
                      key=lambda node_and_max: -1 * node_and_max[1])[:5]
    # print('the five most congested nodes are')
    # print(top_five)

    # Question: Which edges are not utilized at all? Why?

    non_utilised_edges_matrix = (weight_matrix != float(0)) \
                                & (np.logical_not(edge_utilised))

    non_utilised_edges = [[i + 1, j + 1] for i in range(total_nodes)
                          for j in range(total_nodes)
                          if non_utilised_edges_matrix[i, j]]
    # print('the non utilised edges are')
    # print(non_utilised_edges[0:10])
    # print(non_utilised_edges[10:20])
    # print(non_utilised_edges[20:30])
    # print(non_utilised_edges[30:40])
    # print(non_utilised_edges[40:50])
    # print(non_utilised_edges[50:60])
    # print(non_utilised_edges[60:(len(non_utilised_edges)+1)])

    # long explanation to follow
    # print(len(non_utilised_edges))

    # Question: What flow pattern do we observe for parameter epsilon = 0?

    # see solution_epsilon0.py

    # Question: An accident occurs at node 30 (python-index 29) which blocks any route to
    # or from node 30. Which nodes are now the most congested and what is their maximum load?
    # Which nodes (besides node 30) decrease the most in peak value, which nodes in- crease
    # the most in peak value?

    # see solution_accident_occurs.py to see how the weight matrix is adjusted to find
    # max_index_tracker_no30.

    # need import at top

    top_ten = sorted(max_index_tracker_no30,key=lambda node_and_max: -1*node_and_max[1])[:10]
    print(top_ten)
    
    differences = []
    for k in range(total_nodes):
        if k == 29:
            differences.append([k, 0])  # ignore when analysing
        else:
            differences.append([k, max_index_tracker[k][1] - max_index_tracker_no30[k][1]])

    sorted_differences_most = sorted(differences, key=lambda node_and_max: -1 * node_and_max[1])[:5]
    sorted_differences_least = sorted(differences, key=lambda node_and_max: node_and_max[1])[:5]
    print(sorted_differences_most)
    print(sorted_differences_least)



    new_unused = list(non_utilised_edges)

    for _, edge in enumerate(non_utilised_edges):
        if away_from_52(edge):
            new_unused.remove(edge)

    print('length of new_unused is %i' % len(new_unused))
