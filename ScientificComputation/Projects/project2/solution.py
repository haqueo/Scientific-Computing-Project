import csv
import numpy as np
import sys


def node_finish(node):
    return node + 13


def generate_weight_matrix(data):
    total_nodes = data.shape[0]
    weight_matrix = -1 * np.ones((2 * total_nodes + 2, 2 * total_nodes + 2), dtype=int)

    for row in data:

        node_start = row[0]
        weight = row[1]
        jobs = row[2]

        weight_matrix[node_start, node_finish(node_start)] = weight

        for job in jobs:
            weight_matrix[node_finish(node_start), job] = 0

    ## virtual start = 26
    ## virtual finish = 27
    ## nodes = 13

    weight_matrix[26, 0:13] = 0
    weight_matrix[13:26, 27] = 0

    return weight_matrix


def generate_connectivity(file_name):
    global completed_before, duration
    # e.g. file_name = './data/jobslist'
    job = []
    duration = []
    completed_before = []

    with open(file_name, 'r') as file:

        AAA = csv.reader(file)

        for i, row in enumerate(AAA):

            job.append(int(row[0]))

            duration.append(int(row[1]))

            if len(row) > 2:
                completed_before.append([int(node) for node in row[2:]])

            else:
                completed_before.append([])

    file.close()

    dataframe = np.column_stack((job, duration, completed_before))

    return dataframe


def updated_bellman_ford(ist, isp, wei):
    # ----------------------------------
    #  ist:    index of starting node
    #  isp:    index of stopping node
    #  wei:    adjacency matrix (V x V)
    #
    #  shpath: shortest path
    # ----------------------------------

    V = wei.shape[1]

    # step 1: initialization
    Inf = sys.maxint
    d = np.ones((V), float) * np.inf
    p = np.zeros((V), int) * Inf
    d[ist] = 0

    # step 2: iterative relaxation
    for i in range(0, V - 1):
        for u in range(0, V):
            for v in range(0, V):
                w = wei[u, v]
                if (w != 1):
                    if d[u] + w < d[v]:
                        d[v] = d[u] + w
                        p[v] = u

    # step 3: check for negative-weight cycles
    for u in range(0, V):
        for v in range(0, V):
            w = wei[u, v]
            if (w != 0):
                if (d[u] + w < d[v]):
                    #print('graph contains a negative-weight cycle')
                    pass

    # step 4: determine the shortest path
    shpath = [isp]
    while p[isp] != ist:
        shpath.append(p[isp])
        isp = p[isp]
    shpath.append(ist)

    return shpath[::-1]

def iterative_bell():

    # initialise data and weight matrix
    data = generate_connectivity('./data/jobslist')
    weights = generate_weight_matrix(data)
    adjusted_weights = -1*weights

    # create a copy of weight matrix
    temp_weights = adjusted_weights

    # create a list of current nodes
    current_nodes = range(13)

    # create a list of the longest paths
    list_of_longest_paths = []

    # iterate until there are no more current nodes
    while len(current_nodes) != 0:

        # find the longest path
        path = updated_bellman_ford(26,27,temp_weights)
        longest_path = path[1:len(path)-1][::2]

        # add this to the list of longest paths
        list_of_longest_paths.append(longest_path)

        for node in longest_path:

            # remove every node in the list of longest
            # paths from current_nodes
            current_nodes.remove(node)

            # update the weight matrix so no nodes
            # can move to these nodes
            temp_weights[:,node] = 1
            temp_weights[:,node] = 1

    return list_of_longest_paths

def iterative_bell2():

    # initialise data and weight matrix
    data = generate_connectivity('./data/jobslist')
    weights = generate_weight_matrix(data)
    adjusted_weights = -1*weights

    # create a copy of weight matrix
    temp_weights = adjusted_weights

    # create a list of the longest paths
    list_of_longest_paths = []

    not_reached = range(13)

    while len(not_reached) != 0:
        # find the shortest path ie the longest

        # find the longest path
        path = updated_bellman_ford(26,27,temp_weights)
        longest_path = path[1:len(path)-1][::2]
        print(longest_path)
        # add this to the list of longest paths
        list_of_longest_paths.append(longest_path)

        for i,node in enumerate(longest_path):

            if node in not_reached:
                not_reached.remove(node)

            if node != longest_path[-1]:
                temp_weights[node_finish(node),longest_path[i+1]] = 1

    return list_of_longest_paths

def one_step_at_a_time():
    shortest = [0,1,4]





if __name__ == '__main__':

    # data = generate_connectivity('./data/jobslist')
    #
    # weights = generate_weight_matrix(data)
    #
    # adjusted_weights = -1 * weights
    #
    # path = updated_bellman_ford(26, 27, adjusted_weights)
    # longest_path = path[1:len(path)-1][::2]
    #
    # print(longest_path)

    # real question


    paths1 = iterative_bell()
    final_gantt = np.zeros((13,2),dtype=int)
    # print(final_gantt)

    # can_move = [i for i in range(13) if i not in completed_before]
    # for subpath in paths1:
    #     if subpath[0] in can_move:


    times = [[0,41],[41,92],[0,50],[50,86],[92,130],[21,66],[0,21],[66,98],[0,32],[21,70],[41,71],[70,89],[92,118]]
    print(times)

    # print(times)


    # print(completed_before)




    # try 2

    # print(iterative_bell2())


