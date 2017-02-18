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


def update_weight_matrix(epsilon, c, weightMatrix, originalWeightMatrix):
    for l in range(noNodes):
        for m in range(noNodes):
            if originalWeightMatrix[l, m] != float(0):
                weightMatrix[l, m] = originalWeightMatrix[l, m] + epsilon * (
                    float(c[l]) + float(c[m])) / float(2)
    return weightMatrix


def extract_data():
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
    with open('./data/RomeEdges', 'r') as file:
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
    # to calculate the weight matrix. Also create a copy which is the temporary
    # weight matrix.
    wei = misc.calcWei(RomeX, RomeY, RomeA, RomeB, RomeV)
    temp_wei = wei.copy()

    # Initialise minutes and number of nodes
    minutes = 200
    noNodes = wei.shape[0]
    # Need a vector carNumbers which stores the number of cars at each vertex in the graph
    carNumbers = np.zeros(noNodes, dtype=int)
    maxCarNumbers = carNumbers.copy()

    for i in range(minutes):

        fastestRoute = [nextNode(dijk.Dijkst(int(node), 51, temp_wei)) for node in range(noNodes)]

        for jnode in range(noNodes):
            numberOfCars = carNumbers[jnode]
            nodeToMoveTo = fastestRoute[jnode]

            amountMoving = int(np.round(0.7*numberOfCars))
            amountStaying = numberOfCars - amountMoving

            carNumbers[jnode] = amountStaying
            carNumbers[nodeToMoveTo] += amountMoving


        carNumbers[51] = int(np.round(carNumbers[51] * 0.6))

        if i <= 179:
            carNumbers[12] += 20

        maxCarNumbers = [max(carNumbers[node], maxCarNumbers[node]) for node in range(noNodes)]
        print("i is %i" % i)
        print(carNumbers)

        temp_wei = update_weight_matrix(0.01, carNumbers, temp_wei, wei)
    print(max(maxCarNumbers))