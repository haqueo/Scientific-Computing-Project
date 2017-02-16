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
    minutes = 201
    noNodes = wei.shape[0]

    # need a vector c which stores the number of cars at each vertex in the graph
    carNumbers = np.zeros(noNodes, dtype=int)
    # we initialise so there are 20 cars at node 13
    maxNumberCars = np.zeros(noNodes, dtype=int)

    plotofsum = np.zeros(201,dtype=int)

    carNumbers[12] = 20

    for i in range(minutes):

        if (i <= 179):
            carNumbers[12] += 20

        fastestRoute = [nextNode(dijk.Dijkst(int(node), 51, tempwei)) for node in range(noNodes)]

        carNumbersUpdated = carNumbers.copy()

        for jnode, numberOfCars in enumerate(carNumbers):

            amountMoving = int(0.7 * numberOfCars)

            # amountStaying is not just 30%, but "the rest" to ensure that
            # amountStaying + amountMoving = carNumbersUpdated[jnode]
            amountStaying = carNumbersUpdated[jnode] - amountMoving

            nodeToMoveTo = fastestRoute[jnode]

            carNumbersUpdated[jnode] = amountStaying
            carNumbersUpdated[nodeToMoveTo] += amountMoving

        #FIND MAXIMUM NUMBER OF CARS AT EACH NODE


        # all the cars have now moved to their new positions.
        # at node 52, 40% of cars leave the network but 60% are left behind

        leaving51 = int(carNumbersUpdated[51] * 0.4)
        staying51 = carNumbersUpdated[51] - leaving51

        carNumbersUpdated[51] = staying51


        #carNumbersOld becomes updated
        carNumbers = carNumbersUpdated.copy()

        # update tempwei

        epsilon = 0.01
        for l in range(noNodes):
            for m in range(noNodes):
                if tempwei[l, m] != float(0):
                    tempwei[l, m] = wei[l, m] + epsilon * (
                        float(carNumbersUpdated[l]) + float(carNumbersUpdated[m])) / float(2)

        plotofsum[i] = sum(carNumbers)



    plt.figure()

    plt.plot(range(201),plotofsum)

    plt.show()
