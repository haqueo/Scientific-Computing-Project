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
                    # print('graph contains a negative-weight cycle')
                    pass

    # step 4: determine the shortest path
    shpath = [isp]
    while p[isp] != ist:
        shpath.append(p[isp])
        isp = p[isp]
    shpath.append(ist)

    return shpath[::-1]


def start_stop_times(job_sequence_iter, start_stop_array, edge_values):
    earliest_start2 = 0

    for node in job_sequence_iter:
        earliest_end2 = edge_values[node] + earliest_start2

        start_stop[node, 0] = max(start_stop_array[node, 0], earliest_start2)
        start_stop[node, 1] = max(start_stop_array[node, 1], earliest_end2)

        earliest_start2 = earliest_end2


def iterative_bell(adjusted_weights, edge_values):

    # create a copy of the weight matrix
    temp_weights = np.copy(adjusted_weights)

    # create a set called 'removed'
    # this will contain the nodes which we have removed connections with from
    #  the virtual start node. When the size of this set reaches 13, we know
    # we have covered all paths in the network
    removed_nodes = set()

    while len(removed_nodes) < 13:

        full_bellman_path = updated_bellman_ford(26, 27, temp_weights)
        # print("full_bellman_path is %s" % str(full_bellman_path))

        job_sequence = full_bellman_path[1:-1:2]

        if len(job_sequence) > 1:
            last_pair = [job_sequence[-2], job_sequence[-1]]
            removed_nodes.add(last_pair[1])
        else:
            last_pair = [job_sequence[0], 27]
            removed_nodes.add(last_pair[0])

        # remove the last pair from the adjusted_weights
        temp_weights[node_finish(last_pair[0]), last_pair[1]] = 1
        # remove the virtual start node going to b
        temp_weights[26, last_pair[1]] = 1

        print(job_sequence)

        # update start_stop_times
        start_stop_times(job_sequence_iter=job_sequence,
                         start_stop_array=start_stop, edge_values=edge_values)


if __name__ == '__main__':

    data = generate_connectivity('./data/jobslist')

    weights = generate_weight_matrix(data)

    adjusted_weights = -1 * weights

    path = updated_bellman_ford(26, 27, adjusted_weights)
    longest_path = path[1:-1:2]

    start_stop = np.zeros((13, 2), dtype=int)

    iterative_bell(adjusted_weights, data[:, 1])

    print(start_stop)
