# imports
import Dijkstra as dijk
import misc
import numpy as np
import csv
import matplotlib.pyplot as plt


def nextNode(path):
    if len(path) == 1:
        return path[0]
    else:
        return path[1]


def update_weight_matrix(epsilon, c,weightMatrix,originalWeightMatrix):
    for l in range(noNodes):
        for m in range(noNodes):
            if weightMatrix[l, m] != float(0):
                weightMatrix[l, m] = originalWeightMatrix[l, m] + epsilon * (
                    float(c[l]) + float(c[m])) / float(2)
    return weightMatrix


if __name__ == '__main__':

    # import the rome edges file

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
    with open('./data/RomeEdges', 'r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeA = np.concatenate((RomeA, [int(row[0])]))
            RomeB = np.concatenate((RomeB, [int(row[1])]))
            RomeV = np.concatenate((RomeV, [float(row[2])]))
    file.close()

    wei = misc.calcWei(RomeX, RomeY, RomeA, RomeB, RomeV)
    temp_wei = wei.copy()

    # initialise minutes and number of nodes
    minutes = 200
    noNodes = wei.shape[0]

    # need a vector carNumbers which stores the number of cars at each vertex in the graph
    carNumbers = np.zeros(noNodes, dtype=int)

    for i in range(minutes):

        # this vector fastestRoute chooses the next node in the optimal (fastest route) using
        # Dijkstra's algorithm. Note this depends on temp_wei, the updated weight matrix.
        # we need to wrap this in the nextNode function as if we're already at node 52, the next
        # node (at index 1) is not defined.
        fastestRoute = [nextNode(dijk.Dijkst(int(node), 51, temp_wei)) for node in range(noNodes)]

        # we now need to iterate through the vector carNumbers, and move each car according to the next node it needs
        # to go to. But we can't iterate through a vector that we are constantly updating, so we make this copy
        # carNumbersUpdated.
        carNumbersUpdated = carNumbers.copy()

        # we move each car in the network according to rules 1,2 and 3 in the project outline.
        for jnode, numberOfCars in enumerate(carNumbers):

            # This is where cars at jnode have to move to next (step 1)
            nodeToMoveTo = fastestRoute[jnode]

            # We calculate the amount moving, and staying at jnode. (step 2)
            # We have a choice of using int(0.7*numberOfCars) and np.round(0.7*numberOfCars)
            # This isn't specified in the question, but I think it makes more sense to use np.round
            # since the question specifies "be particularly careful with rounding the number of cars
            # to the *nearest integer*".
            amountMoving = np.round(0.7 * numberOfCars)

            # We set amount staying as the number of cars currently at the node, minus the amount moving
            # This is so that the total number of cars is conserved, and not lost through rounding.
            amountStaying = carNumbersUpdated[jnode] - amountMoving

            # We then update the number of cars as required.
            carNumbersUpdated[jnode] = amountStaying
            carNumbersUpdated[nodeToMoveTo] += amountMoving

        # Now we need to remove cars from the system from node 52 (step 4). Again, we use np.round
        carNumbersUpdated[51] = np.round(carNumbersUpdated[51]*0.6)

        # Now we have finished iterating through carNumbers, we can update it with the new values.
        carNumbers = carNumbersUpdated.copy()

        # The initial conditions state to inject 20 cars at node 13 only for the first 180 iterations.
        if i <= 179:
            carNumbers[12] += 20

        # Now we need to update the weight matrix according to step 5.
        # This is at the bottom of the for loop, since step 5 clearly states to do this after
        # "all cars have moved to their new position". I interpret this as meaning after the
        # Initial injection.
        temp_wei = update_weight_matrix(0.01, carNumbers, temp_wei, wei)

        print(sum(carNumbers))





