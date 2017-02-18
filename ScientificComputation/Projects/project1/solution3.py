# imports
import Dijkstra as dijk
import misc
import numpy as np
import csv
import matplotlib.pyplot as plt


def next_node(path):
    """ Returns the next index (after the node itself) in the path.
        If the path contains only one node, returns the node itself.
    """
    if len(path) == 1:
        return path[0]
    else:
        return path[1]


def update_weight_matrix(epsilon, c, original_weight_matrix,noNodes=58):
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
    new_weight_matrix = np.zeros((noNodes,noNodes))
    for i in range(noNodes):
        for j in range(noNodes):
            if original_weight_matrix[i, j] != float(0):
                new_weight_matrix[i, j] = original_weight_matrix[i, j] + \
                                          (epsilon * (float(c[i]) + float(c[j]))) / float(2)
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


if __name__ == '__main__':

    # Import the rome edges file
    extract_data()

    # Use the calcWei function from tutorials, along with the data set given
    # to calculate the weight matrix. Also create a copy which is the
    # temporary weight matrix.
    weightMatrix = misc.calcWei(RomeX, RomeY, RomeA, RomeB, RomeV)
    temp_wei = np.copy(weightMatrix)



    # Initialise minutes and number of nodes
    minutes = 200
    noNodes = weightMatrix.shape[0]

    # Need a vector carNumbers which stores the number of cars at each vertex
    # in the graph.
    carNumbers = np.zeros(noNodes, dtype=int)
    carNumbersUpdated = np.copy(carNumbers)
    maxCarNumbers = np.copy(carNumbers)

    # Iterate through the 200 minutes
    for i in range(minutes):

        # Apply Dijkstra's algorithm to find the fastest path to node 52 in the system.
        #
        fastestRoute = [next_node(dijk.Dijkst(node, 51, temp_wei)) for node in range(noNodes)]


        for jnode in range(noNodes):
            numberOfCars = carNumbers[jnode]
            nodeToMoveTo = fastestRoute[jnode]
            amountMoving = int(np.round(0.7 * numberOfCars))
            amountStaying = numberOfCars - amountMoving

            carNumbersUpdated[jnode] += amountStaying
            carNumbersUpdated[nodeToMoveTo] += amountMoving

        carNumbers = np.copy(carNumbersUpdated)

        carNumbersUpdated = np.zeros(noNodes, dtype=int)

        maxCarNumbers = [max(carNumbers[node], maxCarNumbers[node]) for node in range(noNodes)]

        carNumbers[51] = int(np.round(carNumbers[51] * 0.6))



        temp_wei = update_weight_matrix(0.01, carNumbers,weightMatrix)


        if i <= 179:
            carNumbers[12] += 20


    print(maxCarNumbers[30])