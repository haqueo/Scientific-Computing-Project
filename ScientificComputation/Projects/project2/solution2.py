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

    virtual_start = int(weight_matrix.shape[0]) - 2
    virtual_finish = int(weight_matrix.shape[0]) - 1
    no_nodes = (int(weight_matrix.shape[0]) - 2) / 2

    weight_matrix[virtual_start, 0:no_nodes] = 0
    weight_matrix[no_nodes:virtual_start, virtual_finish] = 0

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

    data_frame = np.column_stack((job, duration, completed_before))

    return data_frame


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
    earliest_start = 0

    for node in job_sequence_iter:
        earliest_end = edge_values[node] + earliest_start

        start_stop[node, 0] = max(start_stop_array[node, 0], earliest_start)
        start_stop[node, 1] = max(start_stop_array[node, 1], earliest_end)

        earliest_start = earliest_end


def iterative_bell(adjusted_weights, edge_values):
    # create a copy of the weight matrix
    temp_weights = np.copy(adjusted_weights)

    # This is a list of 13 Falses
    # If a node appears in a job sequence (i.e. we know its start time)
    # it turns to true.
    removed_nodes = np.zeros(13, dtype=bool)
    counter = 0

    while counter < 13:  # O(1)

        job_sequence = updated_bellman_ford(26, 27, temp_weights)[1:-1:2]  # O(13*E) # all we can change is E

        # we write k = len(job_sequence)

        temp_weights[[node + 13 for node in job_sequence], 27] = 1  # O(k)

        current_time = 0  # O(1)

        for i, job in enumerate(job_sequence):  # O(k)

            if not removed_nodes[job]:  # O(1)

                start_times[job] = current_time  # O(1)
                counter += 1  # O(1)

            current_time += edge_values[job]  # O(1)

        # so the for loop is O(k) in total

        removed_nodes[job_sequence] = True  # O(1)

        print(job_sequence)

        # update start_stop_times
        # start_stop_times(job_sequence_iter=job_sequence,
        # start_stop_array=start_stop, edge_values=edge_values)


if __name__ == '__main__':
    data = generate_connectivity('./data/jobslist')

    weights = generate_weight_matrix(data)

    adjusted_weights = -1 * weights

    longest_path = updated_bellman_ford(26, 27, adjusted_weights)[1:-1:2]

    #######################################################################

    start_times = np.zeros(13, dtype=int)

    iterative_bell(adjusted_weights, data[:, 1])

    stop_times = [data[:, 1][i] + start_times[i] for i in range(13)]

    start_stop = zip(start_times, stop_times)
    print(start_stop)
