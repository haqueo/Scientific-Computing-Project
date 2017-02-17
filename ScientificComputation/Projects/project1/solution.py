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
    tempwei = wei.copy()

    # initialise minutes and number of nodes
    minutes = 200
    noNodes = wei.shape[0]

    # need a vector c which stores the number of cars at each vertex in the graph
    carNumbers = np.zeros(noNodes, dtype=int)
    # we initialise so there are 20 cars at node 13
    maxNumberCars = np.zeros(noNodes, dtype=int)

    for i in range(minutes):


        # print(sum(carNumbers))
        fastestRoute = [nextNode(dijk.Dijkst(int(node), 51, tempwei)) for node in range(noNodes)]

        carNumbersUpdated = carNumbers.copy()

        for jnode, numberOfCars in enumerate(carNumbers):

            nodeToMoveTo = fastestRoute[jnode]

            # USING NP. ROUND

            # alternatively: amountMoving = int(0.7 * numberOfCars)
            amountMoving = np.round(0.7 * numberOfCars)

            # amountStaying is not just 30%, but "the rest" to ensure that
            # amountStaying + amountMoving = carNumbersUpdated[jnode]
            amountStaying = carNumbersUpdated[jnode] - amountMoving



            carNumbersUpdated[jnode] = amountStaying
            carNumbersUpdated[nodeToMoveTo] += amountMoving

        # FIND MAXIMUM NUMBER OF CARS AT EACH NODE


        # all the cars have now moved to their new positions.
        # at node 52, 40% of cars leave the network but 60% are left behind

        ## USING np.round, alternatively: leaving51 = int(carNumbersUpdated[51] * 0.4)

        leaving51 = np.round(carNumbersUpdated[51] * 0.4)
        carNumbersUpdated[51] = carNumbersUpdated[51] - leaving51



        # update tempwei

        tempwei = update_weight_matrix(0.01, carNumbersUpdated,tempwei,wei)

        # carNumbersOld becomes updated
        carNumbers = carNumbersUpdated.copy()

        if (i <= 179):
            carNumbers[12] += 20



        print(sum(carNumbers))






    # c = [0,0,...,0]

    for i in range(200):

        # use c, and move all the cars according to the rules and weight matrix

        # remove cars from node 51

        # update the weight matrix

        # inject 20 cars if i <= 179

      pass