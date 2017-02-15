# imports
import Dijkstra as dijk
import misc
import numpy as np
import csv


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
    minutes = 1
    noNodes = wei.shape[0]

    # need a vector c which stores the number of cars at each vertex in the graph
    carNumbers = np.zeros(noNodes, dtype=int)
    # we initialise so there are 20 cars at node 13



    for i in range(minutes):

        if (minutes <= 179):
            carNumbers[12] += 20
        # inject 20 cars into node 13

        # cars choose the fastest route to node 52.


        # Need to change so that fastest route is calculated only if carNumbers[node]!= 0
        fastestRoute = [nextNode(dijk.Dijkst(int(node), 51, tempwei)) for node in range(noNodes)]


        # cars move to next node BUT
        # only 70% of each move to next node, 30% stay where they are


        carNumbersUpdate = carNumbers.copy()


        #carNumbersUpdate is carNumbersOld
        for jnode, numberOfCars in enumerate(carNumbers):

            amountMoving = int(0.7 * numberOfCars)
            newnoofcars = carNumbers[jnode]
            amountStaying = numberOfCars - amountMoving
            # so we don't add any new cars to the system

            # we have just moved the old cars to new node.
            nodeToMoveTo = fastestRoute[jnode]

            carNumbersUpdate[jnode] = amountStaying
            carNumbersUpdate[nodeToMoveTo] = carNumbersUpdate[nodeToMoveTo] + amountMoving
            # now we need to remove these cars from where they originally where
            if jnode == 13:
                print(carNumbersUpdate)


        # all the cars have now moved to their new positions.
        # at node 52, 40% of cars leave the network but 60% are left behind

        leaving51 = int(carNumbersUpdate[51] * 0.4)
        staying51 = carNumbersUpdate[51] - leaving51

        carNumbersUpdate[51] = staying51

        # update tempwei

        epsilon = 0.01
        for l in range(noNodes):
            for m in range(noNodes):
                if tempwei[l, m] != float(0):
                    tempwei[l, m] = wei[l, m] + epsilon * (float(carNumbersUpdate[l]) + float(carNumbersUpdate[m]))/ float(2)

        carNumbers = carNumbersUpdate.copy()


