# imports
import Dijkstra as dijk
import misc
import numpy as np
import csv
# this import is needed for the last question
from solution_accident_occurs import max_index_tracker_no30


# ------------------------------------------------------------------------
# ---------------------    FUNCTIONS USED     ----------------------------
# ------------------------------------------------------------------------

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


# ------------------------------------------------------------------------
# ---------------------    Main program     ----------------------------
# ------------------------------------------------------------------------


if __name__ == '__main__':

    # Import the rome edges file
    extract_data()

    # Use the calcWei function from tutorials, along with the data set given
    # to calculate the weight matrix. Also create a copy which is the
    # temporary weight matrix.
    weight_matrix = misc.calcWei(RomeX, RomeY, RomeA, RomeB, RomeV)
    temp_wei = weight_matrix.copy()

    # Initialise minutes and number of nodes
    minutes = 200
    noNodes = weight_matrix.shape[0]

    # Need a vector carNumbers which stores the number of cars at each vertex
    # in the graph.
    cars_at_node = np.zeros(noNodes, dtype=int)
    cars_at_node_updated = cars_at_node.copy()  # cars_at_node updated is similar
    max_cars_at_node = cars_at_node.copy()  # max_cars_at_node is similar

    # To find the edges utilised (or not utilised), we need a 58x58 matrix of
    # zeros.
    edges_utilised = np.zeros((noNodes, noNodes), dtype=int)

    # Iterate through the 200 minutes
    for i in range(minutes):

        # Apply Dijkstra's algorithm to find the fastest path to node 52 in
        # the system. Then use next_node to find the next node in the given
        # path. (step 1)
        next_nodes = [next_node(dijk.Dijkst(node, 51, temp_wei))
                      for node in range(noNodes)]

        # Move all cars as in steps 2,3. Iterate through every node in the
        # system to do this.
        for j_node in range(noNodes):

            # Initialise the number of cars at node j_node.
            number_of_cars = cars_at_node[j_node]

            # Initialise the next node to move to.
            node_to_move_to = next_nodes[j_node]

            # 70% of cars will move. to keep the total conserved, the amount
            # staying is just number_of_cars - amount_moving
            amount_moving = int(np.round(0.7 * number_of_cars))
            amount_staying = number_of_cars - amount_moving

            # We now update cars_at_node.
            cars_at_node_updated[j_node] += amount_staying
            cars_at_node_updated[node_to_move_to] += amount_moving

            # Update edges_utilised matrix
            edges_utilised[j_node, node_to_move_to] += 1

        # Now all cars have moved where they need to, we set cars_at_node
        # to this updated vector, and empty the updated vector for the next
        # iteration.
        cars_at_node = cars_at_node_updated.copy()
        cars_at_node_updated = np.zeros(noNodes, dtype=int)

        # Now we calculate the maximum number of cars at each node in the system.
        max_cars_at_node = [max(cars_at_node[node], max_cars_at_node[node]) for node in range(noNodes)]

        # Now we remove 40% of cars from node 52.
        cars_at_node[51] = int(np.round(cars_at_node[51] * 0.6))

        # The temporary weight matrix is updated.
        temp_wei = update_weight_matrix(0.01, cars_at_node, weight_matrix)

        # For the first 180 minutes, 20 cars are injected into node 13.
        if i <= 179:
            cars_at_node[12] += 20

# ------------------------------------------------------------------------
# ---------------------    Analytics/questions ---------------------------
# ------------------------------------------------------------------------

    # Question: Determine for each node the maximum load (maximum number of cars)
    # over the 200 iterations.
    max_index_tracker = [[node + 1, max_cars_at_node[node]] for node in range(noNodes)]

    # Question: Which are the five most congested nodes?
    top_five = sorted(max_index_tracker, key=lambda node_and_max: -1 * node_and_max[1])[:5]

    # Question: Which edges are not utilized at all? Why?
    not_utilised = []
    for i in range(noNodes):
        for j in range(noNodes):
            if (weight_matrix[i, j] != 0) and (edges_utilised[i, j] == 0):
                not_utilised.append([i + 1, j + 1])

    # Question: What flow pattern do we observe for parameter epsilon = 0?
    # see solution_epsilon0.py

    # Question: An accident occurs at node 30 (python-index 29) which blocks any route to
    # or from node 30. Which nodes are now the most congested and what is their maximum load?
    # Which nodes (besides node 30) decrease the most in peak value, which nodes in- crease
    # the most in peak value?

    differences = []
    for k in range(noNodes):
        if k == 12:
            differences.append([k, 0])  # ignore when analysing
        else:
            differences.append([k, max_index_tracker[k][1] - max_index_tracker_no30[k][1]])

    sorted_differences_most = sorted(differences, key=lambda node_and_max: -1 * node_and_max[1])[:5]
    sorted_differences_least = sorted(differences, key=lambda node_and_max: node_and_max[1])[:5]

